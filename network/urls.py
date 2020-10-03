
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("posts/", views.posts_endpoint, name="posts"),
    path("post/", views.post_endpoint, name="post"),
    path("post/<int:post_id>", views.post_endpoint, name="post_id"),
    path("user/", views.user_endpoint, name="user"),
    path("user/<int:user_id>", views.user_endpoint, name="user_id"),
]
