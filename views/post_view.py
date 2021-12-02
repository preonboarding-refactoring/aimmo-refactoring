from flask import Blueprint, make_response, jsonify
from flask import request, jsonify
from flask_jwt_extended.utils import get_jwt
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_apispec import use_kwargs, marshal_with
from services import post_service
from webargs.flaskparser import use_args
from marshmallow import fields
from schema import PostRequestSchema, PostList, PostResponseSchema, CommentRequestSchema, ReplyCommentPaginationSchema, SearchSchema, ReadPostListRequestSchema
from dto import PostDTO, CommentDTO, SearchDTO, ReadPostListDto, ReplyCommentPaginationDTO
from flask_apispec import doc

bp = Blueprint('post', __name__, url_prefix='/posts')


@bp.route('/create', methods=['POST'])
@doc(description='글 작성하기', tags=['post'])
@use_kwargs(PostRequestSchema())
def create_post(post_dto: PostDTO):
    post_dto.author_id = 1
    return post_service.create_post(post_dto)


@bp.route('/', methods=['GET'])
@doc(description='글 리스트 보기', tags=['post'])
@use_kwargs(ReadPostListRequestSchema(), location="query")
@marshal_with(PostList)
def read_post_list(read_post_list_dto:ReadPostListDto):
    return post_service.read_post_list(read_post_list_dto)


@bp.route('/<post_id>', methods=['GET'])
@doc(description='글 자세히 보기', tags=['post'])
@use_kwargs(ReplyCommentPaginationSchema(), location="query")
@marshal_with(PostResponseSchema)
def read_detail(reply_comment_pagination_dto: ReplyCommentPaginationDTO, post_id):
    cookie_value, max_age = post_service.count_hit_post(post_id, request)
    post = post_service.read_post_detail(post_id, reply_comment_pagination_dto)
    response = make_response(post.__dict__)
    response.set_cookie('hitboard', value=cookie_value, max_age=max_age, httponly=True)
    return response


@bp.route('/<post_id>', methods=['DELETE'])
@doc(description='글 삭제하기', tags=['post'])
def delete_post(post_id):
    current_user_id = 1
    if post_service.delete_post_if_user_authorized(post_id, current_user_id):
        return make_response('', 204)
    return make_response(jsonify(msg="권한이 없습니다. 해당 글을 쓰신 유저가 맞는지 확인해주세요.", status_code=401), 401)


@bp.route('/<post_id>', methods=['PUT', 'PATCH'])
@doc(description='글 수정하기', tags=['post'])
@use_kwargs(PostRequestSchema())
def update_post(post_dto: PostDTO, post_id):
    current_user_id = 1
    post_dto.author_id = current_user_id
    post_dto.id = post_id
    if post_service.update_post(post_dto):
        return make_response(jsonify(msg='update_success', status_code=200, id=str(post_id)), 200)
    return make_response(jsonify(msg="권한이 없습니다. 해당 글을 쓰신 유저가 맞는지 확인해주세요", status_code=401), 401)


@bp.route('/<post_id>/comment', methods=['POST'])
@doc(description='댓글달기', tags=['post'])
@use_kwargs(CommentRequestSchema())
def create_comment(comment_dto: CommentDTO, post_id):
    user_id = 1
    comment_dto.author_id = user_id
    comment_dto.post_id = post_id
    post_service.create_comment(comment_dto)
    return make_response(jsonify(msg='create_comment_success', status_code=201, id=str(id)), 201)


@bp.route('/search', methods=['GET'])
@doc(description='검색하기', tags=['post'])
@use_kwargs(SearchSchema(), location="query")
def search_post(search_dto: SearchDTO):
    posts = post_service.search_keyword(search_dto).to_json()
    return make_response(posts, 200)
