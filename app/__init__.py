import asyncio

from flask import Flask
from flask_apscheduler import APScheduler
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from github import Github, Auth

from config import Config

db = SQLAlchemy()
migrate = Migrate()
scheduler = APScheduler()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.logger.setLevel(app.config['LOG_LEVEL'])

    db.init_app(app)
    migrate.init_app(app, db)

    scheduler.init_app(app)

    return app


app = create_app()

if app.config['GITHUB_TOKEN']:
    auth = Auth.Token(app.config['GITHUB_TOKEN'])
else:
    auth = None
github_obj = Github(auth=auth)

if app.config['TELEGRAM_BOT_TOKEN']:
    from app.telegram_bot import TelegramBot

    telegram_bot = TelegramBot(app)
    if not asyncio.run(telegram_bot.test_token()):
        app.logger.fatal('Telegram bot token is invalid or server not available')
        exit()
    telegram_bot.start()
else:
    telegram_bot = None
    app.logger.fatal('Telegram bot token not specified')

scheduler.start()


from app import database, models, routes, tasks  # noqa: E402
