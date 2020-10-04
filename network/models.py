from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField("User", related_name="followers")


class Post(models.Model):
    MAX_LENGTH = 140
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="author")
    text = models.CharField(max_length=MAX_LENGTH)
    post_time = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField("User", related_name="likes")

    def serialize(self, user):
        return {
            "id": self.id,
            "author": self.author.username,
            "text": self.text,
            "timestamp": self.post_time.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes.count(),
            "liked": self.likes.filter(id=user.id).count() > 0,
            "owner": self.author == user,
        }

    def is_valid(self):
        return 0 < len(self.text) <= self.MAX_LENGTH
