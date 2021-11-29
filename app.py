from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from flask_migrate import Migrate

import pymongo
import config


connection = pymongo.MongoClient()
slqite_address = 'sqlite:////test.db'
migrate = Migrate()

app = Flask(__name__)
app.config.from_object(config)
app.config['SQLALCHEMY_DATABASE_URI'] = slqite_address
sqlite_db = SQLAlchemy(app)
sqlite_db.init_app(app)
migrate.init_app(app,sqlite_db)
jwt = JWTManager(app)

test1 = connection.test


@app.route("/", methods=["GET"])
def hello():
    return "hello"
