from http import HTTPStatus

from flask import Response, request

from app import telegram_bot, app
from app.models import Chat, Repo, Release
from app._version import __version__


@app.route('/')
async def index():
    bot_me = await telegram_bot.get_me()
    return (f'<a href="https://t.me/{bot_me.username}">{bot_me.first_name}</a> - a telegram bot for GitHub releases v{__version__}.'
            '<br><br>'
            'Source code available at <a href="https://github.com/JanisV/release-bot">JanisV/release-bot</a>')


@app.route('/stats')
async def stats():
    users = Chat.query.count()
    repos = Repo.query.count()
    releases = Release.query.count()

    statistics = {
        "users": users,
        "repos": repos,
        "releases": releases,
    }
    return statistics


@app.post("/telegram")
async def telegram() -> Response:
    if app.config['SITE_URL']:
        await telegram_bot.webhook(request.json)
        return Response(status=HTTPStatus.OK)
    else:
        return Response(status=HTTPStatus.NOT_IMPLEMENTED)
