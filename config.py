import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
    SITE_URL = os.environ.get('SITE_URL')
    DAILY_SUMMARY_TIME = os.environ.get('DAILY_SUMMARY_TIME', '21:00')
    DAILY_SUMMARY_TIMEZONE = os.environ.get('DAILY_SUMMARY_TIMEZONE', 'Europe/Rome')
    OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
    OPENROUTER_MODEL = os.environ.get('OPENROUTER_MODEL', 'openrouter/auto')
    OPENROUTER_APP_NAME = os.environ.get('OPENROUTER_APP_NAME', 'release-bot')
    OPENROUTER_SITE_URL = os.environ.get('OPENROUTER_SITE_URL')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', f'sqlite:///{basedir}/data/db.sqlite')
    SQLALCHEMY_ECHO = os.environ.get('SQL_DEBUG', '').lower() in ('true', '1', 't')
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
    MAX_REPOS_PER_CHAT = int(os.environ.get('MAX_REPOS_PER_CHAT', 0))
    PROCESS_PRE_RELEASES = bool(GITHUB_TOKEN)
    CHAT_ID = []
    if 'CHAT_ID' in os.environ:
        for chat_id in os.environ.get('CHAT_ID').split(','):
            CHAT_ID.append(int(chat_id))
