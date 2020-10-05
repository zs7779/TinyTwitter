
from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("current_user/", views.current_user, name="current_user"),
    path("posts/", views.posts_view, name="posts"),
    re_path(r"^user/(?P<user_id>[0-9]{1,50})$", views.profile_view, name="user"),
    re_path(r"^post/(?P<post_id>[0-9]{1,50})$", views.post_view, name="post"),
    path("posts_new/", views.posts_endpoint, name="posts_new"),
    re_path(r"^user_mod/(?P<user_id>[0-9]{1,50})$", views.profile_endpoint, name="user_mod"),
    re_path(r"^post_mod/(?P<post_id>[0-9]{1,50})$", views.post_endpoint, name="post_mod"),
]
