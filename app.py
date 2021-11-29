from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
sqlite_db =SQLAlchemy(app)

@app.route("/", methods=["GET"])
def hello():
    return "hello"