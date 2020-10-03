
from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    re_path(r"^posts/$", views.posts_endpoint, name="posts"),
    re_path(r"^user/(?P<user_id>\w{1,50})/$", views.user_endpoint, name="user"),
    path("post/", views.post_endpoint, name="post"),
]
