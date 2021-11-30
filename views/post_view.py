from flask import Blueprint, make_response, jsonify
from flask import request, jsonify
from flask_jwt_extended.utils import get_jwt
# from service import post_service
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_apispec import use_kwargs, marshal_with
from services import post_service
from webargs.flaskparser import use_args
from schema import PostSchema, PostList, PostResponseSchema
from dto import PostDTO
import models

bp = Blueprint('post', __name__, url_prefix='/posts')


@bp.route('/create', methods=['POST'])
@use_args(PostSchema(partial=("author")))
def create_post(post: PostDTO):
    post.author_id = 1
    return post_service.create_post(post)


@bp.route('/', methods=['GET'])
@marshal_with(PostList)
def read_post_list():
    page = request.args.get('page', type=int, default=1)
    category = request.args.get('category')
    return post_service.read_post_list(page, category)


@bp.route('/<post_id>', methods=['GET'])
@marshal_with(PostResponseSchema)
def read_detail(post_id):
    cookie_value, max_age = post_service.count_hit_post(post_id, request)
    post = post_service.read_post_detail(post_id)
    response = make_response(post.__dict__)
    response.set_cookie('hitboard', value=cookie_value, max_age=max_age, httponly=True)
    return response
