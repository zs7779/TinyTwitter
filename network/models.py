from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q
from django.http import JsonResponse
from django.core.exceptions import ValidationError

from .utils import isHashTag, isMention


MAX_LENGTH = 140
DETAIL_SHORT = 0
DETAIL_LONG = 1
DETAIL_FULL = 2


class User(AbstractUser):
    bio = models.CharField(max_length=MAX_LENGTH, default="")
    avatar_url = models.URLField(null=True, blank=True)

    def serialize(self, user=None, detail=DETAIL_FULL):
        result = {
            "id": self.id,
            "username": self.username,
            "avatar": self.avatar_url,
        }
        if detail == DETAIL_SHORT:
            return result
        result.update({
            "bio": self.bio,
            "following_count": self.following.all().count(),
            "follower_count": self.followers.all().count(),
            "following": self.followers.filter(user__id=self.id, follower__id=user.id).count() > 0,
            "followed": self.followers.filter(user__id=user.id, follower__id=self.id).count() > 0,
            "owner": self == user,
        })
        if detail == DETAIL_FULL:
            return result

    def get_user_by_username(username, requestor):
        """
        Returns response of GET user request

        Parameters:
        username (str): username of requested user
        requestor (User): User instance of requestor

        Returns:
        response (JsonResponse): JsonResponse to the request, with serialized User object if successful
        """
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({"error": "User does not exist"}, status=404)
        return JsonResponse({
            "user": user.serialize(requestor),
        })


class Follow(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followers")
    follower = models.ForeignKey("User", on_delete=models.CASCADE, related_name="following")
    create_time = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "user": self.user.serialize(detail=DETAIL_SHORT),
            "follower": self.follower.serialize(detail=DETAIL_SHORT),
        }

    def create_follow(follow, followee, requestor):
        """
        Returns response of POST follow request

        Parameters:
        follow (bool): True for follow, False for unfollow
        followee (User): User instance of the user being followed
        requestor (User): User instance of the user requesting to follow

        Returns:
        response (JsonResponse): JsonResponse with success message 
        """
        if follow:
            try:
                follow_obj = Follow.objects.get(user=followee, follower=requestor)
            except Follow.DoesNotExist:
                follow_obj = Follow(user=followee, follower=requestor)
                follow_obj.save()
        else:
            follows = Follow.objects.filter(user=followee, follower=requestor)
            for follow_obj in follows:
                follow_obj.delete()
        return JsonResponse({"message": "Follow succesful"}, status=200)


class Post(models.Model):
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    text = models.CharField(max_length=MAX_LENGTH)
    media_url = models.URLField(null=True, blank=True)
    parent = models.ForeignKey("Post", on_delete=models.SET_NULL, null=True, blank=True, related_name="children")
    create_time = models.DateTimeField(auto_now_add=True)
    is_comment = models.BooleanField(default=False)
    root_post = models.ForeignKey("Post", on_delete=models.CASCADE, null=True, blank=True, related_name="comments")

    def get_mentions(self):
        """
        Returns list of users mentioned by this poost
        """
        result = [m.user.serialize(detail=DETAIL_SHORT) for m in self.mentions.all()]
        if self.root_post:
            result.append(self.root_post.author.serialize(detail=DETAIL_SHORT))
        if self.parent:
            result.append(self.parent.author.serialize(detail=DETAIL_SHORT))
        return result

    def serialize(self, user=None, detail=DETAIL_FULL):
        result = {
            "id": self.id,
            "author": self.author.serialize(detail=DETAIL_SHORT),
        }
        if detail == DETAIL_SHORT:
            return result
        result.update({
            "text": self.text,
            "media_url": self.media_url,
            "create_time": self.create_time.strftime("%I:%M %p %b %d %Y"),
            "is_comment": self.is_comment,
            "mentions": self.get_mentions(),
            "comment_count": self.children.filter(is_comment=True).count() if self.is_comment else self.comments.all().count(),
            "repost_count": self.children.filter(is_comment=False).count(),
            "like_count": self.likes.all().count(),
            "commented": self.children.filter(is_comment=True, author__id=user.id).count() if self.is_comment else self.comments.filter(author__id=user.id).count(),
            "reposted": self.children.filter(is_comment=False, author__id=user.id).count(),
            "liked": self.likes.filter(user__id=user.id).count(),
        })
        if detail == DETAIL_LONG:
            return result
        result.update({
            "parent": self.parent.serialize(detail=DETAIL_LONG, user=user) if self.parent is not None else None,
            "root_post": self.root_post.serialize(detail=DETAIL_LONG, user=user) if self.is_comment else None,
            "owner": self.author == user,
        })
        if detail == DETAIL_FULL:  
            return result

    def get_posts_by_user(username, requestor, count=20, after=0, order_by="-create_time"):
        """
        Returns response of GET posts of user request

        Parameters:
        username (str): username of requested user
        requestor (User): User instance of the user requesting
        count (int): number of posts requested, default 20
        after (int): starting index of posts requested, default 0
        order_by (str): parameter to django ORM function order_by, default '-create_time'

        Returns:
        response (JsonResponse): JsonResponse to the get request, with serialized Post objects if succesful
        """
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({"error": "User does not exist"}, status=404)
        posts = Post.objects.filter(author=user, is_comment=False).order_by(order_by)[after:after+count]
        return JsonResponse({
            "posts": [post.serialize(requestor) for post in posts],
        }, safe=False)

    def get_posts(path, requestor, count=20, after=0, order_by="-create_time"):
        """
        Returns response of GET posts request, used to get posts for home page

        Parameters:
        path (str): path to get posts, implemented options are 'home' and 'all'
        requestor (User): User instance of the user requesting
        count (int): number of posts requested, default 20
        after (int): starting index of posts requested, default 0
        order_by (str): parameter to django ORM function order_by, default '-create_time'

        Returns:
        response (JsonResponse): JsonResponse to the get request, with serialized Post objects if succesful
        """
        if path == "home":
            posts = Post.objects.filter(Q(author__followers__follower=requestor) | Q(author=requestor), is_comment=False).order_by(order_by)[after:after+count]
            return JsonResponse({
                "posts": [post.serialize(requestor) for post in posts],
            }, safe=False)
        else:
            posts = Post.objects.filter(is_comment=False).order_by(order_by)[after:after+count]
            return JsonResponse({
                "posts": [post.serialize(requestor) for post in posts],
            }, safe=False)

    def get_post_by_id(post_id, requestor, count=20, after=0, order_by="-create_time"):
        """
        Returns response of GET post request

        Parameters:
        post_id (id): id of requested post
        requestor (User): User instance of the user requesting
        count (int): number of comments requested, default 20
        after (int): starting index of comments requested, default 0
        order_by (str): parameter to django ORM function order_by, default '-create_time'

        Returns:
        response (JsonResponse): JsonResponse to the get request, with serialized post and its comments if succesful
        """
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post does not exist"}, status=404)
        if post.is_comment:
            comments_query = post.children.filter(is_comment=True).order_by(order_by)[after:after+count]
        else:
            comments_query = post.comments.all().order_by(order_by)[after:after+count]
        comments = [comment.serialize(user=requestor) for comment in comments_query]
        return JsonResponse({
            "post": post.serialize(requestor),
            "comments": comments,
        }, safe=False)

    def create_post(text, parent_id, requestor, root_post=None, is_comment=False):
        """
        Returns response of POST new post request, used to create new post or comment

        Parameters:
        text (str): text content of the new post
        parent_id (id): id of parent post, None if the post has no parent
        requestor (User): User instance of the user requesting
        root_post (Post): Post instance of the root post in case of a comment, default None
        is_comment (bool): True for comment, False for regular post, default False

        Returns:
        response (JsonResponse): JsonResponse to the post request, with serialized Post object if succesful
        """
        parent_post = None
        if parent_id is not None:
            try:
                parent_post = Post.objects.get(id=parent_id)
            except Post.DoesNotExist:
                return JsonResponse({"error": "Parent post does not exist"}, status=404)      
        else:
            parent_post = None
        post = Post(author=requestor, text=text, parent=parent_post,
                    root_post=root_post, is_comment=is_comment)

        try:
            post.full_clean()
        except ValidationError as e:
            # print(e)
            return JsonResponse({"error": "Post body is illegal"}, status=400, safe=False)
        post.save()

        # Process hashtags and mentions
        words = text.split()
        hashtags = PostTag.create_tags(set(filter(isHashTag, words)), post)
        mentions = Mention.create_mentions(set(filter(isMention, words)), post)
        
        json_message = {
            "message": "Post successful",
        }
        if is_comment:
            json_message["comment"] = post.serialize(requestor)
        else:
            json_message["post"] = post.serialize(requestor)
        return JsonResponse(json_message, status=201)


class Like(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="likes")
    create_time = models.DateTimeField(auto_now_add=True)

    def create_like(like, post, requestor):
        """
        Returns response of POST like request, used to like or unlike a post

        Parameters:
        like (bool): True to like, False to unlike
        post (Post): Post instance of post being liked
        requestor (User): User instance of the user requesting like

        Returns:
        response (JsonResponse): JsonResponse with success message
        """
        if like:
            try:
                like = Like.objects.get(user=requestor, post=post)
            except Like.DoesNotExist:
                like = Like(user=requestor, post=post)
                like.save()
        else:
            likes = Like.objects.filter(user=requestor, post=post)
            for like in likes:
                like.delete()
        return JsonResponse({"message": "Like succesful"}, status=200)


class HashTag(models.Model):
    text = models.CharField(max_length=MAX_LENGTH, unique=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            'text': self.text,
        }

    def get_hashtag_posts(hashtag, requestor, count=20, after=0):
        try:
            tag = HashTag.objects.get(text=hashtag.lower())
        except HashTag.DoesNotExist:
            return JsonResponse({"error": "Hashtag does not exist"}, status=404)
        tags = tag.posts.all()[after:after+count]
        return JsonResponse({
            "posts": [post_tag.post.serialize(requestor) for post_tag in tags],
        }, safe=False)
        

class PostTag(models.Model):
    tag = models.ForeignKey("HashTag", on_delete=models.RESTRICT, related_name="posts")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="hashtags")    

    def serialize(self):
        return {
            'tag': self.tag.serialize(),
            'post': self.post.serialize(detail=DETAIL_SHORT),
        }

    def create_tags(tags, post):
        """
        Create hashtags for posts

        Parameters:
        tags (Set[str]): set of strings to be created as hashtags
        post (Post): post to be associated with the hashtags

        Returns:
        tags_array: created tags
        """
        tags_array = []
        for t in tags:
            try:
                hashtag = HashTag.objects.get(text=t[1:].lower())
            except HashTag.DoesNotExist:
                hashtag = HashTag(text=t[1:].lower())
                hashtag.save()
            tag = PostTag(tag=hashtag, post=post)
            tag.save()
            tags_array.append(tag.serialize())
        return tags_array


class Mention(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="mentions")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="mentions")
    create_time = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "user": self.user.serialize(detail=DETAIL_SHORT),
            "post": self.post.serialize(detail=DETAIL_SHORT),
        }

    def create_mentions(mentions, post):
        """
        Create mentions for posts

        Parameters:
        mentions (Set[str]): set of strings to be created as mentions
        post (Post): post to be associated with the mentions

        Returns:
        mentions_array: created mentions
        """
        mentions_array = []
        for m in mentions:
            try:
                mentioned = User.objects.get(username=m[1:])
            except User.DoesNotExist:
                continue
            mention = Mention(user=mentioned, post=post)
            mention.save()
            mentions_array.append(mention.serialize())
        return mentions_array