
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("posts/", views.posts_view, name="posts"),
    path("post/", views.post_view, name="post"),
    path("user/", views.user_view, name="user"),
]
