from repositories import post_repository
from datetime import datetime,timedelta
import re

def create_post(post ):
    post.created_at = datetime.now()
    return post_repository.create_post(post)


def read_post_list(page, category):
    return post_repository.read_post_list(page, category)


def read_post_detail(id, reply_comment_pagination):
    post_data = post_repository.read_post_detail(id, reply_comment_pagination)
    return post_data


def count_hit_post(id, request):
    ''' 24시까지 유효한 쿠키를 만든다.'''
    expire_date, now = datetime.now(), datetime.now()
    expire_date += timedelta(days=1)
    expire_date = expire_date.replace(hour=0, minute=0, second=0)
    expire_date -= now
    max_age = expire_date.total_seconds()

    cookie_value = request.cookies.get('hitboard', '_')
    if f'{id}' not in cookie_value:
        post_repository.hit_post(id)
        cookie_value += f'{id}_'
    return cookie_value, max_age


def delete_post_if_user_authorized(id, current_user_id):
    return post_repository.delete_post(id, current_user_id)

def update_post(modify_post):
    modify_post.modified_at = datetime.now()
    return post_repository.update_post(modify_post)


def create_comment(comment_dto):
    comment_dto.created_at = datetime.now()
    if comment_dto.oid:
        return post_repository.create_child_comment(comment_dto)
    return post_repository.create_parent_comment(comment_dto)


def search_keyword(search_dto ):
    search_dto.keyword = re.compile('.*' + search_dto.keyword + '.*')
    return post_repository.search_post(search_dto)
