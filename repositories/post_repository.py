import models

def create_post(post):
    post_save=models.Post(**post.__dict__).save()
    return str(post_save.id)
