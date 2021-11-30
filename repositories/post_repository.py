from models import Post

def create_post(post):
    post_save=Post(**post.__dict__).save()
    return str(post_save.id)


def read_post_list(page, category):
    if category:
        return Post.objects(category=category).paginate(page=page, per_page=10)
    return Post.objects.paginate(page=page, per_page=10)

