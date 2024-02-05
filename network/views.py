from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

import json

from .models import User, Post, Follow


def index(request):
    posts = Post.objects.all().order_by("-timestamp")
    
    # Pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
        
    return render(request, "network/index.html", {
        "posts": page_obj
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
    
    # Pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
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
        "posts": page_obj,
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
                
     # Pagination
    paginator = Paginator(following_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
        
    return render(request, "network/following.html", {
        "posts": page_obj
    })
    
def edit_post(request, post_id):
    
    # Query for requested post
    try:
        post = Post.objects.get(poster=request.user, pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    # Get new content
    data = json.loads(request.body)
    new_content = data.get('newContent', '')
    
    # Update post
    post.content = new_content
    post.save()
    
    return JsonResponse({'updated': True, 'data': data}, status=200)
    