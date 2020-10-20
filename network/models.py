from django.contrib.auth.models import AbstractUser
from django.db import models


MAX_LENGTH = 140
DETAIL_SHORT = 0
DETAIL_LONG = 1
DETAIL_FULL = 2


class User(AbstractUser):
    bio = models.CharField(max_length=MAX_LENGTH, default="")
    following_count = models.PositiveIntegerField(default=0)
    follower_count = models.PositiveIntegerField(default=0)

    def serialize(self, user=None, detail=DETAIL_FULL):
        if detail == DETAIL_SHORT:
            return {
                "id": self.id,
                "username": self.username,
            }
        if detail == DETAIL_FULL:
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


class Follow(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followers")
    follower = models.ForeignKey("User", on_delete=models.CASCADE, related_name="following")
    create_time = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "user": self.user.serialize(detail=DETAIL_SHORT),
            "follower": self.follower.serialize(detail=DETAIL_SHORT),
        }


class Post(models.Model):
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    text = models.CharField(max_length=MAX_LENGTH)
    media_url = models.URLField(null=True, blank=True)
    parent = models.ForeignKey("Post", on_delete=models.DO_NOTHING, null=True, blank=True, related_name="reposts")
    create_time = models.DateTimeField(auto_now_add=True)
    comment_count = models.PositiveIntegerField(default=0)
    repost_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    is_comment = models.BooleanField(default=False)
    root_post = models.ForeignKey("Post", on_delete=models.DO_NOTHING, null=True, blank=True, related_name="comments")

    def serialize(self, user=None, detail=DETAIL_FULL):
        if detail == DETAIL_SHORT:
            return {
                "id": self.id,
                "author": self.author.serialize(detail=DETAIL_SHORT),
            }
        if detail == DETAIL_LONG:
            return {
                "id": self.id,
                "author": self.author.serialize(detail=DETAIL_SHORT),
                "text": self.text,
                "media_url": self.media_url,
                "create_time": self.create_time.strftime("%b %d %Y, %I:%M %p"),
                "is_comment": self.is_comment,           
            }
        if detail == DETAIL_FULL:
            return {
                "id": self.id,
                "author": self.author.serialize(detail=DETAIL_SHORT),
                "text": self.text,
                "media_url": self.media_url,
                "parent": self.parent.serialize(detail=DETAIL_LONG) if self.parent is not None else None,
                "create_time": self.create_time.strftime("%b %d %Y, %I:%M %p"),
                "comment_count": self.comment_count,
                "repost_count": self.repost_count,
                "like_count": self.like_count,
                "is_comment": self.is_comment,
                "root_post": self.root_post.serialize(detail=DETAIL_SHORT) if self.is_comment else None,
                "liked": self.likes.filter(user__id=user.id).count() > 0,
                "owner": self.author == user,
            }

    def update_counts(self):
        self.comment_count = self.comments.all().count()
        self.repost_count = self.reposts.all().count()
        self.like_count = self.likes.all().count()
        return self


class Like(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="likes")
    create_time = models.DateTimeField(auto_now_add=True)


class HashTag(models.Model):
    MAX_TAG_LENGTH = 20
    user = models.ForeignKey("User", on_delete=models.DO_NOTHING, related_name="hashtags")
    post = models.ForeignKey("Post", on_delete=models.DO_NOTHING, related_name="hashtags")
    text = models.CharField(max_length=MAX_TAG_LENGTH)
    create_time = models.DateTimeField(auto_now_add=True)


class Mention(models.Model):
    user = models.ForeignKey("User", on_delete=models.DO_NOTHING, related_name="mentions")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="mentions")
    create_time = models.DateTimeField(auto_now_add=True)
