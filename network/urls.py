
from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    re_path(r"^posts/$", views.posts_endpoint, name="posts"),
    path("user/", views.user_endpoint, name="user"),
    re_path(r"^user/(?P<user_id>[0-9]{1,20})$", views.user_endpoint, name="user_id"),
    path("post/", views.post_endpoint, name="post"),
    re_path(r"^post/(?P<post_id>[0-9]{1,20})$", views.post_endpoint, name="post_id"),
]
