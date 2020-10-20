import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, QueryDict
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.views.decorators.cache import cache_control

from .models import User, Post, Follow, Like, HashTag, Mention


def index(request, path=None):
    return render(request, "frontend/index.html")


@require_GET
def current_user(request):
    if request.user.is_authenticated:
        return JsonResponse({"user": request.user.serialize()})
    else:
        return JsonResponse({"user": {}})


@require_GET
def posts_read(request, path=None, username=None):
    data = request.GET
    if data.get("count") is not None and data.get("after") is not None:
        # todo: pages
        pass

    if username is not None:
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({"error": "User does not exist"}, status=404)
        posts = Post.objects.filter(author=user).order_by("-create_time")
        return JsonResponse({
            "posts": [post.serialize(request.user) for post in posts],
        }, safe=False)
    elif path is None:
        posts = Post.objects.all().order_by("-create_time")
        return JsonResponse({
            "posts": [post.serialize(request.user) for post in posts],
        }, safe=False)
    elif path == 'home' and request.user.is_authenticated:
        posts = Post.objects.filter(Q(author__followers__follower=request.user) | Q(author=request.user)).order_by("-create_time")
        return JsonResponse({
            "posts": [post.serialize(request.user) for post in posts],
        }, safe=False)
    else:
        return JsonResponse({"error": "Page does not exist"}, status=404)


@require_GET
def post_read(request, post_id, username=None):
    user = {}
    if username:
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({"error": "User does not exist"}, status=404)
        user = user.serialize(request.user)
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post does not exist"}, status=404)
    comments = [comment.serialize(user=request.user) for comment in post.comments.all()]
    return JsonResponse({
        "post": post.serialize(request.user),
        "comments": comments,
    }, safe=False)


@require_GET
def profile_read(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User does not exist"}, status=404)
    return JsonResponse({
        "user": user.serialize(request.user),
    })


@login_required
@require_POST
def posts_write(request):
    data = json.loads(request.body)
    if data.get('text') is not None:
        post = Post(author=request.user, text=data['text'])
        try:
            post.full_clean()
        except ValidationError as e:
            print(e)
            return JsonResponse({"message": "Post body is illegal"}, status=400, safe=False)
        post.save()
        return JsonResponse({
            "message": "Post successful",
            "post": post.serialize(request.user),
        }, status=201)
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
        if post.author != request.user:
            return JsonResponse({"message": "Forbidden"}, status=403)
        post.delete()
        return JsonResponse({"message": "Delete succesful"}, status=200)

    data = json.loads(request.body)

    if request.method == "POST":
        if data.get('like') is not None:
            if data['like']:
                try:
                    like = Like.objects.get(user=request.user, post=post)
                except Like.DoesNotExist:
                    like = Like(user=request.user, post=post)
                    like.save()
            else:
                likes = Like.objects.filter(user=request.user, post=post)
                for like in likes:
                    like.delete()
            post.update_counts().save()
            return JsonResponse({"message": "Like succesful"}, status=200)
        
        if data.get('text') is not None:
            try:
                parent = Post.objects.get(id=data.get('parent_id'))
            except Post.DoesNotExist:
                return JsonResponse({"message": "Post does not exist"}, status=404)
            comment = Post(author=request.user, text=data['text'], parent=parent, is_comment=True, root_post=post)
            try:
                comment.full_clean()
            except ValidationError as e:
                print(e)
                return JsonResponse({"message": "Comment body is illegal"}, status=400, safe=False)
            comment.save()
            return JsonResponse({
                "message": "Comment succesful",
                "comment": comment.serialize(request.user),
            }, status=201)

    if request.method == "PATCH":
        if data.get('text') is not None:
            if post.author == request.user and data.get('text') is not None:
                post.text = data['text']
                try:
                    post.full_clean()
                except ValidationError as e:
                    print(e)
                    return JsonResponse({"message": "Post body is illegal"}, status=400, safe=False)
                post.save()
                return JsonResponse({"message": "Like succesful"}, status=200)
            return JsonResponse({"message": "Forbidden"}, status=403)

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

    if request.method == "POST":
        data = json.loads(request.body)
        if data.get('follow') is not None:
            if data['follow'] and request.user != user:
                try:
                    follow = Follow.objects.get(user=user, follower=request.user)
                except Follow.DoesNotExist:
                    follow = Follow(user=user, follower=request.user)
                    follow.save()
            else:
                follows = Follow.objects.filter(user=user, follower=request.user)
                for follow in follows:
                    follow.delete()
            request.user.update_counts().save()
            user.update_counts().save()
            return JsonResponse({"message": "Follow succesful"}, status=200)

    if request.method == "PATCH":
        # todo: edit pofile
        if request.user == user:
            pass

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


def profile_view(request, username):
    if request.method == "GET":
        return profile_read(request, username)
    else:
        return profile_write(request, username)
