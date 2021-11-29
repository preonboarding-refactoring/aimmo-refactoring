from flask import Blueprint, jsonify, make_response

from services import auth_service

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup/', methods=['POST'])
def signup(username, password):
    auth_service.signup(username, password)
    return make_response(jsonify(msg='{} signup success'.format(username), status_code=201), 201)


@bp.route('/login/', methods=['POST'])
def login(username, password):
    is_login_success = auth_service.login(username, password)
    if is_login_success:
        return jsonify(access_token=is_login_success, status_code=200)
    else:
        return  make_response(jsonify(msg='잘못된 로그인 정보입니다.', status_code=404), 404)