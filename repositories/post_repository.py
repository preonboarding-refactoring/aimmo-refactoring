from models import Post, Views, Comment, ReplyComment
from schema import PostResponseSchema


def create_post(post):
    post_save = Post(**post.__dict__).save()
    return str(post_save.id)


def read_post_list(page, category):
    if category:
        return Post.objects(category=category).paginate(page=page, per_page=10)
    return Post.objects.paginate(page=page, per_page=10)


def read_post_detail(id, reply_comment_pagination):
    num_posts = Views.objects(post_id=id).count()
    post = Post.objects.fields(slice__comment__reply_comment=[reply_comment_pagination["offset"],
                                                              reply_comment_pagination["offset"] + reply_comment_pagination["limit"]]).get_or_404(
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
    OID = comment_dto.OID
    del comment_dto.post_id
    del comment_dto.OID
    child_comment = ReplyComment(**comment_dto.__dict__)
    Post.objects(id=post_id, comment__oid=OID).update(push__comment__S__reply_comment=child_comment)
    return True


def create_parent_comment(comment_dto):
    del comment_dto.OID
    comment = Comment(**comment_dto.__dict__)
    post = Post.objects.get_or_404(id=comment_dto.post_id)
    post.comment.append(comment)
    post.save()
    return post.to_json
