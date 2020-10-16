from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    re_path(r"^(?P<username>\w{1,50})/$", views.index),
    re_path(r"^(?P<username>\w{1,50})/(?P<post_id>[0-9]{1,50})$", views.index),
    re_path(r"^(?P<path>\w*)$", views.index, name="index"),
]