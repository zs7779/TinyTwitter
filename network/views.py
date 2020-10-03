import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, QueryDict
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post


def index(request):
    return render(request, "network/index.html")


def posts_endpoint(request, post_id=None):
    if request.method == "GET":
        data = request.GET
        print(data.get("count"), data.get("after"))
        if post_id is not None:
            try:
                post = Post.objects.get(id=post_id)
            except Post.DoesNotExist:
                return JsonResponse({"error": "Post does not exist"}, status=404)
            return JsonResponse(post.serialize())

        if data.get("count") is not None and data.get("after") is not None:
            pass

        posts = Post.objects.all().order_by("-post_time")
        user = request.user if request.user.is_authenticated else None
        return JsonResponse([post.serialize(user) for post in posts], safe=False)

    return JsonResponse({
        "error": "Request unknown"
    }, status=400)


@login_required
def post_endpoint(request, post_id=None):
    if request.method == "POST":
        data = json.loads(request.body)
        if data.get('newPostText') is not None and len(data['newPostText']) > 0:
            post_text = data['newPostText']
            post = Post(author=request.user, text=post_text)
            post.save()
            return JsonResponse({"message": "Post successful"}, status=201)
        else:
            return JsonResponse({"message": "Empty post"}, status=400)

    if post_id is None:
        return JsonResponse({"message": "Post ID required"}, status=400)
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"message": "Post does not exist"}, status=404)

    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get('like') is not None:
            if data['like']:
                post.likes.add(request.user)
            else:
                post.likes.remove(request.user)
            post.save()
            return JsonResponse({"message": "Like succesful"}, status=200)
        if data.get('newPostText') is not None:
            if post.author != request.user:
                return JsonResponse({"message": "Not authorized"}, status=401)
            pass

    if request.method == "DELETE":
        if post.author != request.user:
            return JsonResponse({"message": "Not authorized"}, status=401)
        post.delete()
        return JsonResponse({"message": "Delete succesful"}, status=200)

    return JsonResponse({
        "error": "Bad request"
    }, status=400)


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
