from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from flask_migrate import Migrate

import pymongo
import config

sqlite_db = SQLAlchemy()

connection = pymongo.MongoClient()
sqlite_address = 'sqlite:///test.db'
migrate = Migrate()

def create_app():

    app = Flask(__name__)
    app.config.from_object(config)
    app.config['SQLALCHEMY_DATABASE_URI'] = sqlite_address

    sqlite_db.init_app(app)
    migrate.init_app(app, sqlite_db)
    jwt = JWTManager(app)
    import models

    from views import  auth_view
    app.register_blueprint(auth_view.bp)

    test1 = connection.test
    return app

app =create_app()


@app.route("/", methods=["GET"])
def hello():
    return "hello"
