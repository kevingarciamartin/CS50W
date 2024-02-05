
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new"),
    path("profile/<str:user>", views.profile_page, name="profile"),
    path("profile/<str:user>/follow", views.follow, name="follow"),
    path("profile/<str:user>/unfollow", views.unfollow, name="unfollow"),
    path("following", views.following, name="following"),
    
    # API Routes
    path("posts/<int:post_id>", views.edit_post, name="edit_post"),
]
