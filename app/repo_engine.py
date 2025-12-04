import re
from datetime import datetime, timezone, timedelta

import github
from sulguk import transform_html
from telegram import MessageEntity
from telegram.constants import MessageLimit
from telegramify_markdown import markdownify

from app import app, github_obj
from app.github_emoji import github_emoji_map
from app.models import Release, Repo

SKIPPED_POSTFIX = "\n-=SKIPPED=-"

github_extra_html_tags_pattern = re.compile("<p align=\".*?\".*?>|</p>|<a name=\".*?\">|<picture>.*?</picture>|"
                                            "</?h[1-4]>|</?sub>|</?sup>|</?details>|</?summary>|</?dl>|</?dt>|"
                                            "</?dd>|</?em>|</?small>|<br>|<!--.*?-->|<p/>",
                                            flags=re.DOTALL)
github_img_html_tag_pattern = re.compile("<img .*?src=\"(.*?)\".*?>")
github_b_html_tag_pattern = re.compile("<b>(.*?)</b>", flags=re.DOTALL)
github_i_html_tag_pattern = re.compile("<i>(.*?)</i>", flags=re.DOTALL)
github_code_html_tag_pattern = re.compile("<code>(.*?)</code>", flags=re.DOTALL)
github_a_html_tag_pattern = re.compile("<a href=\"(.*?)\".*?>(.*?)</a>", flags=re.DOTALL)
github_emoji_pattern = re.compile(r':[a-z0-9_-]+:')


def format_header(release_note_format, repo, release):
    current_tag = release.tag_name
    if (release.title == current_tag or
            release.title == f"v{current_tag}" or
            f"v{release.title}" == current_tag):
        # Skip release title when it is equal to tag
        release_title = ""
    else:
        release_title = release.title

    if release_note_format in ("quote", "pre"):
        release_header = (
            f"<b>{repo.full_name}</b>\n"
            f"{f"<code>{release_title}</code>" if release_title else ""}"
            f" <a href='{release.html_url}'>{current_tag}</a>"
            f"{" <i>pre-release</i>" if release.prerelease else ""}"
            f"{" <i>updated</i>" if release.updated else ""}\n"
        )
    elif release_note_format == "html":
        release_header = (
            f"**{repo.full_name}**<br>"  # GitHub don't process '\n' instead <br> here
            f"{f"`{release_title}`" if release_title else ""}"
            f" [{current_tag}]({release.html_url})"
            f"{" _pre-release_" if release.prerelease else ""}"
            f"{" _updated_" if release.updated else ""}\n\n"
        )
    else:
        release_header = (
            f"**{repo.full_name}**\n"
            f"{f"`{release_title}`" if release_title else ""}"
            f" [{current_tag}]({release.html_url})"
            f"{" _pre-release_" if release.prerelease else ""}"
            f"{" _updated_" if release.updated else ""}\n\n"
        )

    return release_header


def htmlify_release_body(release_note_format, repo, release):
    header = format_header(release_note_format, repo, release)
    release_body = f"{header}{release.body}"

    rendered_release_body = github_obj.render_markdown(release_body)
    print(rendered_release_body.encode('ascii', errors='replace').decode('ascii'))
    result = transform_html(rendered_release_body)
    print(result.text.encode('ascii', errors='replace').decode('ascii'))
    print(result.entities)

    message_len = len(result.text)
    if message_len > MessageLimit.MAX_TEXT_LENGTH:
        message_len = MessageLimit.MAX_TEXT_LENGTH - len(SKIPPED_POSTFIX)
        result.text = f"{result.text[:message_len]}{SKIPPED_POSTFIX}"

    entities = []
    for entity in result.entities:
        if entity['offset'] >= message_len:
            continue
        if entity['offset'] + entity['length'] >= message_len:
            entity['length'] = message_len - entity['offset']
        url = None
        if 'url' in entity:
            url = entity['url']
            if url.startswith('#'):
                continue
        message_entity = MessageEntity(entity['type'], entity['offset'], entity['length'],
                                       url=url)
        entities.append(message_entity)

    return result.text, entities


def codeify_release_message(release_note_format, repo, release):
    release_body = release.body
    release_body = github_extra_html_tags_pattern.sub(
        "",
        release_body
    )
    release_body = github_img_html_tag_pattern.sub(
        "🖼️\\1",
        release_body
    )
    if len(release_body) > MessageLimit.MAX_TEXT_LENGTH - 256:
        release_body = f"{release_body[:MessageLimit.MAX_TEXT_LENGTH - 256]}{SKIPPED_POSTFIX}"

    header = format_header(release_note_format, repo, release)
    if release_note_format == "quote":
        message = f"{header}<blockquote>{release_body}</blockquote>"
    else:  # release_note_format == "pre":
        message = f"{header}<pre>{release_body}</pre>"

    return message


def markdownify_release_message(release_note_format, repo, release):
    release_body = release.body
    release_body = github_extra_html_tags_pattern.sub(
        "",
        release_body
    )
    release_body = github_img_html_tag_pattern.sub(
        "🖼️\\1",
        release_body
    )
    if len(release_body) > MessageLimit.MAX_TEXT_LENGTH - 256:
        release_body = f"{release_body[:MessageLimit.MAX_TEXT_LENGTH - 256]}{SKIPPED_POSTFIX}"

    release_body = github_b_html_tag_pattern.sub(
        "**\\1**", release_body
    )
    release_body = github_i_html_tag_pattern.sub(
        "_\\1_", release_body
    )
    release_body = github_code_html_tag_pattern.sub(
        "`\\1`", release_body
    )
    release_body = github_a_html_tag_pattern.sub(
        "[\\2](\\1)", release_body
    )
    release_body = release_body.replace("<hr>", "---")
    release_body = release_body.replace("[!NOTE]", "**ⓘ Note**")
    release_body = release_body.replace("[!TIP]", "**💡 Tip**")
    release_body = release_body.replace("[!IMPORTANT]", "**❗ Important**")
    release_body = release_body.replace("[!WARNING]", "**⚠️ Warning**")
    release_body = release_body.replace("[!CAUTION]", "**🛑 Caution**")
    if github_emoji_pattern.search(release_body):
        for key, value in github_emoji_map.items():
            release_body = release_body.replace(f":{key}:", value)

    header = format_header(release_note_format, repo, release)
    release_body = f"{header}{release_body}"
    message = markdownify(release_body)
    while len(message) >= MessageLimit.MAX_TEXT_LENGTH:
        release_body = f"{release_body[:-100]}{SKIPPED_POSTFIX}"
        message = markdownify(release_body)

    return message


def format_release_message(release_note_format, repo, release):
    if release_note_format in ("quote", "pre"):
        message = codeify_release_message(release_note_format, repo, release)
        entities = None
    elif release_note_format == "html":
        message, entities = htmlify_release_body(release_note_format, repo, release)
    else:
        message = markdownify_release_message(release_note_format, repo, release)
        entities = None

    return message, entities


def store_latest_release(session, repo, repo_obj):
    release = None
    prerelease = None
    tag = None

    if app.config['PROCESS_PRE_RELEASES']:
        if repo.get_releases().totalCount > 0:
            prerelease = repo.get_releases()[0]
            if not prerelease.prerelease or prerelease.draft:
                prerelease = None
            if prerelease and datetime.now(timezone.utc) - timedelta(minutes=15) < prerelease.published_at:
                prerelease = None

    try:
        release = repo.get_latest_release()
        if release.draft:
            release = None
    except github.GithubException as e:
        # Repo has no releases yet
        if repo.get_tags().totalCount > 0:
            tag = repo.get_tags()[0]

    if release or prerelease:
        if release:
            release.updated = False
            release_obj = session.query(Release).join(Repo) \
                .filter(Repo.id == repo_obj.id).filter(Release.release_id == release.id) \
                .first()
            if release_obj:
                stored_release_date = release_obj.release_date.replace(tzinfo=timezone.utc)
                if release.last_modified_datetime > stored_release_date:
                    release_obj.release_date = release.last_modified_datetime
                    release_obj.pre_release = release.prerelease
                    session.commit()

                    release.updated = True
                else:
                    release = None
            else:
                release_obj = Release(
                    release_id=release.id,
                    tag_name=release.tag_name,
                    release_date=release.last_modified_datetime,
                    link=release.html_url,
                    pre_release=release.prerelease,
                )
                repo_obj.releases.append(release_obj)
                session.commit()

        if prerelease:
            prerelease.updated = False
            release_obj = session.query(Release).join(Repo) \
                .filter(Repo.id == repo_obj.id).filter(Release.release_id == prerelease.id) \
                .first()
            if not release_obj:
                release_obj = Release(
                    release_id=prerelease.id,
                    tag_name=prerelease.tag_name,
                    release_date=prerelease.published_at,
                    link=prerelease.html_url,
                    pre_release=prerelease.prerelease,
                )
                repo_obj.releases.append(release_obj)
                session.commit()
            else:
                prerelease = None

        return release, prerelease
    elif tag:
        release_obj = session.query(Release).join(Repo) \
            .filter(Repo.id == repo_obj.id).filter(Release.tag_name == tag.name) \
            .first()
        if not release_obj:
            release_obj = Release(
                tag_name=tag.name,
                release_date=tag.last_modified_datetime,
            )
            repo_obj.releases.append(release_obj)
            session.commit()
            return tag, None

    return None, None
