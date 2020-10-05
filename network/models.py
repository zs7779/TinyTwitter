from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    MAX_LENGTH = 140
    bio = models.CharField(max_length=MAX_LENGTH, default="")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "bio": self.bio,
            "followings": self.followings.count(),
            "followers": self.followers.count(),
        }


class Follow(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followers")
    follower = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followings")

    def serialize(self):
        return {
            "user": {
                "id": self.user.id,
                "username": self.user.username,
            },
            "follower": {
                "id": self.user.id,
                "username": self.user.username,
            }
        }


class Post(models.Model):
    MAX_LENGTH = 280
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    text = models.CharField(max_length=MAX_LENGTH)
    post_time = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField("User", related_name="likes")

    def serialize(self, user):
        return {
            "id": self.id,
            "author": self.author.serialize(),
            "text": self.text,
            "timestamp": self.post_time.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes.count(),
            "liked": self.likes.filter(id=user.id).count() > 0,
            "owner": self.author == user,
        }

    def is_valid(self):
        return 0 < len(self.text) <= self.MAX_LENGTH
