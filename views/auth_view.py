from flask import Blueprint, jsonify, make_response

from services import auth_service

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup/', methods=['POST'])
def signup(username, password):
    auth_service.signup(username, password)
    return make_response(jsonify(msg='{} signup success'.format(username), status_code=201), 201)