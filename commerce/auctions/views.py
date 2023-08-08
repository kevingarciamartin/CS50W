from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Category, Bid, Comment


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(isActive=True),
        "categories": Category.objects.all()
    })

def category_index(request):
    category = request.POST["category"]
    if category == "all":
        return HttpResponseRedirect(reverse("index"))
    else:
        category = Category.objects.get(category_name=category)
        return render(request, "auctions/index.html", {
            "listings": Listing.objects.filter(isActive=True, category=category),
            "categories": Category.objects.all()
        })
        
def category_watchlist(request):
    category = request.POST["category"]
    if category == "all":
        return HttpResponseRedirect(reverse("watchlist"))
    else:
        category = Category.objects.get(category_name=category)
        listings = Listing.objects.filter(category=category, watchlist=request.user)
        return render(request, "auctions/watchlist.html", {
            "watchlist": listings,
            "categories": Category.objects.all()
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
def create_listing(request):
    if request.method == "POST":
        item = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        image = request.POST["image"]
        category = request.POST["category"]
        category = Category.objects.get(category_name=category)
        
        new_listing = Listing(
            item=item,
            listing_price=float(price),
            description=description,
            image=image,
            lister=request.user,
            category=category
        )
        new_listing.save()
        return HttpResponseRedirect(reverse("index"))
        
    return render(request, "auctions/create.html", {
        "categories": Category.objects.all()
    })
    
def close_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.isActive = False
    listing.save()
    return HttpResponseRedirect(reverse("listing", args=(listing_id, )))
    

def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing_in_watchlist = request.user in listing.watchlist.all()
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "listing_in_watchlist": listing_in_watchlist,
        "comments": Comment.objects.filter(listing=listing)
    })
    
def add_to_watchlist(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        user = request.user
        listing.watchlist.add(user)
        user.number_of_watchlist += 1
        user.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id, )))

def remove_from_watchlist(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        user = request.user
        listing.watchlist.remove(user)
        user.number_of_watchlist -= 1
        user.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id, )))
    
def watchlist(request):
    user = request.user
    watchlist = user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist,
        "categories": Category.objects.all()
    })
    
def bid(request, listing_id):
    if request.method == "POST":
        bid = request.POST["bid"]
        listing = Listing.objects.get(pk=listing_id)
        if listing.number_of_bids == 0:
            is_sufficiently_large = True if float(bid) >= listing.listing_price else False
        else:
            is_sufficiently_large = True if float(bid) > listing.highest_bid.bid else False
            
        if is_sufficiently_large:
            bid = Bid(bid=float(bid), bidder=request.user)
            bid.save()
            listing.highest_bid = bid
            listing.number_of_bids += 1
            listing.save()
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "listing_in_watchlist": request.user in listing.watchlist.all(),
                "comments": Comment.objects.filter(listing=listing),
                "message": "Bid was successful! You are now the highest bidder.",
                "bid_success": True
            })
        else:
            if listing.number_of_bids == 0:
                message = "Bid was denied. Please enter a value equal to or greater than the listing price."
            else:
                message = "Bid was denied. Please enter a value greater than the current bid."
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "listing_in_watchlist": request.user in listing.watchlist.all(),
                "comments": Comment.objects.filter(listing=listing),
                "message": message,
                "bid_success": False
            })
            
def comment(request, listing_id):
    comment = request.POST["comment"]
    listing = Listing.objects.get(pk=listing_id)
    new_comment = Comment(comment=comment, commenter=request.user, listing=listing)
    new_comment.save()
    return HttpResponseRedirect(reverse("listing", args=(listing_id, )))
        