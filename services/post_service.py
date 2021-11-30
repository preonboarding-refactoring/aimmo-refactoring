from repositories import post_repository
from datetime import datetime,timedelta

def create_post(post ):
    post.created_at = datetime.now()
    return post_repository.create_post(post)


def read_post_list(page, category):
    return post_repository.read_post_list(page, category)


def read_post_detail(id):
    post_data = post_repository.read_post_detail(id)
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