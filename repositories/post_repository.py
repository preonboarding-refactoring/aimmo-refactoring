from models import Post, Views, Comment, ReplyComment
from schema import PostResponseSchema
from sqlalchemy.exc import IntegrityError


def create_post(post_dto):
    post_save = Post(**post_dto.__dict__).save()
    return str(post_save.id)


def read_post_list(read_post_list_dto):
    if read_post_list_dto.category:
        return Post.objects(category=read_post_list_dto.category).paginate(page=read_post_list_dto.page, per_page=10)
    return Post.objects.paginate(page=read_post_list_dto.page, per_page=10)


def read_post_detail(id, reply_comment_pagination):
    num_posts = Views.objects(post_id=id).count()
    post = Post.objects.fields(slice__comment__reply_comment=[reply_comment_pagination.offset,
                                                              reply_comment_pagination.offset +
                                                              reply_comment_pagination.limit]).get_or_404(
        id=id)
    post_response = PostResponseSchema()
    post_response = post_response.load(post.to_mongo().to_dict())
    post_response.views = num_posts
    return post_response


def hit_post(id):
    Views(post_id=id).save()


def delete_post(id, current_user_id):
    post = Post.objects.get_or_404(id=id)
    if post.author_id == current_user_id:
        post.delete()
        return True
    return False


def update_post(modify_post):
    post = Post.objects.get_or_404(id=modify_post.id)
    if post.author_id == modify_post.author_id:
        post.update(**modify_post.__dict__)
        return True
    return False


def create_child_comment(comment_dto):
    post_id = comment_dto.post_id
    oid = comment_dto.oid
    del comment_dto.post_id
    del comment_dto.oid
    child_comment = ReplyComment(**comment_dto.__dict__)
    try:
        Post.objects(id=post_id, comment__oid=oid).update(push__comment__S__reply_comment=child_comment)
        return True
    except:
        return False


def create_parent_comment(comment_dto):
    del comment_dto.oid
    comment = Comment(**comment_dto.__dict__)
    post = Post.objects.get_or_404(id=comment_dto.post_id)
    post.comment.append(comment)
    post.save()
    return post.to_json


def search_post(search_dto):
    if not search_dto.category:
        return Post.objects(title=search_dto.keyword)
    return Post.objects(title=search_dto.keyword, category=search_dto.category)
