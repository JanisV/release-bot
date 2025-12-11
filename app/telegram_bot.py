import asyncio
import json
import logging
import re
import threading
import urllib.parse

import github
import requirements
import telegram
import urllib3
from sqlalchemy import true
from telegram import Chat as TelegramChat
from telegram import Update, LinkPreviewOptions, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import InlineKeyboardMarkupLimit, ParseMode
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from app import github_obj, db
from app._version import __version__
from app.models import Chat, Repo, ChatRepo, Release
from app.repo_engine import store_latest_release, format_release_message, htmlify_release_body

MAX_UPLOADED_FILE_SIZE = 1024 * 10  # 10kB

direct_pattern = re.compile(".+/.+")
github_link_pattern = re.compile("https://github.com/([^/]+/[^/]+)/?")
pypi_link_pattern = re.compile("https://pypi.org/project/(.+)/")
npm_link_pattern = re.compile("https://www.npmjs.com/package/(.+)")


def get_or_create_chat(session, chat_id):
    chat = session.get(Chat, chat_id)
    if not chat:
        chat = Chat(
            id=chat_id,
        )
        session.add(chat)
        session.commit()

    return chat


def get_latest_chat_release(session, chat, repo):
    if repo.releases:
        chat_repo = session.query(ChatRepo) \
            .filter(ChatRepo.chat_id == chat.id).filter(ChatRepo.repo_id == repo.id) \
            .first()

        if chat_repo.process_pre_releases:
            return repo.releases[-1]
        else:
            return session.query(Release) \
                .filter(Release.repo_id == repo.id) \
                .filter(Release.pre_release != true()) \
                .order_by(Release.id.desc()) \
                .first()
    else:
        return None


class TelegramBot(object):

    def __init__(self, app=None):
        self.application = None
        self.app = None

        if app:
            self.init_app(app)

    def init_app(self, app):
        logging.getLogger().setLevel(app.config['LOG_LEVEL'])

        self.app = app

        self.application = Application.builder().token(self.app.config['TELEGRAM_BOT_TOKEN']).build()

        self.application.add_handler(CommandHandler("about", self.about_command))
        self.application.add_handler(CommandHandler("delete", self.delete_command))
        self.application.add_handler(CommandHandler("editlist", self.edit_list_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("list", self.list_command))
        self.application.add_handler(CommandHandler("prerelease", self.prerelease_command))
        self.application.add_handler(CommandHandler("settings", self.settings_command))
        self.application.add_handler(CommandHandler("starred", self.starred_command))
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("stats", self.stats_command))
        self.application.add_handler(CommandHandler("test", self.test_command))
        self.application.add_handler(MessageHandler(filters.COMMAND, self.unknown_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.message))
        self.application.add_handler(MessageHandler(filters.Document.ALL, self.download_file))
        self.application.add_handler(CallbackQueryHandler(self.button))

    def _get_chat_id(self, update: Update):
        chat_id = update.effective_chat.id
        if not self.app.config['CHAT_ID']:
            return chat_id
        else:
            if chat_id in self.app.config['CHAT_ID']:
                return chat_id
        return None

    def _is_group(self, update: Update):
        if update.effective_chat.type in [TelegramChat.GROUP, TelegramChat.SUPERGROUP]:
            return True
        return False

    async def set_commands(self, application):
        await application.bot.set_my_commands([('list', "show your subscriptions"),
                                               ('editlist', "show and edit your subscriptions"),
                                               ('prerelease', "unsubscribe from repo pre-releases"),
                                               ('delete', "unsubscribe from repo releases"),
                                               ('starred', "subscribe to user's starred repos"),
                                               ('settings', "change output format"),
                                               ('about', "information about this bot"),
                                               ('help', "brief usage info")])

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /start is issued."""
        if self._get_chat_id(update):
            await update.message.reply_text(
                "Send a message containing repo for subscribing in one of the following formats: "
                "owner/repo, https://github.com/owner/repo"
            )

    async def about_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /about is issued."""
        if self._get_chat_id(update):
            await update.message.reply_text(
                f"release-bot - a telegram bot for GitHub releases v{__version__}\n"
                "Source code available at https://github.com/JanisV/release-bot"
            )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /help is issued."""
        if self._get_chat_id(update):
            await update.message.reply_text(
                "For subscribe to a new GitHub releases send a message containing owner and name of repo (owner/repo), "
                "GitHub/PyPI/npm URL or upload requirements.txt or package.json file.\n\n"
                "Available commands:\n"
                "/start - show welcome message\n"
                "/about - information about this bot\n"
                "/help - brief usage info\n"
                "/list - show your subscriptions\n"
                "/editlist - show and edit your subscriptions\n"
                "/delete - (in reply to release note message) unsubscribe from repo\n"
                "/delete owner/repo - unsubscribe from specified repo\n"
                "/prerelease - (in reply to release note message) unsubscribe from pre-releases of specified repo\n"
                "/prerelease owner/repo - unsubscribe from pre-releases of specified repo\n"
                "/starred username - subscribe to user's starred repos\n"
                "/starred - unsubscribe from user's starred repos\n"
                "/settings - change output format\n"
                "/stats - basic server statistics"
            )

    async def list_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /list is issued."""
        if chat_id := self._get_chat_id(update):
            with self.app.app_context():
                text = "Your subscriptions:\n"
                chat = get_or_create_chat(db.session, chat_id)
                for i, repo in enumerate(chat.repos):
                    repo_emoji = ''
                    if repo.archived:
                        repo_emoji += ' 📦'
                    if repo.blocked:
                        repo_emoji += ' 🚫'
                    text += f"{i + 1}. <b><a href='{repo.link}'>{repo.full_name}</a></b>{repo_emoji}\n"

            await update.message.reply_html(
                text,
                link_preview_options=LinkPreviewOptions(is_disabled=True),
            )

    async def prerelease_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Process the command /prerelease."""
        if self._get_chat_id(update):
            if chat_id := self._get_chat_id(update):
                with self.app.app_context():
                    if update.message.reply_to_message:
                        repo_name = update.message.reply_to_message.text.split('\n', 1)[0]
                    else:
                        if not context.args or len(context.args) != 1 or not direct_pattern.search(context.args[0]):
                            await update.message.reply_text(
                                "Specify a GitHub repo in the following format: /delete owner/repo")
                            return

                        repo_name = context.args[0]

                    chat = get_or_create_chat(db.session, chat_id)
                    repo_obj = db.session.query(Repo) \
                        .filter(Repo.full_name == repo_name) \
                        .first()
                    if repo_obj and repo_obj in chat.repos:
                        chat_repo = db.session.query(ChatRepo) \
                            .filter(ChatRepo.chat_id == chat.id).filter(ChatRepo.repo_id == repo_obj.id) \
                            .first()
                        chat_repo.process_pre_releases = not chat_repo.process_pre_releases
                        db.session.commit()

                        if chat_repo.process_pre_releases:
                            reply_message = f"You are subscribed to repo <b>{repo_obj.full_name}</b> pre-releases."
                        else:
                            reply_message = f"You are unsubscribed from repo <b>{repo_obj.full_name}</b> pre-releases."
                        repo_url = repo_obj.link
                        await update.message.get_bot().send_message(chat_id, reply_message,
                                                                    parse_mode=ParseMode.HTML,
                                                                    link_preview_options=LinkPreviewOptions(
                                                                        url=repo_url,
                                                                        prefer_small_media=True)
                                                                    )
                    else:
                        await update.message.reply_text(
                            "Error: Repo not founded."
                        )

    async def delete_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Process the command /delete."""
        if self._get_chat_id(update):
            if chat_id := self._get_chat_id(update):
                with self.app.app_context():
                    if update.message.reply_to_message:
                        repo_name = update.message.reply_to_message.text.split('\n', 1)[0]
                    else:
                        if not context.args or len(context.args) != 1 or not direct_pattern.search(context.args[0]):
                            await update.message.reply_text(
                                "Specify a GitHub repo in the following format: /delete owner/repo")
                            return

                        repo_name = context.args[0]

                    chat = get_or_create_chat(db.session, chat_id)
                    repo_obj = db.session.query(Repo) \
                        .filter(Repo.full_name == repo_name) \
                        .first()
                    if repo_obj and repo_obj in chat.repos:
                        chat.repos.remove(repo_obj)
                        db.session.commit()

                        reply_message = f"Deleted repo: <b>{repo_obj.full_name}</b>"
                        repo_url = repo_obj.link
                        await update.message.get_bot().send_message(chat_id, reply_message,
                                                                    parse_mode=ParseMode.HTML,
                                                                    link_preview_options=LinkPreviewOptions(
                                                                        url=repo_url,
                                                                        prefer_small_media=True)
                                                                    )
                    else:
                        await update.message.reply_text(
                            "Error: Repo not founded."
                        )

    def get_repo_keyboard(self, chat_id, curr_page):
        btn_per_line = 4
        lines = (InlineKeyboardMarkupLimit.TOTAL_BUTTON_NUMBER - 3) // btn_per_line

        keyboard = []
        with self.app.app_context():
            chat = get_or_create_chat(db.session, chat_id)
            if len(chat.repos) == 0:
                return None

            for repo in chat.repos[curr_page * lines:(curr_page + 1) * lines]:
                repo_name = repo.full_name.split('/')[1]
                latest_release = get_latest_chat_release(db.session, chat, repo)
                if latest_release:
                    repo_current_tag = latest_release.tag_name
                    if latest_release.link:
                        repo_current_tag_url = latest_release.link
                    else:
                        repo_current_tag_url = f"{repo.link}/releases/tag/{repo_current_tag}"
                else:
                    repo_current_tag = "N/A"
                    repo_current_tag_url = f"{repo.link}/releases"
                chat_repo = db.session.query(ChatRepo) \
                    .filter(ChatRepo.chat_id == chat.id).filter(ChatRepo.repo_id == repo.id) \
                    .first()
                process_pre_releases = "✔️" if chat_repo.process_pre_releases else "❌"
                keyboard.append([InlineKeyboardButton(repo_name, url=repo.link),
                                 InlineKeyboardButton(repo_current_tag, url=repo_current_tag_url),
                                 InlineKeyboardButton(f"Pre: {process_pre_releases}️️",
                                                      callback_data=f"pre-{curr_page}-{repo.id}"),
                                 InlineKeyboardButton("🗑️",
                                                      callback_data=f"delete-{curr_page}-{repo.id}")])

            if not keyboard:
                return keyboard

            assert btn_per_line == len(keyboard[0])

            if len(chat.repos) > (curr_page + 1) * lines:
                if curr_page > 0:
                    keyboard.append([InlineKeyboardButton("⬅️ Prev", callback_data=f"prev-{curr_page - 1}"),
                                     InlineKeyboardButton("Cancel", callback_data="cancel"),
                                     InlineKeyboardButton("Next ➡️", callback_data=f"next-{curr_page + 1}")])
                else:
                    keyboard.append([InlineKeyboardButton("Cancel", callback_data="cancel"),
                                     InlineKeyboardButton("Next ➡️", callback_data=f"next-{curr_page + 1}")])
            else:
                if curr_page > 0:
                    keyboard.append([InlineKeyboardButton("⬅️ Prev", callback_data=f"prev-{curr_page - 1}"),
                                     InlineKeyboardButton("Cancel", callback_data="cancel")])
                else:
                    keyboard.append([InlineKeyboardButton("Cancel", callback_data="cancel")])
            keyboard_markup = InlineKeyboardMarkup(keyboard)
            return keyboard_markup

    async def edit_list_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /editlist is issued."""
        if chat_id := self._get_chat_id(update):
            keyboard = self.get_repo_keyboard(chat_id, 0)
            if keyboard:
                await update.message.reply_text("Here's all your added repos with their releases:",
                                                reply_markup=keyboard)
            else:
                await update.message.reply_text("You are haven't repos yet.")

    async def add_repo(self, chat_id, repo, bot, silent=False) -> None:
        with self.app.app_context():
            chat = get_or_create_chat(db.session, chat_id)

            if self.app.config['MAX_REPOS_PER_CHAT']:
                if len(chat.repos) >= self.app.config['MAX_REPOS_PER_CHAT']:  # TODO: Use SQL COUNT instead Python len
                    if not silent:
                        await bot.send_message(
                            chat_id=chat.id,
                            text=f"Maximum number of repos per user reached.",
                        )
                    return

            repo_obj = db.session.get(Repo, repo.id)
            if not repo_obj:
                repo_obj = Repo(
                    id=repo.id,
                    full_name=repo.full_name,
                    description=repo.description,
                    link=repo.html_url,
                    archived=repo.archived,
                )

                store_latest_release(db.session, repo, repo_obj)

                db.session.add(repo_obj)
                db.session.commit()

            if chat in repo_obj.chats:
                if not silent:
                    await bot.send_message(
                        chat_id=chat.id,
                        text=f"GitHub repo <b>{repo.full_name}</b> has already been added.",
                        parse_mode=ParseMode.HTML,
                        link_preview_options=LinkPreviewOptions(
                            url=repo.html_url,
                            prefer_small_media=True)
                    )
            else:
                repo_obj.chats.append(chat)
                db.session.commit()

                if repo_obj.archived:
                    await bot.send_message(
                        chat_id=chat.id,
                        text=f"Added GitHub repo: <b>{repo.full_name}</b>, "
                             f"but it is archived",
                        parse_mode=ParseMode.HTML,
                        link_preview_options=LinkPreviewOptions(
                            url=repo.html_url,
                            prefer_small_media=True)
                    )
                elif repo_obj.get_latest_release():
                    await bot.send_message(
                        chat_id=chat.id,
                        text=f"Added GitHub repo: <b>{repo.full_name}</b>",
                        parse_mode=ParseMode.HTML,
                        link_preview_options=LinkPreviewOptions(
                            url=repo.html_url,
                            prefer_small_media=True)
                    )
                else:
                    await bot.send_message(
                        chat_id=chat.id,
                        text=f"Added GitHub repo: <b>{repo.full_name}</b>, "
                             f"but it has not releases",
                        parse_mode=ParseMode.HTML,
                        link_preview_options=LinkPreviewOptions(
                            url=repo.html_url,
                            prefer_small_media=True)
                    )

    async def add_starred_repos(self, chat_id, github_user, bot) -> None:
        repos = github_user.get_starred()
        for repo in repos:
            await self.add_repo(chat_id, repo, bot, True)

    async def button(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if chat_id := self._get_chat_id(update):
            query = update.callback_query

            # CallbackQueries need to be answered, even if no notification to the user is needed
            # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
            await query.answer()

            if query.data == 'cancel':
                await query.delete_message()
            elif query.data == 'unsubscribe_user':
                with self.app.app_context():
                    chat = get_or_create_chat(db.session, chat_id)
                    github_username = chat.github_username
                    chat.github_username = None
                    db.session.commit()

                    await query.edit_message_text(text=f"Unsubscribed from user {github_username}.")
            elif query.data.startswith("subscribe_user-"):
                github_user_name = query.data.split("-", 1)[1]
                try:
                    github_user = github_obj.get_user(github_user_name)
                except github.GithubException as e:
                    await update.message.reply_text("Error: User not founded.")
                    return

                with self.app.app_context():
                    chat = get_or_create_chat(db.session, chat_id)
                    chat.github_username = github_user.login
                    db.session.commit()

                    await query.edit_message_text(text=f"Subscribed to user {github_user.login} starred repos.")

                await self.add_starred_repos(chat_id, github_user, update.callback_query.get_bot())
            elif query.data.startswith("add_repos-"):
                github_user_name = query.data.split("-", 1)[1]
                try:
                    github_user = github_obj.get_user(github_user_name)
                except github.GithubException as e:
                    await update.message.reply_text("Error: User not founded.")
                    return

                await self.add_starred_repos(chat_id, github_user, update.callback_query.get_bot())

                await query.delete_message()
            elif query.data == "release_note_format":
                with self.app.app_context():
                    chat = get_or_create_chat(db.session, chat_id)
                    keyboard = [[InlineKeyboardButton(f"{"✅" if chat.release_note_format == "quote" else ""} Quote",
                                                      callback_data="release_note_format-quote"),
                                 InlineKeyboardButton(f"{"✅" if chat.release_note_format == "pre" else ""} Pre",
                                                      callback_data="release_note_format-pre"),
                                 InlineKeyboardButton(f"{"✅" if not chat.release_note_format else ""} Markdown",
                                                      callback_data="release_note_format-markdown"),
                                 InlineKeyboardButton(f"{"✅" if chat.release_note_format == "html" else ""} HTML",
                                                      callback_data="release_note_format-html"), ],
                        [InlineKeyboardButton("Cancel", callback_data="cancel")]]
                    reply_markup = InlineKeyboardMarkup(keyboard)

                await query.edit_message_reply_markup(reply_markup)
            elif query.data.startswith("release_note_format-"):
                with self.app.app_context():
                    chat = get_or_create_chat(db.session, chat_id)
                    if query.data == "release_note_format-quote":
                        chat.release_note_format = "quote"
                    elif query.data == "release_note_format-pre":
                        chat.release_note_format = "pre"
                    elif query.data == "release_note_format-markdown":
                        chat.release_note_format = None
                    elif query.data == "release_note_format-html":
                        chat.release_note_format = "html"
                    else:
                        await update.message.reply_text("Error: Unknown format.")
                        return
                    db.session.commit()

                await query.edit_message_text(text=f"Release note format changed.")
            elif query.data.startswith("next-"):
                next_page = int(query.data.split("-", 1)[1])
                keyboard = self.get_repo_keyboard(chat_id, next_page)
                if keyboard:
                    await query.edit_message_reply_markup(keyboard)
            elif query.data.startswith("prev-"):
                prev_page = int(query.data.split("-", 1)[1])
                keyboard = self.get_repo_keyboard(chat_id, prev_page)
                if keyboard:
                    await query.edit_message_reply_markup(keyboard)
            elif query.data.startswith("pre-"):
                _, curr_page, repo_id = query.data.split("-", 2)
                with self.app.app_context():
                    chat = get_or_create_chat(db.session, chat_id)
                    repo_obj = db.session.get(Repo, repo_id)
                    if not repo_obj:
                        await update.message.reply_text("Error: Repo not founded.")
                        return

                    chat_repo = db.session.query(ChatRepo) \
                        .filter(ChatRepo.chat_id == chat.id).filter(ChatRepo.repo_id == repo_obj.id) \
                        .first()
                    chat_repo.process_pre_releases = not chat_repo.process_pre_releases
                    db.session.commit()

                    if chat_repo.process_pre_releases:
                        reply_message = f"You are subscribed to repo <b>{repo_obj.full_name}</b> pre-releases."
                    else:
                        reply_message = f"You are unsubscribed from repo <b>{repo_obj.full_name}</b> pre-releases."
                    repo_url = repo_obj.link

                keyboard = self.get_repo_keyboard(chat_id, int(curr_page))
                await query.edit_message_reply_markup(keyboard)

                await update.callback_query.get_bot().send_message(chat_id, reply_message,
                                                                   parse_mode=ParseMode.HTML,
                                                                   link_preview_options=LinkPreviewOptions(
                                                                       url=repo_url,
                                                                       prefer_small_media=True)
                                                                   )
            elif query.data.startswith("delete-"):
                _, curr_page, repo_id = query.data.split("-", 2)
                curr_page = int(curr_page)
                with self.app.app_context():
                    chat = get_or_create_chat(db.session, chat_id)
                    repo_obj = db.session.get(Repo, repo_id)
                    if repo_obj:
                        chat.repos.remove(repo_obj)
                        db.session.commit()

                        reply_message = f"Deleted repo: <b>{repo_obj.full_name}</b>"
                        repo_url = repo_obj.link
                    else:
                        reply_message = "Error: Repo not founded."
                        repo_url = ""

                keyboard = self.get_repo_keyboard(chat_id, curr_page)
                if keyboard:
                    await query.edit_message_reply_markup(keyboard)
                else:
                    if curr_page > 0:
                        keyboard = self.get_repo_keyboard(chat_id, curr_page - 1)
                        await query.edit_message_reply_markup(keyboard)
                    else:
                        await query.edit_message_text(text="You no longer have any repos.")

                await update.callback_query.get_bot().send_message(chat_id, reply_message,
                                                                   parse_mode=ParseMode.HTML,
                                                                   link_preview_options=LinkPreviewOptions(
                                                                       url=repo_url,
                                                                       prefer_small_media=True)
                                                                   )

    async def starred_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /starred is issued."""
        if chat_id := self._get_chat_id(update):
            with self.app.app_context():
                chat = get_or_create_chat(db.session, chat_id)
                if chat.github_username:
                    keyboard = [[InlineKeyboardButton("Unsubscribe from user", callback_data="unsubscribe_user")],
                                [InlineKeyboardButton("Cancel", callback_data="cancel")]]
                    reply_markup = InlineKeyboardMarkup(keyboard)

                    await update.message.reply_text(f"You are already subscribe to the user {chat.github_username}.\n"
                                                    "Unsubscribe now?",
                                                    reply_markup=reply_markup)
                    return

            if not context.args or len(context.args) > 1:
                await update.message.reply_text("Specify a GitHub username in the following format: /starred username")
                return

            github_user_name = context.args[0]
            try:
                github_user = github_obj.get_user(github_user_name)
            except github.GithubException as e:
                await update.message.reply_text("Sorry, I can't find that user.")
                return

            starred = github_user.get_starred()

            keyboard = [[InlineKeyboardButton("Subscribe user", callback_data=f"subscribe_user-{github_user_name}")],
                        [InlineKeyboardButton("Add user's repos", callback_data=f"add_repos-{github_user_name}")],
                        [InlineKeyboardButton("Cancel", callback_data="cancel")]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(f"User {github_user_name} has {starred.totalCount} starred repos. "
                                            "Subscribe to the user or add user's repos once?",
                                            reply_markup=reply_markup)

    async def settings_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /settings is issued."""
        if self._get_chat_id(update):
            keyboard = [[InlineKeyboardButton("Release note format", callback_data="release_note_format")],
                        [InlineKeyboardButton("Cancel", callback_data="cancel")]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(f"Settings",
                                            reply_markup=reply_markup)

    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /stats is issued."""
        if self._get_chat_id(update):
            with (self.app.app_context()):
                release_count = db.session.query(Release).count()
                repo_count = db.session.query(Repo).count()
                user_count = db.session.query(Chat).count()
                subscription_count = db.session.query(ChatRepo).count()

                text = (f"I have to update {release_count} releases for {repo_count} repos via {subscription_count} "
                        f"subscriptions added by {user_count} users.")

            await update.message.reply_text(text)

    async def test_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /test is issued."""
        if chat_id := self._get_chat_id(update):
            with (self.app.app_context()):
                chat = get_or_create_chat(db.session, chat_id)

            if not context.args or len(context.args) > 1:
                await update.message.reply_text("Specify a GitHub release URL")
                return

            github_release_url = context.args[0]
            path_parts = urllib.parse.urlparse(github_release_url).path.strip('/').split('/')
            if len(path_parts) < 5 or path_parts[2] != 'releases' or path_parts[3] != 'tag':
                await update.message.reply_text("Wrong GitHub release URL")
                return

            repo = github_obj.get_repo(f"{path_parts[0]}/{path_parts[1]}")
            release = repo.get_release(path_parts[4])
            release.updated = False

            message, parse_mode, entities = format_release_message(chat.release_note_format, repo, release)

            await update.message.get_bot().send_message(chat_id, message,
                                                        parse_mode=parse_mode,
                                                        entities=entities,
                                                        link_preview_options=LinkPreviewOptions(
                                                            url=repo.html_url,
                                                            prefer_small_media=True)
                                                        )

    def _pypi2github(self, project_name):
        resp = urllib3.request("GET", f"https://pypi.org/pypi/{project_name}/json")
        repo_name = None
        if resp.status == 200:
            pypi_data = json.loads(resp.data.decode('utf-8'))
            if pypi_data["info"]["project_urls"]:
                if ("Source" in pypi_data["info"]["project_urls"] and
                        github_link_pattern.search(pypi_data["info"]["project_urls"]["Source"])):
                    link_groups = github_link_pattern.search(pypi_data["info"]["project_urls"]["Source"])
                    repo_name = link_groups.group(1)
                elif ("Source Code" in pypi_data["info"]["project_urls"] and
                      github_link_pattern.search(pypi_data["info"]["project_urls"]["Source Code"])):
                    link_groups = github_link_pattern.search(pypi_data["info"]["project_urls"]["Source Code"])
                    repo_name = link_groups.group(1)
                elif ("Homepage" in pypi_data["info"]["project_urls"] and
                      github_link_pattern.search(pypi_data["info"]["project_urls"]["Homepage"])):
                    link_groups = github_link_pattern.search(pypi_data["info"]["project_urls"]["Homepage"])
                    repo_name = link_groups.group(1)
            elif pypi_data["info"]["home_page"] and github_link_pattern.search(pypi_data["info"]["home_page"]):
                link_groups = github_link_pattern.search(pypi_data["info"]["home_page"])
                repo_name = link_groups.group(1)

        return resp.status, repo_name

    def _npm2github(self, package_name):
        package_name_quoted = urllib.parse.quote(package_name, safe='')
        resp = urllib3.request("GET", f"https://api.npms.io/v2/package/{package_name_quoted}")
        repo_name = None
        if resp.status == 200:
            npm_data = json.loads(resp.data.decode('utf-8'))
            if ("repository" in npm_data["collected"]["metadata"]["links"] and
                    github_link_pattern.search(npm_data["collected"]["metadata"]["links"]["repository"])):
                link_groups = github_link_pattern.search(npm_data["collected"]["metadata"]["links"]["repository"])
                repo_name = link_groups.group(1)
            elif ("homepage" in npm_data["collected"]["metadata"]["links"] and
                  github_link_pattern.search(npm_data["collected"]["metadata"]["links"]["homepage"])):
                link_groups = github_link_pattern.search(npm_data["collected"]["metadata"]["links"]["homepage"])
                repo_name = link_groups.group(1)
            elif ("homepage" in npm_data["collected"]["metadata"]["links"] and
                  github_link_pattern.search(npm_data["collected"]["metadata"]["links"]["repository"])):
                link_groups = github_link_pattern.search(npm_data["collected"]["metadata"]["links"]["repository"])
                repo_name = link_groups.group(1)

        return resp.status, repo_name

    async def message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Add GitHub repo"""
        if chat_id := self._get_chat_id(update):
            if self._is_group(update):
                text = update.effective_message.text.lower()
                bot_name = update.message.get_bot().username.lower()
                if not text.startswith(f"@{bot_name}"):
                    return

            if pypi_link_pattern.search(update.message.text):
                link_groups = pypi_link_pattern.search(update.message.text)
                project = link_groups.group(1)
                status, repo_name = self._pypi2github(project)
                if status == 200:
                    if not repo_name:
                        await update.message.reply_text(f"Project {project} has not link to GitHub repository.")
                        return
                else:
                    await update.message.reply_text("Error: Invalid repo.")
                    return
            elif npm_link_pattern.search(update.message.text):
                link_groups = npm_link_pattern.search(update.message.text)
                package_name = link_groups.group(1)
                status, repo_name = self._npm2github(package_name)
                if status == 200:
                    if not repo_name:
                        await update.message.reply_text(f"Project {package_name} has not link to GitHub repository.")
                        return
                else:
                    await update.message.reply_text("Error: Invalid repo.")
                    return
            elif github_link_pattern.search(update.message.text):
                link_groups = github_link_pattern.search(update.message.text)
                repo_name = link_groups.group(1)
            elif direct_pattern.search(update.message.text):
                repo_name = update.message.text
            else:
                await update.message.reply_text("Error: Invalid repo.")
                return

            try:
                repo = github_obj.get_repo(repo_name)
            except github.GithubException as e:
                await update.message.reply_text("Sorry, I can't find that repo.")
                print(f"GithubException for {repo_name} in message: {e}")
                return

            await self.add_repo(chat_id, repo, update.get_bot(), False)

    async def download_file(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Add GitHub repo from uploaded requirements.txt"""
        if chat_id := self._get_chat_id(update):
            if update.message.document.file_size > MAX_UPLOADED_FILE_SIZE:
                await update.message.reply_text("I can't process too big file.")
                return
            if update.message.document.file_name == "requirements.txt":
                file = await context.bot.get_file(update.message.document)
                data = await file.download_as_bytearray()
                decoded_string = data.decode("utf-8", errors='replace')
                for req in requirements.parse(decoded_string):
                    status, repo_name = self._pypi2github(req.name)
                    if status == 200 and repo_name:
                        try:
                            repo = github_obj.get_repo(repo_name)
                        except github.GithubException as e:
                            print("Github Exception in download_file", e)
                            continue

                        await self.add_repo(chat_id, repo, update.get_bot(), True)
            elif update.message.document.file_name == "package.json":
                file = await context.bot.get_file(update.message.document)
                data = await file.download_as_bytearray()
                decoded_string = data.decode("utf-8", errors='replace')
                json_data = json.loads(decoded_string)
                if "dependencies" in json_data:
                    for package in json_data["dependencies"].keys():
                        status, repo_name = self._npm2github(package)
                        if status == 200 and repo_name:
                            try:
                                repo = github_obj.get_repo(repo_name)
                            except github.GithubException as e:
                                print("Github Exception in download_file", e)
                                continue

                            await self.add_repo(chat_id, repo, update.get_bot(), True)
            else:
                await update.message.reply_text("I don't know this file format.")
                return

    async def unknown_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if self._get_chat_id(update):
            if self._is_group(update):
                text = update.effective_message.text.lower()
                bot_name = update.message.get_bot().username.lower()
                if len(text) > 2 and "@" in text[1:] and f"@{bot_name}" not in text:
                    return

            await update.message.reply_text("Sorry, I don't understand. Please pick one of the valid options.")
            await self.start_command(update, context)

    async def get_me(self, *args, **kwargs):
        async with self.application.bot:
            return await self.application.bot.getMe(*args, **kwargs)

    async def send_message(self, *args, **kwargs):
        async with self.application.bot:
            await self.application.bot.send_message(*args, **kwargs)

    async def test_token(self):
        try:
            async with self.application.bot:
                return True
        except telegram.error.InvalidToken:
            return False

    async def webhook(self, data):
        async with self.application.bot:
            await self.application.process_update(Update.de_json(data=data, bot=self.application.bot))

    async def run_webhook(self):
        await self.application.initialize()
        async with self.application.bot:
            await self.set_commands(self.application)
            await self.application.bot.set_webhook(url=f"{self.app.config['SITE_URL']}/telegram",
                                                   allowed_updates=Update.ALL_TYPES)

    async def run_polling(self):
        async with self.application:
            await self.application.start()
            await self.set_commands(self.application)
            await self.application.updater.start_polling()
            while True:
                await asyncio.sleep(1)

    def start(self):
        if self.app.config['SITE_URL']:
            asyncio.run(self.run_webhook())
        else:
            # Start the bot instance in thread
            bot = TelegramBot(self.app)
            thread = threading.Thread(target=asyncio.run, args=(bot.run_polling(),))
            thread.daemon = True
            thread.start()
