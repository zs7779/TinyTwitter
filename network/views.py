import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, QueryDict
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Post, Follow, Comment, Like, HashTag, Mention


def index(request, path=''):
    return render(request, "network/index.html")


@require_GET
def current_user(request):
    if request.user.is_authenticated:
        return JsonResponse({"user": request.user.snippet()})
    else:
        return JsonResponse({"user": {}})


@require_GET
def posts_read(request, path=""):
    if not request.GET.get("json"):
        return render(request, "network/index.html")

    data = request.GET
    if data.get("count") is not None and data.get("after") is not None:
        # todo: pages
        pass

    if path == "all" or path == "home" and not request.user.is_authenticated:
        posts = Post.objects.all().order_by("-create_time")
        return JsonResponse({
            "user": {},
            "posts": [post.serialize(request.user) for post in posts],
        }, safe=False)
    elif path == "home" and request.user.is_authenticated:
        posts = Post.objects.filter(Q(author__followers__follower=request.user) | Q(author=request.user)).order_by("-create_time")
        return JsonResponse({
            "user": {},
            "posts": [post.serialize(request.user) for post in posts],
        }, safe=False)
    else:
        # todo: query for username, but lookout for conflict with keywords
        posts = Post.objects.all().order_by("-create_time")
        return JsonResponse({
            "user": {},
            "posts": [post.serialize(request.user) for post in posts],
        }, safe=False)


@require_GET
def post_read(request, post_id, username=None):
    if not request.GET.get("json"):
        return render(request, "network/index.html")

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post does not exist"}, status=404)
    return JsonResponse(post.serialize(request.user))


@require_GET
def profile_read(request, username):
    if not request.GET.get("json"):
        return render(request, "network/index.html")

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User does not exist"}, status=404)
    posts = Post.objects.filter(author=user).order_by("-create_time")
    return JsonResponse({
        "user": user.serialize(request.user),
        "posts": [post.serialize(request.user) for post in posts],
    })


@login_required
@require_POST
def posts_write(request):
    data = json.loads(request.body)
    if data.get('isComment') is True:
        # todo: comment
        pass

    if data.get('postText') is not None:
        post = Post(author=request.user, text=data['postText'])
        if post.is_valid():
            post.save()
            return JsonResponse({"message": "Post successful"}, status=201)
    return JsonResponse({"message": "Post body is illegal"}, status=400)


@login_required
@require_http_methods(["PUT", "DELETE"])
def post_write(request, post_id, username=None):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"message": "Post does not exist"}, status=404)

    if request.method == "PUT":
        data = json.loads(request.body)
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

        if data.get('postText') is not None:
            if post.author == request.user and data.get('postText') is not None:
                post.text = data['postText']
                post.save()
                return JsonResponse({"message": "Like succesful"}, status=200)
            return JsonResponse({"message": "Forbidden"}, status=403)

    if request.method == "DELETE":
        if post.author != request.user:
            return JsonResponse({"message": "Forbidden"}, status=403)
        post.delete()
        return JsonResponse({"message": "Delete succesful"}, status=200)

    return JsonResponse({
        "error": "Bad request"
    }, status=400)


@login_required
@require_http_methods(["POST", "PUT"])
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

    if request.method == "PUT":
        # todo: edit pofile
        if request.user == user:
            pass

    return JsonResponse({
        "error": "Bad request"
    }, status=400)


def posts_view(request, path=''):
    if request.method == "GET":
        return posts_read(request, path)
    else:
        return posts_write(request)


def post_view(request, post_id, username=None):
    if request.method == "GET":
        return post_read(request, post_id, username)
    else:
        return post_write(request, post_id, username)


def profile_view(request, username):
    if request.method == "GET":
        return profile_read(request, username)
    else:
        return profile_write(request, username)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return redirect("/")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return redirect("/")
    else:
        return render(request, "network/register.html")
