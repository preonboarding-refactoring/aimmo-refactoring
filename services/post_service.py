from repositories import post_repository
from datetime import datetime

def create_post(post ):
    post.created_at = datetime.now()
    return post_repository.create_post(post)


def read_post_list(page, category):
    return post_repository.read_post_list(page, category)