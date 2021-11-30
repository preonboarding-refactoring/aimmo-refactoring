from marshmallow import Schema, fields, post_load

class PostDTO:
    def __init__(self, title, content,category):
        self.title = title
        self.content = content
        self.category = category


class PostSchema(Schema):
    title = fields.String()
    content = fields.String()
    category = fields.String()
    author = fields.Integer()

    @post_load
    def make_post(self, data, **kwargs):
        return PostDTO(**data)



class PostList(Schema):
   page = fields.Integer()
   per_page = fields.Integer()
   total = fields.Integer()
   items = fields.List(fields.Nested(PostSchema))

