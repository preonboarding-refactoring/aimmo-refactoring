from app import sqlite_db
from models import User


def signup(username, hashed_password):
    user = User(username=username, password=hashed_password)
    sqlite_db.session.add(user)
    sqlite_db.session.commit()