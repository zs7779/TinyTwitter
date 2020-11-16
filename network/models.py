import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models, DatabaseError, transaction
from django.db.models import Count, Q, signals
from django.dispatch import receiver
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.templatetags.static import static

from .utils import isHashTag, isMention, presign_s3_post, s3_delete


MAX_LENGTH = 140
DETAIL_SHORT = 0
DETAIL_MEDIUM = 1
DETAIL_LONG = 2
DETAIL_FULL = 3


class User(AbstractUser):
    bio = models.CharField(max_length=MAX_LENGTH, default="")
    avatar_url = models.URLField(null=True, blank=True)
    last_visit = models.DateTimeField(null=True, blank=True)

    def serialize(self, requestor=None, detail=DETAIL_FULL):
        result = {
            "id": self.id,
            "username": self.username,
            "avatar": static('frontend/avatar_placeholder.jpg') if self.avatar_url is None else self.avatar_url,
        }
        if detail == DETAIL_SHORT:
            return result
        result.update({
            "bio": self.bio,
            "following_count": self.following.all().count(),
            "follower_count": self.followers.all().count(),
            "following": self.followers.filter(user__id=self.id, follower__id=requestor.id).count() > 0,
            "followed": self.followers.filter(user__id=requestor.id, follower__id=self.id).count() > 0,
            "owner": self == requestor,
        })
        if detail == DETAIL_FULL:
            return result

    def edit_profile(self, bio=None, avatar=None):
        self.bio = self.bio if bio is None else bio

        if avatar is not None:
            if "amazonaws.com" in self.avatar_url:
                media_key = self.avatar_url.split('amazonaws.com/')[-1]
                response = s3_delete(key=media_key, bucket='project-tt-bucket')
            self.avatar_url = avatar

        try:
            self.full_clean()
        except ValidationError as e:
            # print(e)
            return JsonResponse({"error": "Profile body is illegal"}, status=400, safe=False)
        self.save()
        return JsonResponse({"message": "Edit succesful"}, status=200)

    def get_user_information(self, path=None, after=0, count=20, order_by='-create_time'):
        last_visit = self.date_joined if self.last_visit is None else self.last_visit
        user = self.serialize(self)
        user['authenticated'] = True
        posts_ids = self.posts.values('id')
        if path is None:
            user['notifications'] = Post.objects.filter(Q(mentions__user=self) | Q(root_post__id__in=posts_ids) | Q(parent__id__in=posts_ids), create_time__gt=last_visit).count()
        else:
            user['notifications'] = 0
            if path == "mentions":
                user['notices'] = [m.post.serialize(self, detail=DETAIL_LONG) for m in self.mentions.order_by(order_by)[after:after+count]]
            if path == "replies":
                user['notices'] = [p.serialize(self, detail=DETAIL_LONG) for p in Post.objects.filter(Q(root_post__id__in=posts_ids) | Q(parent__id__in=posts_ids)).order_by(order_by)[after:after+count]]
            self.last_visit = datetime.datetime.now()
            self.save()
        return user

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
            "medias": [media.serialize() for media in self.medias.all()],
            "create_time": self.create_time.strftime("%I:%M %p %b %d %Y"),
            "is_comment": self.is_comment,
            "mentions": self.get_mentions(),
            "comment_count": self.children.filter(is_comment=True).count() if self.is_comment else self.comments.all().count(),
            "repost_count": self.children.filter(is_comment=False).count(),
            "like_count": self.likes.all().count(),
        })
        if detail == DETAIL_MEDIUM:
            return result
        result.update({
            "commented": self.children.filter(is_comment=True, author__id=user.id).count() if self.is_comment else self.comments.filter(author__id=user.id).count(),
            "reposted": self.children.filter(is_comment=False, author__id=user.id).count(),
            "liked": self.likes.filter(user__id=user.id).count(),
            "owner": self.author == user,
        })
        if detail == DETAIL_LONG:
            return result
        result.update({
            "parent": self.parent.serialize(detail=DETAIL_LONG, user=user) if self.parent is not None else None,
            "root_post": self.root_post.serialize(detail=DETAIL_LONG, user=user) if self.is_comment else None,
        })
        if detail == DETAIL_FULL:  
            return result
    
    def get_trends(requestor):
        # From all posts cuz we don't have enough data, probably should be truncated by time
        top_posts = Post.objects.filter(~Q(author=requestor)) \
                                .annotate(hotness=Count("likes")+Count("children")+Count("comments")) \
                                .order_by("-hotness")[:10]
        top_users = set([p.author for p in top_posts if p.author.followers.filter(user__id=p.author.id, follower__id=requestor.id).count() == 0])
        top_hashtags = HashTag.objects.annotate(hotness=Count("posts")) \
                                      .order_by("-hotness")[:3]
        return {
            'users': [user.serialize(requestor=requestor, detail=DETAIL_FULL) for user in top_users][:2],
            'posts': [post.serialize(detail=DETAIL_MEDIUM) for post in top_posts[:2]],
            'hashtags': [hashtag.serialize() for hashtag in top_hashtags[:3]],
        }

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

    def create_post(text, media_url, parent_id, requestor, root_post=None, is_comment=False):
        """
        Returns response of POST new post request, used to create new post or comment

        Parameters:
        text (str): text content of the new post
        media (str): url of uploaded media
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

        with transaction.atomic():
            post = Post(author=requestor, text=text, parent=parent_post,
                        root_post=root_post, is_comment=is_comment)
            try:
                post.full_clean()
            except ValidationError as e:
                return JsonResponse({"error": "Post body is illegal"}, status=400, safe=False)
            post.save()

            if media_url is not None:
                media = Media(user=requestor, post=post, media_url=media_url, media_type='IMG')
                try:
                    media.full_clean()
                except ValidationError as e:
                    print(e)
                    return JsonResponse({"error": "Post body is illegal"}, status=400, safe=False)
                media.save()

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
            'id': self.id,
            'text': self.text,
            'num_posts': self.posts.count(),
        }

    def get_hashtag_posts(hashtag, requestor, count=20, after=0, order_by="-create_time"):
        try:
            tag = HashTag.objects.get(text=hashtag.lower())
        except HashTag.DoesNotExist:
            return JsonResponse({"error": "Hashtag does not exist"}, status=404)
        tags = tag.posts.order_by(order_by)[after:after+count]
        return JsonResponse({
            "posts": [post_tag.post.serialize(requestor) for post_tag in tags],
        }, safe=False)
        

class PostTag(models.Model):
    tag = models.ForeignKey("HashTag", on_delete=models.RESTRICT, related_name="posts")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="hashtags")
    create_time = models.DateTimeField(auto_now_add=True)

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
            "post": self.post.serialize(detail=DETAIL_MEDIUM),
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

class Media(models.Model):
    MEDIA_TYPES = [
        ('IMG', 'Photo'),
        ('GIF', 'Animated Picture'),
        ('VID', 'Video'),
    ]
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="medias")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="medias")
    media_url = models.URLField()
    media_type = models.CharField(
        max_length=3,
        choices=MEDIA_TYPES,
        default='IMG',
    )

    def serialize(self):
        return {
            'media_url': self.media_url
        }

@receiver(signals.post_delete, sender=Media)
def delete_media(sender, instance, *args, **kwargs):
    if "amazonaws.com" not in instance.media_url:
        return

    media_key = instance.media_url.split('amazonaws.com/')[-1]
    response = s3_delete(key=media_key, bucket='project-tt-bucket')
    