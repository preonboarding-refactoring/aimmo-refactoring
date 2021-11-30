from marshmallow import Schema, post_load
import bson
from marshmallow import ValidationError, fields, missing
from datetime import datetime

from dto import PostDTO, PostResponseDTO


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


class PostSchema(Schema):
    title = fields.String()
    content = fields.String()
    category = fields.String()
    author_id = fields.Integer()

    @post_load
    def make_post(self, data, **kwargs):
        return PostDTO(**data)


class PostList(Schema):
    page = fields.Integer()
    per_page = fields.Integer()
    total = fields.Integer()
    items = fields.List(fields.Nested(PostSchema))


class PostResponseSchema(Schema):
    title = fields.String()
    content = fields.String()
    category = fields.String()
    author_id = fields.Integer()
    _id = ObjectId()
    created_at = MyDateTimeField()
    comment = fields.List(fields.String)

    @post_load
    def make_post_response(self, data, **kwargs):
        return PostResponseDTO(**data)
