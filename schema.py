from marshmallow import Schema, fields

class Post(Schema):
    title = fields.String()
    content =fields.String()
    category =fields.String()
    author = fields.Integer()