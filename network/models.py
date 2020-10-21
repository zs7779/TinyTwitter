from django.contrib.auth.models import AbstractUser
from django.db import models


MAX_LENGTH = 140
DETAIL_SHORT = 0
DETAIL_LONG = 1
DETAIL_FULL = 2


class User(AbstractUser):
    bio = models.CharField(max_length=MAX_LENGTH, default="")

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
                "following_count": self.following.all().count(),
                "follower_count": self.followers.all().count(),
                "following": self.followers.filter(user__id=self.id, follower__id=user.id).count() > 0,
                "followed": self.followers.filter(user__id=user.id, follower__id=self.id).count() > 0,
                "owner": self == user,
            }


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
    parent = models.ForeignKey("Post", on_delete=models.SET_NULL, null=True, blank=True, related_name="children")
    create_time = models.DateTimeField(auto_now_add=True)
    is_comment = models.BooleanField(default=False)
    root_post = models.ForeignKey("Post", on_delete=models.SET_NULL, null=True, blank=True, related_name="comments")

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
                "is_comment": self.is_comment,
                "root_post": self.root_post.serialize(detail=DETAIL_SHORT) if self.is_comment else None,
                "comment_count": self.children.filter(is_comment=True).count() if self.is_comment else self.comments.all().count(),
                "repost_count": self.children.filter(is_comment=False).count(),
                "like_count": self.likes.all().count(),
                "commented": self.children.filter(is_comment=True, author__id=user.id).count() if self.is_comment else self.comments.filter(author__id=user.id).count(),
                "reposted": self.children.filter(is_comment=False, author__id=user.id).count(),
                "liked": self.likes.filter(user__id=user.id).count(),
                "owner": self.author == user,
            }


class Like(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="likes")
    create_time = models.DateTimeField(auto_now_add=True)


class HashTag(models.Model):
    MAX_TAG_LENGTH = 20
    user = models.ForeignKey("User", on_delete=models.SET_NULL, null=True, blank=True, related_name="hashtags")
    post = models.ForeignKey("Post", on_delete=models.SET_NULL, null=True, blank=True, related_name="hashtags")
    text = models.CharField(max_length=MAX_TAG_LENGTH)
    create_time = models.DateTimeField(auto_now_add=True)


class Mention(models.Model):
    user = models.ForeignKey("User", on_delete=models.SET_NULL, null=True, blank=True, related_name="mentions")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="mentions")
    create_time = models.DateTimeField(auto_now_add=True)
