from django.db import migrations
from django.contrib.auth.hashers import make_password
import json
import random


def load_testdata(apps, schema_editor):
    random.seed(123)
    # decide if post is repost/comment, <0.2 is original, > 0.5 is comment, middle is repost
    post_rand = [random.random() for i in range(500)]
    # 1st post cannot repost
    post_rand[0] = 0
    # decide parent in case of repost/comment
    parent = [random.randrange(0, i) if i > 0 else 0 for i in range(500)]
    # print(parent)
    # remember root as data populate
    root = []
    for i in range(500):
        is_comment = True if post_rand[i] > 0.5 else False
        if is_comment:
            if post_rand[parent[i]] > 0.5:
                root.append(root[parent[i]])
            else:
                root.append(parent[i])
        else:
            root.append(i)

    User = apps.get_model('network', 'User')
    Post = apps.get_model('network', 'Post')
    users = json.load(open('network/testdata/users.json'))
    posts = json.load(open('network/testdata/posts.json'))

    for u in users:
        User.objects.create(username=u['username'],
                            email=u['username']+'@test.com',
                            password=make_password(u['password']))

    for i, p in enumerate(posts):
        user = User.objects.get(id=int(p['author'])+1)
        is_comment = True if post_rand[i] > 0.5 else False
        parent_post = None if post_rand[i] < 0.2 else Post.objects.get(id=parent[i]+1)
        root_post = None

        if is_comment:
            if post_rand[parent[i]] > 0.5:
                root_post = Post.objects.get(id=root[parent[i]]+1)
            else:
                root_post = Post.objects.get(id=parent[i]+1)

        post = Post(author=user, text=p['text'],
                    parent=parent_post,
                    is_comment=is_comment,
                    root_post=root_post)
        post.save()



class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_testdata),
    ]
