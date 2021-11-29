
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token
from repositories import auth_repository


def signup(username, password):
    hashed_password=generate_password_hash(password)
    return auth_repository.signup(username, hashed_password)


def login(username, password):
    user_id_num = auth_repository.login(username, password)
    if user_id_num > 0:
        return create_access_token(user_id_num)
    else:
        return None