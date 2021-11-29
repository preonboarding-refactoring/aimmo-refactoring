from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymongo

connection = pymongo.MongoClient()
slqite_address = 'sqlite:////test.db'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = slqite_address
sqlite_db = SQLAlchemy(app)

test1 = connection.test


@app.route("/", methods=["GET"])
def hello():
    return "hello"
