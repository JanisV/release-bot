from datetime import datetime, timezone

from app import db


def aware_utcnow():
    return datetime.now(timezone.utc)


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lang = db.Column(db.String(2), default='en')
    github_username = db.Column(db.String)
    release_note_format = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=aware_utcnow)

    repos = db.relationship('Repo', secondary='chat_repo', back_populates='chats')


class Repo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String)
    description = db.Column(db.String)
    link = db.Column(db.String)
    archived = db.Column(db.Boolean)
    blocked = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=aware_utcnow)

    chats = db.relationship('Chat', secondary='chat_repo', back_populates='repos')
    releases = db.relationship('Release', back_populates='repos', cascade="all, delete-orphan")

    def is_orphan(self):
        # TODO: Use SQL COUNT instead Python len
        return len(self.chats) == 0

    def get_latest_release(self):
        if self.releases:
            return self.releases[-1]
        else:
            return None


class ChatRepo(db.Model):
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), primary_key=True)
    repo_id = db.Column(db.Integer, db.ForeignKey('repo.id'), primary_key=True)
    process_pre_releases = db.Column(db.Boolean, default=True, server_default=db.sql.True_())
    starred = db.Column(db.Boolean, default=False, server_default=db.sql.False_())


class Release(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    release_id = db.Column(db.Integer)
    tag_name = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    link = db.Column(db.String)
    pre_release = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=aware_utcnow)

    repo_id = db.Column(db.ForeignKey('repo.id'))
    repos = db.relationship('Repo', back_populates='releases')
