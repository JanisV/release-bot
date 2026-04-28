import asyncio
import json
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import github
import telegram
import urllib3
from github.GitRelease import GitRelease
from github.Tag import Tag
from telegram import LinkPreviewOptions
from telegram.constants import MessageLimit, ParseMode

from app import models
from app import github_obj, db, telegram_bot, scheduler
from app.models import ChatRepo, ReleaseNotification
from app.repo_engine import store_latest_release, format_release_message


OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
SUMMARY_MAX_RELEASE_BODY_CHARS = 8000
SUMMARY_FALLBACK_SNIPPET_CHARS = 240
SUMMARY_TRUNCATION_SUFFIX = "\n...[truncated]"


def _parse_daily_summary_time(value):
    if not value:
        return None

    parts = value.strip().split(":")
    if len(parts) != 2:
        raise ValueError("DAILY_SUMMARY_TIME must be in HH:MM format")

    hour = int(parts[0])
    minute = int(parts[1])
    if hour < 0 or hour > 23 or minute < 0 or minute > 59:
        raise ValueError("DAILY_SUMMARY_TIME must be a valid 24h time")

    return hour, minute


def _normalize_release_body(body):
    if not body:
        return ""
    body = body.strip()
    if len(body) > SUMMARY_MAX_RELEASE_BODY_CHARS:
        body = f"{body[:SUMMARY_MAX_RELEASE_BODY_CHARS]}{SUMMARY_TRUNCATION_SUFFIX}"
    return body


def _day_window_utc(now_utc, tz_name):
    tz = ZoneInfo(tz_name)
    local_now = now_utc.astimezone(tz)
    day_start_local = local_now.replace(hour=0, minute=0, second=0, microsecond=0)
    day_end_local = day_start_local + timedelta(days=1)
    return (day_start_local.astimezone(timezone.utc),
            day_end_local.astimezone(timezone.utc),
            day_start_local.date().isoformat())


def _trim_message(text, max_len=MessageLimit.MAX_TEXT_LENGTH):
    if len(text) <= max_len:
        return text
    return f"{text[:max_len - len(SUMMARY_TRUNCATION_SUFFIX)]}{SUMMARY_TRUNCATION_SUFFIX}"


def _build_summary_prompt(notifications, day_label, tz_name):
    items = []
    for note in notifications:
        body = _normalize_release_body(note.release_body)
        if not body:
            body = "No changelog provided."
        items.append(
            "Repo: {repo}\nTag: {tag}\nTitle: {title}\nURL: {url}\nChangelog:\n{body}".format(
                repo=note.repo_full_name or "Unknown",
                tag=note.release_tag or "",
                title=note.release_title or "",
                url=note.release_url or note.repo_link or "",
                body=body,
            )
        )

    header = (
        "You are a release notes assistant. Summarize today's release notifications.\n"
        "Day: {day} ({tz})\n"
        "Rules:\n"
        "- Include every item; do not merge or omit items.\n"
        "- For each item, provide repo name, version/tag, and 1-3 bullet highlights.\n"
        "- Output must be Telegram Markdown (not MarkdownV2).\n"
        "- Use *bold* for headings, use '-' for bullets.\n"
        "- Avoid underscores, backticks, tables, and code blocks.\n"
        "- Use plain URLs (no Markdown links).\n"
        "- Keep the output under 3000 characters.\n\n"
        "Items:\n"
    ).format(day=day_label, tz=tz_name)

    items_text = "\n---\n".join(items)
    return f"{header}{items_text}"


def _fallback_summary(notifications, day_label, tz_name):
    lines = [f"*Release Summary* - {day_label} ({tz_name})", ""]
    for note in notifications:
        title = note.release_title or ""
        tag = note.release_tag or ""
        line = f"- *Repo:* {note.repo_full_name or 'Unknown'}".strip()
        if tag or title:
            detail = " ".join(part for part in [tag, title] if part)
            line = f"{line} ({detail})"
        lines.append(line)
        if note.release_body:
            snippet = " ".join(note.release_body.split())
            if len(snippet) > SUMMARY_FALLBACK_SNIPPET_CHARS:
                snippet = f"{snippet[:SUMMARY_FALLBACK_SNIPPET_CHARS]}{SUMMARY_TRUNCATION_SUFFIX}"
            lines.append(f"  - Highlights: {snippet}")
        else:
            lines.append("  - Highlights: No changelog provided.")

    return "\n".join(lines).strip()


def _openrouter_summary(api_key, model, prompt, app_name, site_url, logger):
    if not api_key:
        return None

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    if site_url:
        headers["HTTP-Referer"] = site_url
    if app_name:
        headers["X-Title"] = app_name

    payload = {
        "model": model or "openrouter/auto",
        "messages": [
            {
                "role": "system",
                "content": "Summarize software release notifications for Telegram using Markdown (not MarkdownV2).",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
        "max_tokens": 800,
    }

    http = urllib3.PoolManager()
    try:
        response = http.request(
            "POST",
            OPENROUTER_API_URL,
            body=json.dumps(payload).encode("utf-8"),
            headers=headers,
            timeout=urllib3.Timeout(connect=5.0, read=60.0),
        )
    except Exception as exc:
        logger.error(f"OpenRouter request failed: {exc}")
        return None

    if response.status >= 400:
        logger.error(f"OpenRouter response error {response.status}: {response.data}")
        return None

    try:
        data = json.loads(response.data.decode("utf-8"))
    except json.JSONDecodeError:
        logger.error("OpenRouter response was not valid JSON")
        return None

    choices = data.get("choices", [])
    if not choices:
        logger.error("OpenRouter response missing choices")
        return None

    message = choices[0].get("message", {})
    return message.get("content")


def _record_release_notification(session, chat, repo_obj, release, release_body, release_url, release_tag, release_title):
    notification = ReleaseNotification(
        chat_id=chat.id,
        repo_id=repo_obj.id,
        release_id=getattr(release, "id", None),
        release_tag=release_tag,
        release_title=release_title,
        release_url=release_url,
        release_body=_normalize_release_body(release_body),
        repo_full_name=repo_obj.full_name,
        repo_link=repo_obj.link,
        pre_release=getattr(release, "prerelease", False),
        updated=getattr(release, "updated", False),
    )
    session.add(notification)
    session.commit()


@scheduler.task('cron', id='poll_github', hour='*')
def poll_github():
    with scheduler.app.app_context():
        for repo_obj in models.Repo.query.all():
            # TODO: Filter blocked repos from SQL query
            if repo_obj.blocked:
                continue

            try:
                scheduler.app.logger.info(f"Poll GitHub repo {repo_obj.full_name}")
                repo = github_obj.get_repo(repo_obj.id)
            except github.UnknownObjectException as e:
                message = f"GitHub repo {repo_obj.full_name} has been deleted"
                for chat in repo_obj.chats:
                    try:
                        asyncio.run(telegram_bot.send_message(chat_id=chat.id,
                                                              text=message,
                                                              disable_web_page_preview=True))
                    except telegram.error.Forbidden as e:
                        pass

                scheduler.app.logger.info(message)
                db.session.delete(repo_obj)
                db.session.commit()
                continue
            except github.GithubException as e:
                if e.status in (403, 451):
                    message = f"GitHub repo {repo_obj.full_name} has been blocked"
                    for chat in repo_obj.chats:
                        try:
                            asyncio.run(telegram_bot.send_message(chat_id=chat.id,
                                                                  text=message,
                                                                  disable_web_page_preview=True))
                        except telegram.error.Forbidden as e:
                            pass

                    scheduler.app.logger.info(message)
                    repo_obj.blocked = True
                    db.session.commit()
                else:
                    scheduler.app.logger.error(f"GithubException for {repo_obj.full_name} in poll_github: {e}")
                continue

            if repo.archived and not repo_obj.archived:
                message = f"GitHub repo <b>{repo_obj.full_name}</b> has been archived"
                for chat in repo_obj.chats:
                    try:
                        asyncio.run(telegram_bot.send_message(chat_id=chat.id,
                                                              text=message,
                                                              parse_mode=ParseMode.HTML,
                                                              link_preview_options=LinkPreviewOptions(
                                                                  url=repo_obj.link,
                                                                  prefer_small_media=True)
                                                              ))
                    except telegram.error.Forbidden as e:
                        pass

                scheduler.app.logger.info(message)
                repo_obj.archived = repo.archived
                db.session.commit()
            elif not repo.archived and repo_obj.archived:
                repo_obj.archived = repo.archived
                db.session.commit()

            release_or_tag, prerelease = store_latest_release(db.session, repo, repo_obj)
            if isinstance(release_or_tag, GitRelease):
                release = release_or_tag
                scheduler.app.logger.info(f"Process new release {release.title}")

                for chat in repo_obj.chats:
                    message, parse_mode, entities = format_release_message(chat.release_note_format, repo, release)

                    try:
                        asyncio.run(telegram_bot.send_message(chat_id=chat.id,
                                                              text=message,
                                                              parse_mode=parse_mode,
                                                              entities=entities,
                                                              link_preview_options=LinkPreviewOptions(
                                                                  url=repo_obj.link,
                                                                  prefer_small_media=True)
                                                              ))
                    except telegram.error.Forbidden as e:
                        scheduler.app.logger.info('Bot was blocked by the user')
                        db.session.delete(chat)
                        db.session.commit()
                    else:
                        _record_release_notification(
                            db.session,
                            chat,
                            repo_obj,
                            release,
                            release.body,
                            release.html_url,
                            release.tag_name,
                            release.title,
                        )
            elif isinstance(release_or_tag, Tag):
                tag = release_or_tag
                scheduler.app.logger.info(f"Process new tag {tag.name}")

                # TODO: Use tag.message as release_body text
                message = (f"<a href='{repo.html_url}'>{repo.full_name}</a>:\n"
                           f"<code>{tag.name}</code>")

                for chat in repo_obj.chats:
                    try:
                        asyncio.run(telegram_bot.send_message(chat_id=chat.id,
                                                              text=message,
                                                              parse_mode=ParseMode.HTML,
                                                              link_preview_options=LinkPreviewOptions(
                                                                  url=repo_obj.link,
                                                                  prefer_small_media=True)
                                                              ))
                    except telegram.error.Forbidden as e:
                        scheduler.app.logger.info('Bot was blocked by the user')
                        db.session.delete(chat)
                        db.session.commit()
                    else:
                        _record_release_notification(
                            db.session,
                            chat,
                            repo_obj,
                            tag,
                            None,
                            f"{repo.html_url}/releases/tag/{tag.name}",
                            tag.name,
                            tag.name,
                        )
            if isinstance(prerelease, GitRelease):
                release = prerelease
                scheduler.app.logger.info(f"Process new prerelease {release.title}")

                for chat in repo_obj.chats:
                    chat_repo = db.session.query(ChatRepo) \
                        .filter(ChatRepo.chat_id == chat.id).filter(ChatRepo.repo_id == repo_obj.id) \
                        .first()
                    if not chat_repo.process_pre_releases:
                        break

                    message, parse_mode, entities = format_release_message(chat.release_note_format, repo, release)

                    try:
                        asyncio.run(telegram_bot.send_message(chat_id=chat.id,
                                                              text=message,
                                                              parse_mode=parse_mode,
                                                              entities=entities,
                                                              link_preview_options=LinkPreviewOptions(
                                                                  url=repo_obj.link,
                                                                  prefer_small_media=True)
                                                              ))
                    except telegram.error.Forbidden as e:
                        scheduler.app.logger.info('Bot was blocked by the user')
                        db.session.delete(chat)
                        db.session.commit()
                    else:
                        _record_release_notification(
                            db.session,
                            chat,
                            repo_obj,
                            release,
                            release.body,
                            release.html_url,
                            release.tag_name,
                            release.title,
                        )


@scheduler.task('cron', id='poll_github_user', hour='*/8')
def poll_github_user():
    with scheduler.app.app_context():
        for chat in models.Chat.query.filter(models.Chat.github_username.is_not(None)).all():
            try:
                github_user = github_obj.get_user(chat.github_username)
            except github.GithubException as e:
                scheduler.app.logger.error(f"Can't found user '{chat.github_username}'")
                continue

            try:
                asyncio.run(telegram_bot.add_starred_repos(chat.id, github_user, telegram_bot))
            except telegram.error.Forbidden as e:
                scheduler.app.logger.info('Bot was blocked by the user')
                db.session.delete(chat)
                db.session.commit()

            for repo_obj in chat.repos:
                try:
                    repo = github_obj.get_repo(repo_obj.id)
                except github.GithubException as e:
                    if e.status in (451,):
                        message = f"GitHub repo {repo_obj.full_name} has been blocked"
                        scheduler.app.logger.info(message)
                    else:
                        raise e
                    continue

                starred = repo in github_user.get_starred()
                chat_repo = db.session.query(ChatRepo) \
                    .filter(ChatRepo.chat_id == chat.id).filter(ChatRepo.repo_id == repo_obj.id) \
                    .first()
                if chat_repo.starred != starred:
                    chat_repo.starred = starred
                    db.session.commit()


@scheduler.task('cron', id='clear_db', week='*')
def clear_db():
    with scheduler.app.app_context():
        for repo_obj in models.Repo.query.all():
            #  TODO: Use sqlalchemy_utils.auto_delete_orphans
            if repo_obj.is_orphan():
                scheduler.app.logger.info(f"Delete orphaned GitHub repo {repo_obj.full_name}")
                db.session.delete(repo_obj)
                db.session.commit()
                continue


def daily_release_summary():
    if not telegram_bot:
        return

    with scheduler.app.app_context():
        config = scheduler.app.config
        tz_name = config.get('DAILY_SUMMARY_TIMEZONE', 'UTC')
        now_utc = datetime.now(timezone.utc)
        day_start, day_end, day_label = _day_window_utc(now_utc, tz_name)

        api_key = config.get('OPENROUTER_API_KEY')
        model = config.get('OPENROUTER_MODEL')
        app_name = config.get('OPENROUTER_APP_NAME')
        site_url = config.get('OPENROUTER_SITE_URL') or config.get('SITE_URL')

        if not api_key:
            scheduler.app.logger.info('Daily summary skipped: OPENROUTER_API_KEY not set')
            return

        for chat in models.Chat.query.all():
            notifications = db.session.query(ReleaseNotification) \
                .filter(ReleaseNotification.chat_id == chat.id) \
                .filter(ReleaseNotification.summarized_at.is_(None)) \
                .filter(ReleaseNotification.sent_at >= day_start) \
                .filter(ReleaseNotification.sent_at < day_end) \
                .order_by(ReleaseNotification.sent_at.asc()) \
                .all()

            if not notifications:
                continue

            prompt = _build_summary_prompt(notifications, day_label, tz_name)
            summary = _openrouter_summary(api_key, model, prompt, app_name, site_url, scheduler.app.logger)
            if not summary:
                summary = _fallback_summary(notifications, day_label, tz_name)

            summary = _trim_message(summary)

            try:
                asyncio.run(telegram_bot.send_message(chat_id=chat.id,
                                                      text=summary,
                                                      parse_mode=ParseMode.MARKDOWN,
                                                      disable_web_page_preview=True))
            except telegram.error.BadRequest:
                asyncio.run(telegram_bot.send_message(chat_id=chat.id,
                                                      text=summary,
                                                      disable_web_page_preview=True))
            except telegram.error.Forbidden as e:
                scheduler.app.logger.info('Bot was blocked by the user')
                db.session.delete(chat)
                db.session.commit()
                continue

            summarized_at = datetime.now(timezone.utc)
            for note in notifications:
                note.summarized_at = summarized_at
            db.session.commit()


def _register_daily_summary_job():
    config = scheduler.app.config
    summary_time = config.get('DAILY_SUMMARY_TIME')
    if not summary_time:
        scheduler.app.logger.info('Daily summary disabled: DAILY_SUMMARY_TIME not set')
        return

    try:
        hour, minute = _parse_daily_summary_time(summary_time)
    except ValueError as exc:
        scheduler.app.logger.error(f"Daily summary disabled: {exc}")
        return

    tz_name = config.get('DAILY_SUMMARY_TIMEZONE', 'UTC')
    try:
        ZoneInfo(tz_name)
    except Exception:
        scheduler.app.logger.error(f"Invalid DAILY_SUMMARY_TIMEZONE '{tz_name}', using UTC")
        tz_name = 'UTC'

    scheduler.add_job(
        id='daily_release_summary',
        func=daily_release_summary,
        trigger='cron',
        hour=hour,
        minute=minute,
        timezone=tz_name,
        replace_existing=True,
    )


_register_daily_summary_job()
