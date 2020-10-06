import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, QueryDict
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Follow, Comment, Like, HashTag, Mention


def index(request):
    return render(request, "network/index.html")


@require_GET
def current_user(request):
    if request.user.is_authenticated:
        return JsonResponse({"user": request.user.snippet()})
    else:
        return JsonResponse({"user": {}})


@require_GET
def posts_view(request):
    if not request.GET.get("json"):
        return render(request, "network/index.html")

    data = request.GET
    if data.get("count") is not None and data.get("after") is not None:
        # todo: pages
        pass

    posts = Post.objects.all().order_by("-create_time")
    return JsonResponse({
        "user": {},
        "posts": [post.serialize(request.user) for post in posts],
    }, safe=False)


@require_GET
def post_view(request, post_id):
    if not request.GET.get("json"):
        return render(request, "network/index.html")

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post does not exist"}, status=404)
    return JsonResponse(post.serialize(request.user))


@require_GET
def profile_view(request, user_id):
    if not request.GET.get("json"):
        return render(request, "network/index.html")

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User does not exist"}, status=404)
    posts = Post.objects.filter(author=user).order_by("-create_time")
    return JsonResponse({
        "user": user.serialize(request.user),
        "posts": [post.serialize(request.user) for post in posts],
    })


@login_required
@require_POST
def posts_endpoint(request):
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
def post_endpoint(request, post_id):
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
            # todo: edit post
            if post.author != request.user:
                pass
            return JsonResponse({"message": "Not authorized"}, status=401)

    if request.method == "DELETE":
        if post.author != request.user:
            return JsonResponse({"message": "Not authorized"}, status=401)
        post.delete()
        return JsonResponse({"message": "Delete succesful"}, status=200)

    return JsonResponse({
        "error": "Bad request"
    }, status=400)


@login_required
@require_http_methods(["POST", "PUT"])
def profile_endpoint(request, user_id):
    try:
        user = User.objects.get(id=user_id)
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


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
