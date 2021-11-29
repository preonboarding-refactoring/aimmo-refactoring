from app import sqlite_db
from app import mongo_db


class User(sqlite_db.Model):
    id = sqlite_db.Column(sqlite_db.Integer, primary_key=True, autoincrement=True)
    username = sqlite_db.Column(sqlite_db.String(20), unique=True, nullable=False)
    password = sqlite_db.Column(sqlite_db.String(200), nullable=False)


class ReplyComment(mongo_db.EmbeddedDocument):
    content = mongo_db.StringField(required=True)
    create_date = mongo_db.DateTimeField(required=True)


class Comment(mongo_db.EmbeddedDocument):
    content = mongo_db.StringField()
    create_date = mongo_db.DateTimeField(required=True)
    reply_comment = mongo_db.ListField(mongo_db.EmbeddedDocumentField(ReplyComment))


class Post(mongo_db.Document):
    title = mongo_db.StringField(max_length=120, required=True)
    content = mongo_db.StringField()
    author_id = mongo_db.IntField()
    create_date = mongo_db.DateTimeField()
    modify_date = mongo_db.DateTimeField()
    category = mongo_db.StringField(max_length=30)
    comment = mongo_db.ListField(mongo_db.EmbeddedDocumentField(Comment))


class Views(mongo_db.Document):
    post = mongo_db.ReferenceField(Post)
