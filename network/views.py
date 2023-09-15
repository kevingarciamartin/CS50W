from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Follow


def index(request):
    posts = Post.objects.all().order_by("-timestamp")
    return render(request, "network/index.html", {
        "posts": posts
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def new_post(request):
    poster = request.user
    content = request.POST["content"]
    
    new_post = Post(
        poster=poster,
        content=content
    )
    
    new_post.save()
    
    return HttpResponseRedirect(reverse("index"))


def profile_page(request, user):
    user = User.objects.get(username=user)
    posts = Post.objects.filter(poster=user).order_by("-timestamp")
    following = Follow.objects.filter(follower=user)
    followers = Follow.objects.filter(followed=user)
    
    try:
        check_follow = followers.filter(follower=User.objects.get(pk=request.user.id))
        if len(check_follow) != 0:
            is_following = True
        else:
            is_following = False
    except:
        is_following = False
    
    return render(request, "network/profile.html", {
        "profile_user": user,
        "posts": posts,
        "following": following,
        "followers": followers,
        "isFollowing": is_following
    })
    
    
def follow(request, user):
    follower = User.objects.get(pk=request.user.id)
    followed = User.objects.get(username=request.POST["followed"])
    
    follow = Follow(follower=follower, followed=followed)
    
    follow.save()
    
    return HttpResponseRedirect(reverse("profile", args=[request.POST["followed"]]))
    
    
def unfollow(request, user):
    follower = User.objects.get(pk=request.user.id)
    followed = User.objects.get(username=request.POST["followed"])
    
    follow = Follow.objects.get(follower=follower, followed=followed)
    
    follow.delete()
    
    return HttpResponseRedirect(reverse("profile", args=[request.POST["followed"]]))


def following(request):
    user = User.objects.get(pk=request.user.id)
    following = Follow.objects.filter(follower=user)
    all_posts = Post.objects.all().order_by("-timestamp")
    
    following_posts = []
    
    for post in all_posts:
        for person in following:
            if person.followed == post.poster:
                following_posts.append(post) 
        
    return render(request, "network/following.html", {
        "posts": following_posts
    })