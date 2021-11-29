from app import sqlite_db

class User(sqlite_db.Model):
    id = sqlite_db.Column(sqlite_db.Integer, primary_key=True, autoincrement=True)
    username = sqlite_db.Column(sqlite_db.String(20), unique=True, nullable=False)
    password = sqlite_db.Column(sqlite_db.String(200), nullable=False)