import asyncio

import github
import telegram
from github.GitRelease import GitRelease
from github.Tag import Tag
from telegram import LinkPreviewOptions
from telegram._utils.defaultvalue import DEFAULT_NONE
from telegram.constants import ParseMode

from app import models
from app import github_obj, db, telegram_bot, scheduler
from app.models import ChatRepo
from app.repo_engine import store_latest_release, format_release_message, htmlify_release_body


@scheduler.task('cron', id='poll_github', hour='*/3')
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

                for chat in repo_obj.chats:
                    message, entities = format_release_message(chat.release_note_format, repo, release)

                    if chat.release_note_format in ("quote", "pre"):
                        parse_mode = ParseMode.HTML
                    elif chat.release_note_format == "html":
                        parse_mode = DEFAULT_NONE
                    else:
                        parse_mode = ParseMode.MARKDOWN_V2

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
            elif isinstance(release_or_tag, Tag):
                tag = release_or_tag

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
            if isinstance(prerelease, GitRelease):
                release = prerelease

                for chat in repo_obj.chats:
                    chat_repo = db.session.query(ChatRepo) \
                        .filter(ChatRepo.chat_id == chat.id).filter(ChatRepo.repo_id == repo_obj.id) \
                        .first()
                    if not chat_repo.process_pre_releases:
                        break

                    message = format_release_message(chat, repo, release)

                    if chat.release_note_format in ("quote", "pre"):
                        parse_mode = ParseMode.HTML
                    else:
                        parse_mode = ParseMode.MARKDOWN_V2

                    try:
                        asyncio.run(telegram_bot.send_message(chat_id=chat.id,
                                                              text=message,
                                                              parse_mode=parse_mode,
                                                              link_preview_options=LinkPreviewOptions(
                                                                  url=repo_obj.link,
                                                                  prefer_small_media=True)
                                                              ))
                    except telegram.error.Forbidden as e:
                        scheduler.app.logger.info('Bot was blocked by the user')
                        db.session.delete(chat)
                        db.session.commit()


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
