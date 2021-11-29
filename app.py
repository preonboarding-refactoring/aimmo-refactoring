from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from flask_migrate import Migrate
from flask_mongoengine import MongoEngine

import config

sqlite_db = SQLAlchemy()

sqlite_address = 'sqlite:///test.db'
migrate = Migrate()
mongo_db = MongoEngine()

def create_app():

    app = Flask(__name__)
    app.config.from_object(config)
    app.config['SQLALCHEMY_DATABASE_URI'] = sqlite_address
    app.config['MONGODB_SETTINGS'] = {
        'host': 'mongodb://localhost/aimmo'
    }

    sqlite_db.init_app(app)
    migrate.init_app(app, sqlite_db)
    jwt = JWTManager(app)
    mongo_db.init_app(app)
    import models

    from views import  auth_view, post_view
    app.register_blueprint(auth_view.bp)
    app.register_blueprint(post_view.bp)

    return app

app =create_app()


@app.route("/", methods=["GET"])
def hello():
    return "hello"
