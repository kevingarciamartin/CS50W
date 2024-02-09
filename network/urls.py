
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
    path("posts/edit/<int:post_id>", views.edit_post, name="edit_post"),
    path("posts/is_liked/<int:post_id>", views.is_liked, name="is_liked"),
    path("posts/like/<int:post_id>", views.like, name="like"),
    path("posts/unlike/<int:post_id>", views.unlike, name="unlike"),
    path("posts/get_likes/<int:post_id>", views.get_likes, name="get_likes"),
]
