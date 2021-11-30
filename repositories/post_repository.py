from models import Post, Views
from schema import PostResponseSchema
from dto import PostResponseDTO


def create_post(post):
    post_save = Post(**post.__dict__).save()
    return str(post_save.id)


def read_post_list(page, category):
    if category:
        return Post.objects(category=category).paginate(page=page, per_page=10)
    return Post.objects.paginate(page=page, per_page=10)


def read_post_detail(id):
    num_posts = Views.objects(post_id=id).count()
    post = Post.objects.get_or_404(id=id)
    post_response= PostResponseSchema()
    post_response = post_response.load(post.to_mongo().to_dict())
    post_response.views= num_posts
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