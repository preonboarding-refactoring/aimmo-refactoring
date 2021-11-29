from app import sqlite_db
from models import User
from werkzeug.security import check_password_hash


def signup(username, hashed_password):
    user = User(username=username, password=hashed_password)
    sqlite_db.session.add(user)
    sqlite_db.session.commit()


def login(username, password):
    user = User.query.filter_by(username=username).first()
    if not user:
        return 0
    else:
        if check_password_hash(user.password, password):
            return user.id
        else:
            return 0