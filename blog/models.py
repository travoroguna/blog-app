from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from flask import current_app
from flask_migrate import Migrate
import datetime


db = current_app.extensions["sqlalchemy"]

def now():
    return datetime.datetime.now(datetime.timezone.utc)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(255))
    posts = db.relationship("Post", back_populates="author", cascade="all, delete-orphan")
    drafts = db.relationship("Draft", back_populates="author")

    def __str__(self) -> str:
        return f"User(username={self.username})"

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, nullable=False, default=now)
    modified = db.Column(db.DateTime, nullable=False, default=now, onupdate=now)
    author= db.relationship("User", back_populates="posts")
    author_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

    def __str__(self) -> str:
        return f"Post(title={self.title}, author={self.author}, created={self.created}, modified={self.modified})"


class Draft(db.Model):
    __tablename__ = "drafts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text)
    body = db.Column(db.Text)

    author_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete='CASCADE'))
    author = db.relationship("User", back_populates="drafts")
