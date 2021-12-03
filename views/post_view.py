from flask import Blueprint, make_response, jsonify
from flask import request, jsonify
from flask_jwt_extended.utils import get_jwt
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_apispec import use_kwargs, marshal_with

from exceptions import InvalidUsage
from services import post_service
from schema import (PostRequestSchema, PostListResponseSchema, PostResponseSchema, CommentRequestSchema,
                    ReplyCommentPaginationSchema,
                    SearchSchema, ReadPostListRequestSchema, BasicResponseSchema)
from dto import (PostDTO, CommentDTO, SearchDTO, ReadPostListDto, ReplyCommentPaginationDTO)
from flask_apispec import doc

bp = Blueprint('post', __name__, url_prefix='/posts')


@bp.route('', methods=['POST'])
@doc(description='글 작성하기', tags=['post'])
@use_kwargs(PostRequestSchema())
@marshal_with(BasicResponseSchema, code=201)
def create_post(post_dto: PostDTO):
    post_dto.author_id = 1
    post_service.create_post(post_dto)
    return jsonify(msg='update_success')


@bp.route('', methods=['GET'])
@doc(description='글 리스트 보기', tags=['post'])
@use_kwargs(ReadPostListRequestSchema(), location="query")
@marshal_with(PostListResponseSchema, code=200)
def read_post_list(read_post_list_dto: ReadPostListDto):
    return post_service.read_post_list(read_post_list_dto)


@bp.route('/<post_id>', methods=['GET'])
@doc(description='글 자세히 보기', tags=['post'])
@use_kwargs(ReplyCommentPaginationSchema(), location="query")
@marshal_with(PostResponseSchema, code=200)
def read_detail(reply_comment_pagination_dto: ReplyCommentPaginationDTO, post_id: str):
    cookie_value, max_age = post_service.count_hit_post(post_id, request)
    post = post_service.read_post_detail(post_id, reply_comment_pagination_dto)
    response = make_response(post.__dict__)
    response.set_cookie('hitboard', value=cookie_value, max_age=max_age, httponly=True)
    return response


@bp.route('/<post_id>', methods=['DELETE'])
@doc(description='글 삭제하기', tags=['post'])
@marshal_with(None,code=204)
def delete_post(post_id: str):
    current_user_id = 1
    if post_service.delete_post_if_user_authorized(post_id, current_user_id):
        return make_response('', 204)
    else:
        raise InvalidUsage.no_authority()

@bp.route('/<post_id>', methods=['PUT', 'PATCH'])
@doc(description='글 수정하기', tags=['post'])
@use_kwargs(PostRequestSchema())
@marshal_with(BasicResponseSchema, code=200)
def update_post(post_dto: PostDTO, post_id: str):
    current_user_id = 1
    post_dto.author_id = current_user_id
    post_dto.id = post_id
    if post_service.update_post(post_dto):
        return jsonify(msg='update_success'), 200
    else:
        raise InvalidUsage.no_authority()


@bp.route('/<post_id>/comment', methods=['POST'])
@doc(description='댓글달기', tags=['post'])
@use_kwargs(CommentRequestSchema())
@marshal_with(BasicResponseSchema, 201)
def create_comment(comment_dto: CommentDTO, post_id: str):
    user_id = 1
    comment_dto.author_id = user_id
    comment_dto.post_id = post_id
    if post_service.create_comment(comment_dto):
        return jsonify(msg='create_comment_success')
    else:
        raise  InvalidUsage.post_not_found()


@bp.route('/search', methods=['GET'])
@doc(description='검색하기', tags=['post'])
@use_kwargs(SearchSchema(), location="query")
@marshal_with(PostResponseSchema( many=True), code=200)
def search_post(search_dto: SearchDTO):
    return post_service.search_keyword(search_dto)
