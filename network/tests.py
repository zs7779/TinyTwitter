from django.test import TestCase, Client
from .models import User, Post, Like, Follow
import json


users = json.load(open('network/testdata/users.json'))
posts = json.load(open('network/testdata/posts.json'))


class ReadTestCase(TestCase):
    def test_posts_visitor(self):
        c = Client()
        response = c.get('/api/posts/')
        self.assertEqual(response.status_code, 200)
        response = c.get('/api/posts/home')
        self.assertEqual(response.status_code, 200)
        user1 = User.objects.all()[0]
        response = c.get(f'/api/users/{user1.username}/posts/')
        self.assertEqual(response.status_code, 200)

    def test_post_visitor(self):
        c = Client()
        post1 = Post.objects.all()[0]
        response = c.get(f'/api/posts/{post1.id}')
        self.assertEqual(response.status_code, 200)
        user1 = User.objects.all()[0]
        response = c.get(f'/api/users/{user1.username}/posts/{post1.id}')
        self.assertEqual(response.status_code, 200)
    
    def test_user_visitor(self):
        c = Client()
        user1 = User.objects.all()[0]
        response = c.get(f'/api/users/{user1.username}')
        self.assertEqual(response.status_code, 200)

    def test_posts_user(self):
        user1 = users[0]
        c = Client()
        c.login(username=user1['username'], password=user1['password'])
        
        response = c.get('/api/posts/')
        self.assertEqual(response.status_code, 200)
        response = c.get('/api/posts/home')
        self.assertEqual(response.status_code, 200)
        user1 = User.objects.all()[0]
        response = c.get(f'/api/users/{user1.username}/posts/')
        self.assertEqual(response.status_code, 200)

    def test_post_user(self):
        user1 = users[0]
        c = Client()
        c.login(username=user1['username'], password=user1['password'])

        post1 = Post.objects.all()[0]
        response = c.get(f'/api/posts/{post1.id}')
        self.assertEqual(response.status_code, 200)
        user1 = User.objects.all()[0]
        response = c.get(f'/api/users/{user1.username}/posts/{post1.id}')
        self.assertEqual(response.status_code, 200)
    
    def test_user_user(self):
        user1 = users[0]
        c = Client()
        c.login(username=user1['username'], password=user1['password'])

        user1 = User.objects.all()[0]
        response = c.get(f'/api/users/{user1.username}')
        self.assertEqual(response.status_code, 200)

class PostsWriteTestCase(TestCase):
    def test_new_post_good(self):
        user1 = users[0]
        c = Client()
        c.login(username=user1['username'], password=user1['password'])

        old_count = Post.objects.filter(is_comment=False).count()
        response = c.post('/api/posts/',
                          data={'text': '1'},
                          content_type="application/json")
        self.assertEqual(response.status_code, 201)
        new_count = Post.objects.filter(is_comment=False).count()
        self.assertEqual(old_count+1, new_count)

    def test_new_post_bad_text(self):
        user1 = users[0]
        c = Client()
        c.login(username=user1['username'], password=user1['password'])

        old_count = Post.objects.filter(is_comment=False).count()
        response = c.post('/api/posts/',
                          data={'text': ''},
                          content_type="application/json")
        self.assertEqual(response.status_code, 400)
        new_count = Post.objects.filter(is_comment=False).count()
        self.assertEqual(old_count, new_count)

    def test_new_repost_good(self):
        user1 = users[0]
        c = Client()
        c.login(username=user1['username'], password=user1['password'])

        old_count = Post.objects.filter(is_comment=False).count()
        post1 = Post.objects.all()[0]
        response = c.post('/api/posts/',
                          data={'text': '1', 'parent_id': post1.id},
                          content_type="application/json")
        self.assertEqual(response.status_code, 201)
        new_count = Post.objects.filter(is_comment=False).count()
        self.assertEqual(old_count+1, new_count)

    def test_new_repost_bad_parent(self):
        user1 = users[0]
        c = Client()
        c.login(username=user1['username'], password=user1['password'])

        old_count = Post.objects.filter(is_comment=False).count()
        post1 = Post.objects.all()[0]
        response = c.post('/api/posts/',
                          data={'text': '1', 'parent_id': -1},
                          content_type="application/json")
        self.assertEqual(response.status_code, 404)
        new_count = Post.objects.filter(is_comment=False).count()
        self.assertEqual(old_count, new_count)

class PostWriteTestCase(TestCase):
    def test_new_comment_good(self):
        user1 = users[0]
        c = Client()
        c.login(username=user1['username'], password=user1['password'])

        old_count = Post.objects.filter(is_comment=True).count()
        post1 = Post.objects.all()[0]
        response = c.post(f'/api/posts/{post1.id}',
                          data={'text': '1', 'parent_id': post1.id},
                          content_type="application/json")
        self.assertEqual(response.status_code, 201)
        new_count = Post.objects.filter(is_comment=True).count()
        self.assertEqual(old_count+1, new_count)

    def test_new_comment_bad_id(self):
        user1 = users[0]
        c = Client()
        c.login(username=user1['username'], password=user1['password'])

        old_count = Post.objects.filter(is_comment=True).count()
        post1 = Post.objects.all()[0]
        response = c.post(f'/api/posts/{-1}',
                          data={'text': '1', 'parent_id': post1.id},
                          content_type="application/json")
        self.assertEqual(response.status_code, 404)
        new_count = Post.objects.filter(is_comment=True).count()
        self.assertEqual(old_count, new_count)
    
    def test_new_comment_bad_parent(self):
        user1 = users[0]
        c = Client()
        c.login(username=user1['username'], password=user1['password'])

        old_count = Post.objects.filter(is_comment=True).count()
        post1 = Post.objects.all()[0]
        response = c.post(f'/api/posts/{post1.id}',
                          data={'text': '1', 'parent_id': -1},
                          content_type="application/json")
        self.assertEqual(response.status_code, 404)
        new_count = Post.objects.filter(is_comment=True).count()
        self.assertEqual(old_count, new_count)

    def test_delete_post_good(self):
        user1 = users[0]
        c = Client()
        c.login(username=user1['username'], password=user1['password'])

        old_count = Post.objects.count()
        post1 = User.objects.get(username=user1['username']).posts.all()[0]
        response = c.delete(f'/api/posts/{post1.id}')
        self.assertEqual(response.status_code, 200)
        new_count = Post.objects.count()
        self.assertEqual(old_count-1, new_count)

    def test_delete_post_bad_authorization(self):
        user1 = users[0]
        user2 = users[1]
        c = Client()
        c.login(username=user1['username'], password=user1['password'])

        old_count = Post.objects.count()
        post2 = User.objects.get(username=user2['username']).posts.all()[0]
        response = c.delete(f'/api/posts/{post2.id}')
        self.assertEqual(response.status_code, 403)
        new_count = Post.objects.count()
        self.assertEqual(old_count, new_count)

    def test_delete_post_bad_id(self):
        user1 = users[0]
        c = Client()
        c.login(username=user1['username'], password=user1['password'])

        old_count = Post.objects.count()
        post1 = User.objects.get(username=user1['username']).posts.all()[0]
        response = c.delete(f'/api/posts/{-1}')
        self.assertEqual(response.status_code, 404)
        new_count = Post.objects.count()
        self.assertEqual(old_count, new_count)

    def test_new_like_good(self):
        user1 = users[0]
        c = Client()
        c.login(username=user1['username'], password=user1['password'])

        old_count = Like.objects.count()
        post1 = Post.objects.all()[0]
        response = c.post(f'/api/posts/{post1.id}',
                          data={'like': True},
                          content_type="application/json")
        self.assertEqual(response.status_code, 200)
        new_count = Like.objects.count()
        self.assertEqual(old_count+1, new_count)

    def test_new_unlike_good(self):
        user1 = users[0]
        c = Client()
        c.login(username=user1['username'], password=user1['password'])

        old_count = Like.objects.count()
        post1 = Post.objects.all()[0]
        response = c.post(f'/api/posts/{post1.id}',
                          data={'like': True},
                          content_type="application/json")
        self.assertEqual(response.status_code, 200)
        new_count = Like.objects.count()
        self.assertEqual(old_count+1, new_count)
        response = c.post(f'/api/posts/{post1.id}',
                          data={'like': False},
                          content_type="application/json")
        self.assertEqual(response.status_code, 200)
        new_count = Like.objects.count()
        self.assertEqual(old_count, new_count)

    def test_edit_post_good(self):
        user1 = users[0]
        c = Client()
        c.login(username=user1['username'], password=user1['password'])

        old_count = Post.objects.count()
        post1 = User.objects.get(username=user1['username']).posts.all()[0]
        response = c.patch(f'/api/posts/{post1.id}',
                          data={'text': 'tespoirakjdgkqjheb'},
                          content_type="application/json")
        self.assertEqual(response.status_code, 200)
        new_count = Post.objects.count()
        self.assertEqual(old_count, new_count)
        post1 = Post.objects.get(id=post1.id)
        self.assertEqual(post1.text, 'tespoirakjdgkqjheb')

    def test_edit_post_bad_authorization(self):
        user1 = users[0]
        user2 = users[1]
        c = Client()
        c.login(username=user1['username'], password=user1['password'])

        old_count = Post.objects.count()
        post1 = User.objects.get(username=user2['username']).posts.all()[0]
        response = c.patch(f'/api/posts/{post1.id}',
                          data={'text': 'tespoirakjdgkqjhebnzcjzxiojhwe'},
                          content_type="application/json")
        self.assertEqual(response.status_code, 403)
        new_count = Post.objects.count()
        self.assertEqual(old_count, new_count)
        post1 = User.objects.all()[0].posts.all()[0]
        self.assertNotEqual(post1.text, 'tespoirakjdgkqjhebnzcjzxiojhwe')

class ProfileWriteTestCase(TestCase):
    def test_new_follow_good(self):
        user1 = users[0]
        user2 = users[1]
        c = Client()
        c.login(username=user1['username'], password=user1['password'])

        old_count = Follow.objects.count()
        response = c.post(f'/api/users/{user2["username"]}',
                          data={'follow': True},
                          content_type="application/json")
        self.assertEqual(response.status_code, 200)
        new_count = Follow.objects.count()
        self.assertEqual(old_count+1, new_count)
        response = c.post(f'/api/users/{user2["username"]}',
                          data={'follow': True},
                          content_type="application/json")
        self.assertEqual(response.status_code, 200)
        new_count = Follow.objects.count()
        self.assertEqual(old_count+1, new_count)

    def test_new_unfollow_good(self):
        user1 = users[0]
        user2 = users[1]
        c = Client()
        c.login(username=user1['username'], password=user1['password'])

        old_count = Follow.objects.count()
        response = c.post(f'/api/users/{user2["username"]}',
                          data={'follow': True},
                          content_type="application/json")
        self.assertEqual(response.status_code, 200)
        new_count = Follow.objects.count()
        self.assertEqual(old_count+1, new_count)
        response = c.post(f'/api/users/{user2["username"]}',
                          data={'follow': False},
                          content_type="application/json")
        self.assertEqual(response.status_code, 200)
        new_count = Follow.objects.count()
        self.assertEqual(old_count, new_count)
        response = c.post(f'/api/users/{user2["username"]}',
                          data={'follow': False},
                          content_type="application/json")
        self.assertEqual(response.status_code, 200)
        new_count = Follow.objects.count()
        self.assertEqual(old_count, new_count)
    
    def test_new_follow_bad_username(self):
        user1 = users[0]
        c = Client()
        c.login(username=user1['username'], password=user1['password'])

        old_count = Follow.objects.count()
        response = c.post(f'/api/users/{"_bad_user_adsklhzxlcioqwenmhf_"}',
                          data={'follow': True},
                          content_type="application/json")
        self.assertEqual(response.status_code, 404)
        new_count = Follow.objects.count()
        self.assertEqual(old_count, new_count)
    
    def test_new_follow_bad_same_user(self):
        user1 = users[0]
        c = Client()
        c.login(username=user1['username'], password=user1['password'])

        old_count = Follow.objects.count()
        response = c.post(f'/api/users/{user1["username"]}',
                          data={'follow': True},
                          content_type="application/json")
        self.assertEqual(response.status_code, 403)
        new_count = Follow.objects.count()
        self.assertEqual(old_count, new_count)