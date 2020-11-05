
from django.urls import path, re_path

from . import views

urlpatterns = [
    path("api/current_user/", views.current_user, name="current_user"),
    path("api/posts/", views.posts_view, name="posts_all"),
    re_path(r"^api/posts/(?P<path>[a-zA-Z]{1,4})$", views.posts_view, name="posts"),
    re_path(r"^api/posts/(?P<post_id>[0-9]{1,50})$", views.post_view, name="post"),
    re_path(r"^api/users/(?P<username>\w{1,50})$", views.profile_view, name="user"),
    re_path(r"^api/users/(?P<username>\w{1,50})/posts/$", views.posts_view, name="user_posts"),
    re_path(r"^api/users/(?P<username>\w{1,50})/posts/(?P<post_id>[0-9]{1,50})$", views.post_view, name="user_post"),
    re_path(r"^api/hashtags/(?P<hashtag>\w{1,140})$", views.hashtag_view, name="hashtag"),
]
