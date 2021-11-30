class PostDTO:
    def __init__(self, title, content, category):
        self.title = title
        self.content = content
        self.category = category


class PostResponseDTO:
    views: int
    def __init__(self, title, content, category, author_id, created_at, comment, _id):
        self._id = _id
        self.title = title
        self.content = content
        self.category = category
        self.author_id = author_id
        self.created_at = created_at
        self.comment = comment