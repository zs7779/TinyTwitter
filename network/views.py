import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, QueryDict
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.views.decorators.cache import cache_control

from .models import User, Post, Follow, Like, HashTag, Mention


def index(request, path=None):
    return render(request, "frontend/index.html")


@require_GET
def current_user(request, path=None):
    # Get current user for frontend app
    # needed for notification
    if request.user.is_authenticated:
        data = request.GET
        count = int(data.get("count", 20))
        after = int(data.get("after", 0))
        user = request.user.get_user_information(path=path, after=after, count=count)
        return JsonResponse({"user": user})
    else:
        return JsonResponse({"user": {'authenticated': False}})


@require_GET
def posts_read(request, path=None, username=None):
    data = request.GET
    count = int(data.get("count", 20))
    after = int(data.get("after", 0))
    if username is not None:
        # Get posts of one user
        return Post.get_posts_by_user(username=username, requestor=request.user, count=count, after=after)
    elif path == 'home' and request.user.is_authenticated:
        # Get home page of logged-in user (posts of followees)
        return Post.get_posts(path='home', requestor=request.user, count=count, after=after)
    else:
        # Get all posts, also is home page of unlogged-in user
        return Post.get_posts(path='all', requestor=request.user, count=count, after=after)


@require_GET
def post_read(request, post_id, username=None):
    if username:
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({"error": "User does not exist"}, status=404)
    data = request.GET
    count = int(data.get("count", 20))
    after = int(data.get("after", 0))
    # Get one post
    return Post.get_post_by_id(post_id=post_id, requestor=request.user, count=count, after=after)


@require_GET
def hashtag_read(request, hashtag):
    data = request.GET
    count = int(data.get("count", 20))
    after = int(data.get("after", 0))
    return HashTag.get_hashtag_posts(hashtag=hashtag, requestor=request.user, count=count, after=after)


@require_GET
def profile_read(request, username):
    # Get user by username
    return User.get_user_by_username(username=username, requestor=request.user)


@login_required
@require_POST
def posts_write(request):
    data = json.loads(request.body)
    if data.get('text') is not None:
        # Handle new post
        return Post.create_post(text=data.get('text'), parent_id=data.get('parent_id'),
                                requestor=request.user)
    return JsonResponse({
        "error": "Bad request"
    }, status=400)


@login_required
@require_http_methods(["POST", "PATCH", "DELETE"])
def post_write(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"message": "Post does not exist"}, status=404)

    if request.method == "DELETE":
        # Delete post by authorized user, may need to be changed to access group related logic
        if post.author != request.user:
            return JsonResponse({"message": "Forbidden"}, status=403)
        post.delete()
        return JsonResponse({"message": "Delete succesful"}, status=200)

    data = json.loads(request.body)

    if request.method == "POST":
        if data.get('like') is not None:
            # Handles like/unlike
            return Like.create_like(like=data.get('like'), post=post, requestor=request.user)
        
        if data.get('text') is not None:
            # Handles new comments, which compare to normal posts, have root_post
            return Post.create_post(text=data.get('text'), parent_id=data.get('parent_id'),
                                    root_post=post, is_comment=True, requestor=request.user)

    return JsonResponse({
        "error": "Bad request"
    }, status=400)


@login_required
@require_http_methods(["POST", "PATCH"])
def profile_write(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User does not exist"}, status=404)

    data = json.loads(request.body)
    if request.method == "POST":
        if data.get('follow') is not None:
            # Handles follow/unfollow by authorized user
            if request.user == user:
                return JsonResponse({"error": "Unable to follow this user"}, status=403)
            return Follow.create_follow(follow=data.get('follow'), followee=user, requestor=request.user)

    if request.method == "PATCH":
        # Handle edit of user profile
        if request.user != user:
            return JsonResponse({"message": "Forbidden"}, status=403)
        if data.get('bio') is not None or data.get('avatar') is not None:
            return user.edit_profile(bio=data.get('bio'), avatar=data.get('avatar'))

    return JsonResponse({
        "error": "Bad request"
    }, status=400)


def posts_view(request, path=None, username=None):
    if request.method == "GET":
        return posts_read(request, path, username)
    else:
        return posts_write(request)


def post_view(request, post_id, username=None):
    if request.method == "GET":
        return post_read(request, post_id, username)
    else:
        return post_write(request, post_id)


def hashtag_view(request, hashtag):
    return hashtag_read(request, hashtag)


def profile_view(request, username):
    if request.method == "GET":
        return profile_read(request, username)
    else:
        return profile_write(request, username)
