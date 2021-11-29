from flask import Blueprint, make_response, jsonify
from flask import request, jsonify
from flask_jwt_extended.utils import get_jwt
# from service import post_service
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_apispec import use_kwargs
from services import post_service
from webargs.flaskparser import use_args
from schema import PostDTO, PostSchema
import models

bp = Blueprint('post', __name__, url_prefix='/post')


@bp.route('/create', methods=['POST'])
@use_args(PostSchema(partial=("author")))
def create_post(post: PostDTO):
    post.author_id = 1
    return post_service.create_post(post)
