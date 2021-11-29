
from werkzeug.security import generate_password_hash

from repositories import auth_repository


def signup(username, password):
    hashed_password=generate_password_hash(password)
    return auth_repository.signup(username, hashed_password)