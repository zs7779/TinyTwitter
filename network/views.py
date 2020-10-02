import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post


def index(request):
    return render(request, "network/index.html")


def posts_endpoint(request):
    posts = Post.objects.all().order_by("-post_time")
    return JsonResponse([post.serialize() for post in posts], safe=False)


def post_endpoint(request, post_id=-1):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"message": "Please log in or register"}, status=401)
        post_text = json.loads(request.body)['newPostText']
        post = Post(author=request.user, text=post_text)
        post.save()
        return JsonResponse({"message": "Post succesful"}, status=201)

    if request.method == "GET":
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post does not exist"}, status=404)
        return JsonResponse(post.serialize())


def user_endpoint(request, user_id=None):
    pass


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
