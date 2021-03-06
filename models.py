from app import sqlite_db
from app import mongo_db
from bson.objectid import ObjectId


class User(sqlite_db.Model):
    id = sqlite_db.Column(sqlite_db.Integer, primary_key=True, autoincrement=True)
    username = sqlite_db.Column(sqlite_db.String(20), unique=True, nullable=False)
    password = sqlite_db.Column(sqlite_db.String(200), nullable=False)


class ReplyComment(mongo_db.EmbeddedDocument):
    content = mongo_db.StringField(required=True)
    created_at = mongo_db.DateTimeField(required=True)
    author_id = mongo_db.IntField()


class Comment(mongo_db.EmbeddedDocument):
    content = mongo_db.StringField()
    created_at = mongo_db.DateTimeField(required=True)
    reply_comment = mongo_db.ListField(mongo_db.EmbeddedDocumentField(ReplyComment))
    post_id =  mongo_db.StringField()
    author_id = mongo_db.IntField()
    oid = mongo_db.ObjectIdField(default=ObjectId)


class Post(mongo_db.Document):
    title = mongo_db.StringField(max_length=120, required=True)
    content = mongo_db.StringField()
    author_id = mongo_db.IntField()
    created_at = mongo_db.DateTimeField()
    modified_at = mongo_db.DateTimeField()
    category = mongo_db.StringField(max_length=30)
    comment = mongo_db.ListField(mongo_db.EmbeddedDocumentField(Comment))


class Views(mongo_db.Document):
    post_id = mongo_db.StringField()
