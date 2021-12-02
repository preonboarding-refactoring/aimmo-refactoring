from marshmallow import Schema, post_load
import bson
from marshmallow import ValidationError, fields, missing, INCLUDE
from datetime import datetime

from dto import PostDTO, PostResponseDTO, CommentDTO, SearchDTO, ReadPostListDto


class MyDateTimeField(fields.DateTime):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, datetime):
            return value
        return super()._deserialize(value, attr, data)


class ObjectId(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return str(bson.ObjectId(value))
        except Exception:
            raise ValidationError("invalid ObjectId `%s`" % value)

    def _serialize(self, value, attr, obj):
        if value is None:
            return missing
        return str(value)


class ReplyComment(Schema):
    content = fields.String()
    author_id = fields.Integer()
    created_at = MyDateTimeField()


class Comment(Schema):
    content = fields.String()
    category = fields.String()
    author_id = fields.Integer()
    created_at = MyDateTimeField()
    post_id = fields.String()
    reply_comment = fields.List(fields.Nested(ReplyComment))
    oid = ObjectId()


class PostRequestSchema(Schema):
    title = fields.String()
    content = fields.String()
    category = fields.String()

    @post_load
    def make_post(self, data, **kwargs):
        return PostDTO(**data)


class PostList(Schema):
    page = fields.Integer()
    per_page = fields.Integer()
    total = fields.Integer()
    items = fields.List(fields.Nested(PostRequestSchema))


class PostResponseSchema(Schema):
    title = fields.String()
    content = fields.String()
    category = fields.String()
    author_id = fields.Integer()
    _id = ObjectId()
    created_at = MyDateTimeField()
    comment = fields.List(fields.Nested(Comment))

    @post_load
    def make_post_response(self, data, **kwargs):
        return PostResponseDTO(**data)

    class Meta:
        unknown = INCLUDE


class CommentRequestSchema(Schema):
    content = fields.String()
    oid = fields.String(missing="")

    @post_load
    def make_comment_dto(self, data, **kwargs):
        return CommentDTO(**data)


class ReplyCommentPaginationSchema(Schema):
    offset = fields.Integer(missing=1)
    limit = fields.Integer(missing=3)


class SearchSchema(Schema):
    keyword = fields.String()
    category = fields.String(missing="")

    @post_load
    def make_searchDTO(self, data, **kwargs):
        return SearchDTO(**data)

class ReadPostListRequestSchema(Schema):
    page = fields.Integer(missing=1)
    category = fields.String(missing="")

    @post_load
    def make_read_post_list_dto(self, data, **kwargs):
        return ReadPostListDto(**data)
