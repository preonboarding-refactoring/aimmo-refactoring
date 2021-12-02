import datetime


class PostDTO:
    author_id:int
    created_at: datetime.datetime
    def __init__(self, title, content, category):
        self.title = title
        self.content = content
        self.category = category


class PostResponseDTO:
    views: int
    def __init__(self, title, content, category, author_id, created_at, comment, _id, modified_at):
        self._id = _id
        self.title = title
        self.content = content
        self.category = category
        self.author_id = author_id
        self.created_at = created_at
        self.comment = comment
        self.modified_at = modified_at


class CommentDTO:
    created_at: datetime.datetime
    author_id: int
    post_id: str
    def __init__(self, content, oid):
        self.content = content
        self.oid = oid


class SearchDTO:
    def __init__(self, keyword, category):
        self.keyword = keyword
        self.category = category

class ReadPostListDto:
    def __init__(self, page, category):
        self.page = page
        self.category = category


class ReplyCommentPaginationDTO:
    def __init__(self, offset, limit):
        self.page = offset
        self.category = limit
