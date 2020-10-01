from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField("User", related_name="followers")


class Post(models.Model):
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="author")
    text = models.CharField(max_length=140)
    post_time = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
