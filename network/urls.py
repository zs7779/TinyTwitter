
from django.urls import path, re_path

from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("current_user/", views.current_user, name="current_user"),
    re_path(r"^posts/(?P<path>[a-zA-Z]{0,4})$", views.posts_view, name="posts"),
    re_path(r"^posts/(?P<post_id>[0-9]{1,50})$", views.post_view, name="post"),
    re_path(r"^users/(?P<username>\w{1,50})$", views.profile_view, name="user"),
    re_path(r"^(?P<path>\w*)$", views.index, name="index"),
]
