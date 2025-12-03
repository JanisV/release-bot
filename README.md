[![Telegram Chat](https://img.shields.io/static/v1?label=Bot&message=release-bot&color=29a1d4&logo=telegram)](https://t.me/janisreleasebot)
[![Python 3.12](https://img.shields.io/badge/python-3.12-x.svg)](https://www.python.org/downloads/release/python-312/)
[![GitHub license](https://img.shields.io/github/license/JanisV/release-bot.svg)](https://github.com/JanisV/release-bot/blob/main/LICENSE)
[![Latest build](https://github.com/JanisV/release-bot/actions/workflows/docker.yml/badge.svg)](https://github.com/JanisV/release-bot/pkgs/container/release-bot)
[![Maintainability](https://api.codeclimate.com/v1/badges/b75abdb47ff5ec2cc5cf/maintainability)](https://codeclimate.com/github/JanisV/release-bot/maintainability)

# release-bot - a Telegram bot that notifies you of new GitHub releases

This is a Telegram bot that monitors the releases of given repos, sending messages upon a new release.

If you don't need a local installation you can use public bot, avalaible at https://t.me/janisreleasebot.

![Screenshot](https://github.com/user-attachments/assets/7587a21e-72c3-4462-9b19-d321f85c68dc)

## Alternatives

This bot is inspired by [new(releases)](https://newreleases.io/), [Github releases notify bot](https://github.com/pyatyispyatil/github-releases-notify-bot) and [release-bot](https://github.com/chofnar/release-bot).

Other similar tools:

- [Dockcheck](https://github.com/mag37/dockcheck) - CLI tool to automate docker image updates;
- [Renovate](https://docs.renovatebot.com/) - Automated dependency updates

## Features

- Easy subscription to repo by owner/name, GitHub/PyPI/npm URL or uploading requirements.txt or package.json file
- Rich markdown formatting for release note
- Auto subscription to starred repos
- Ready for self-hosting, has docker image
- Work locally, without white IP and domain name
- Only Telegram token required

## Commands

`/start` - show welcome message  
`/about` - information about this bot  
`/help` - brief usage info  
`/list` - show your subscriptions  
`/editlist` - show and edit your subscriptions  
`/starred username` - subscribe to user's starred repos  
`/starred` - unsubscribe from user's starred repos  
`/settings` - change output format  
`/stats` - basic server statistics  
`/test URL` - show specified release message

## Stack

- Python 3.12
- Flask
- telegramify_markdown
- python-telegram-bot
- PyGithub
- APScheduler via Flask-APScheduler
- SQLAlchemy via Flask-SQLAlchemy
- Alembic via Flask-Migrate - SQLAlchemy database migrations

## Running it yourself

### With docker

Using docker compose:

```yaml
services:
  release-bot:
    container_name: release-bot
    image: ghcr.io/janisv/release-bot:latest
    restart: unless-stopped
    environment:
      - TELEGRAM_BOT_TOKEN=<telegram_token>
      #- GITHUB_TOKEN=<github_token> # optional
      #- SITE_URL=https://<your_domain_name> # optional
    ports:
      - 5000:5000
    volumes:
      - /path/to/data:/app/data
```

or docker run:

`docker run -p 5000:5000 -e TELEGRAM_BOT_TOKEN="<telegram_token>" -v /path/to/data:/app/data -d --name release-bot ghcr.io/janisv/release-bot:latest`

### From source

Look at Development section

### Set the necessary env vars

`TELEGRAM_BOT_TOKEN` - get this from [BotFather](https://t.me/botfather). You'll need to create a bot.

`GITHUB_TOKEN` - (optional) GitHub personal access token (classic) or fine-grained personal access token. When not specified working well for about 20 repos. More info at [Rate limits for the REST API](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api?apiVersion=2022-11-28).

`SITE_URL` - (optional) URL used for listening for incoming requests from the Telegram servers. When not specified uses polling instead webhooks. More info at [Marvin's Marvellous Guide to All Things Webhook](https://core.telegram.org/bots/webhooks).

`CHAT_ID` - (optional) Only messages from the specified chat ID are accepted. Can be a comma separated list. You can get your chat ID with [@getmyid_bot](https://t.me/getmyid_bot). If not specified, all messages are accepted.

`DATABASE_URI` - (optional) When not specified local SQLite uses.

`MAX_REPOS_PER_CHAT` - (optional) Limit number of repos per user. Default 0 - unlimited.

`LOG_LEVEL` - (optional) Default INFO.

## Development

Setup env vars and run:

```shell
pip3 install -r requirements.txt
flask db upgrade
python3 -m flask run -h 0.0.0.0
```

For use webhooks locally, you may want to use [localhost.run](https://localhost.run/).
