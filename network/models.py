from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    MAX_LENGTH = 140
    bio = models.CharField(max_length=MAX_LENGTH, default="")
    following_count = models.PositiveIntegerField(default=0)
    follower_count = models.PositiveIntegerField(default=0)

    def snippet(self):
        return {
            "id": self.id,
            "username": self.username,
        }

    def serialize(self, user):
        return {
            "id": self.id,
            "username": self.username,
            "bio": self.bio,
            "following_count": self.following_count,
            "follower_count": self.follower_count,
            "following": self.followers.filter(user__id=self.id, follower__id=user.id).count() > 0,
            "followed": self.followers.filter(user__id=user.id, follower__id=self.id).count() > 0,
            "owner": self == user,
        }

    def update_counts(self):
        self.following_count = self.following.all().count()
        self.follower_count = self.followers.all().count()
        return self

    def is_valid(self):
        return len(self.bio) <= self.MAX_LENGTH


class Follow(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followers")
    follower = models.ForeignKey("User", on_delete=models.CASCADE, related_name="following")
    create_time = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "user": self.user.snippet(),
            "follower": self.follower.snippet(),
        }


class Post(models.Model):
    MAX_LENGTH = 140
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    text = models.CharField(max_length=MAX_LENGTH)
    parent = models.ForeignKey("Post", on_delete=models.DO_NOTHING, null=True, related_name="reposts")
    create_time = models.DateTimeField(auto_now_add=True)
    comment_count = models.PositiveIntegerField(default=0)
    repost_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)

    def serialize(self, user):
        return {
            "id": self.id,
            "author": self.author.snippet(),
            "text": self.text,
            "create_time": self.create_time.strftime("%b %d %Y, %I:%M %p"),
            "comment_count": self.comment_count,
            "repost_count": self.repost_count,
            "like_count": self.like_count,
            "liked": self.likes.filter(user__id=user.id).count() > 0,
            "owner": self.author == user,
        }

    def update_counts(self):
        self.comment_count = self.comments.all().count()
        self.repost_count = self.reposts.all().count()
        self.like_count = self.likes.all().count()
        return self

    def is_valid(self):
        return 0 < len(self.text) <= self.MAX_LENGTH


class Comment(models.Model):
    MAX_LENGTH = 140
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="comments")
    text = models.CharField(max_length=MAX_LENGTH)
    parent = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comments")
    create_time = models.DateTimeField(auto_now_add=True)

    def serialize(self, user):
        return {
            "id": self.id,
            "author": self.author.snippet(),
            "text": self.text,
            "create_time": self.create_time.strftime("%b %d %Y, %I:%M %p"),
            "owner": self.author == user,
        }


class Like(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="likes")
    create_time = models.DateTimeField(auto_now_add=True)


class HashTag(models.Model):
    MAX_LENGTH = 20
    user = models.ForeignKey("User", on_delete=models.DO_NOTHING, related_name="hashtags")
    post = models.ForeignKey("Post", on_delete=models.DO_NOTHING, related_name="hashtags")
    text = models.CharField(max_length=MAX_LENGTH)
    create_time = models.DateTimeField(auto_now_add=True)


class Mention(models.Model):
    user = models.ForeignKey("User", on_delete=models.DO_NOTHING, related_name="mentions")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="mentions")
    create_time = models.DateTimeField(auto_now_add=True)
