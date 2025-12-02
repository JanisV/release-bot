import difflib
import os

from github import Auth, Github
from urllib.parse import urlparse

from app.repo_engine import format_release_message


class ChatMock:
    def __init__(self):
        self.release_note_format = None


class RepoMock:
    def __init__(self, full_name):
        self.full_name = full_name


class ReleaseMock:
    def __init__(self, body, tag_name):
        self.body = body
        self.tag_name = tag_name
        self.title = tag_name
        self.html_url = ''
        self.prerelease = False
        self.updated = False


def split_release_url(url):
    path_parts = urlparse(url).path.strip('/').split('/')
    if len(path_parts) >= 3 and path_parts[2] == 'releases':
        # full_name = f"{path_parts[0]}/{path_parts[1]}"
        owner = path_parts[0]
        repo = path_parts[1]
    else:
        return None

    if len(path_parts) >= 5 and path_parts[2] == 'releases' and path_parts[3] == 'tag':
        tag_name = path_parts[4]
    else:
        return None

    return owner, repo, tag_name


def get_release(github_obj, url):
    owner, repo_name, tag_name = split_release_url(url)
    full_name = f"{owner}/{repo_name}"

    repo = github_obj.get_repo(full_name)

    release = repo.get_release(tag_name)
    with open(f"{owner}__{repo_name}__{tag_name}.md", 'w', encoding='utf-8', newline='') as file:
        file.write(release.body.replace('\r', ''))
        return release.body.replace('\r', '')

    return None


def format_message(url, release_body=None):
    owner, repo_name, tag_name = split_release_url(url)
    full_name = f"{owner}/{repo_name}"

    if release_body is None:
        src_file = f"{owner}__{repo_name}__{tag_name}.md"
        with open(src_file, 'r', encoding='utf-8') as file:
            release_body = file.read()

    chat = ChatMock()
    repo = RepoMock(full_name)
    release = ReleaseMock(release_body, tag_name)

    message = format_release_message(chat, repo, release)

    with open(f"{owner}__{repo_name}__{tag_name}.tg", 'w', encoding='utf-8', newline='') as file:
        file.write(message.replace('\r', ''))
    return message


release_urls = (
    "https://github.com/PyGithub/PyGithub/releases/tag/v2.8.1",
    "https://github.com/Rongronggg9/RSS-to-Telegram-Bot/releases/tag/v2.10.0",
    "https://github.com/SiliconLabs/gecko_sdk/releases/tag/v4.4.5",
    "https://github.com/WinMerge/winmerge/releases/tag/v2.16.50",
    "https://github.com/fail2ban/fail2ban/releases/tag/1.1.0",
    "https://github.com/healthchecks/healthchecks/releases/tag/v3.13",
    "https://github.com/immich-app/immich/releases/tag/v1.118.0",
    "https://github.com/immich-app/immich/releases/tag/v1.135.2",
    "https://github.com/immich-app/immich/releases/tag/v1.136.0",
    "https://github.com/jeffvli/feishin/releases/tag/v0.22.0",
    "https://github.com/karakeep-app/karakeep/releases/tag/v0.18.0",
    "https://github.com/karakeep-app/karakeep/releases/tag/v0.29.0",
    "https://github.com/linuxserver/docker-cops/releases/tag/3.8.2-ls279",
    "https://github.com/linuxserver/docker-jackett/releases/tag/v0.22.772-ls557",
    "https://github.com/linuxserver/docker-mastodon/releases/tag/v4.3.0-ls108",
    "https://github.com/linuxserver/docker-mastodon/releases/tag/v4.5.2-ls171",
    "https://github.com/linuxserver/docker-sabnzbd/releases/tag/4.5.5-ls238",
    "https://github.com/louislam/dockge/releases/tag/1.5.0",
    "https://github.com/miguelgrinberg/Flask-Migrate/releases/tag/v4.1.0",
    "https://github.com/nextcloud/all-in-one/releases/tag/v12.1.4",
    "https://github.com/numpy/numpy/releases/tag/v2.3.2",
    "https://github.com/python-telegram-bot/python-telegram-bot/releases/tag/v22.3",
    "https://github.com/stashapp/stash/releases/tag/v0.29.3",
    "https://github.com/swingmx/swingmusic/releases/tag/v2.1.0",
    "https://github.com/urllib3/urllib3/releases/tag/2.5.0",
)


github_token = os.environ.get('GITHUB_TOKEN')

if github_token:
    auth = Auth.Token(github_token)
else:
    auth = None
github_obj = Github(auth=auth)

for release_url in release_urls:
    release_body = get_release(github_obj, release_url)
    # release_body = None
    message = format_message(release_url, release_body)

for release_url in release_urls:
    owner, repo_name, tag_name = split_release_url(release_url)
    full_name = f"{owner}/{repo_name}"

    src_file = f"{owner}__{repo_name}__{tag_name}.tg"
    with open(src_file, 'r', encoding='utf-8') as file:
        formatted_release_body = file.read()

    src_file = f"{owner}__{repo_name}__{tag_name}.md"
    with open(src_file, 'r', encoding='utf-8') as file:
        github_release_body = file.read()

    chat = ChatMock()
    repo = RepoMock(full_name)
    release = ReleaseMock(github_release_body, tag_name)

    message = format_release_message(chat, repo, release)

    diffs = difflib.unified_diff(formatted_release_body.splitlines(), message.splitlines(),
                                 fromfile=f"{owner}__{repo_name}__{tag_name}.tg", tofile=release_url)
    for line in diffs:
        print(line)
