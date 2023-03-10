from flask import current_app, g
from .models import db, User, Post
from typing import Optional
from werkzeug.security import check_password_hash, generate_password_hash


def new_user(username: str, password: str) -> bool:
    if db.session.query(User).filter_by(username=username).first():
        return False
    new_user = User(username=username, password=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()
    return True

def delete_user(username: str):
    if user := db.session.query(User).filter_by(username=username).first():
        db.session.delete(user)
        g.user = None
        db.session.commit()

def get_user_by_id(user_id: int) -> User:
    return db.session.query(User).filter_by(id=user_id).first()

def get_post_by_id(post_id: int) -> Post:
    return db.session.query(Post).filter_by(id=post_id).first()

def login(username: str, password: str) -> Optional[User]:
    if user := db.session.query(User).filter_by(username=username).first():
        if check_password_hash(user.password, password):
            return user
    return None

def new_post(title: str, body: str):
    post = Post(title=title, body=body, author=g.user)
    db.session.add(post)
    db.session.commit()

def get_posts(offset = 0, limit = 10) -> list[Post]:
    print(db.session.query(Post).all())
    return db.session.query(Post).limit(limit).all()

def edit_post(post_id: int, title: str, body: str):
    post = db.session.query(Post).filter_by(id=post_id).first()
    post.title = title
    post.body = body
    db.session.commit()

def delete_post(post_id: int):
    post = db.session.query(Post).filter_by(id=post_id).first()
    db.session.delete(post)
    db.session.commit()

