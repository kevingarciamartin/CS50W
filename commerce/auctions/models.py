from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=64, blank=True, null=True)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    number_of_watchlist = models.IntegerField(default=0)
    
    def __str__(self):
        return self.username
    
class Category(models.Model):
    category_name = models.CharField(max_length=64)
    image = models.CharField(max_length=500, null=True)
    
    def __str__(self):
        return self.category_name

class Bid(models.Model):
    bid = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="bidder")
    
    def __str__(self):
        return f"{self.bidder} bid ${self.bid}"
    
class Listing(models.Model):
    
    item = models.CharField(max_length=64)
    listing_price = models.DecimalField(max_digits=20, decimal_places=2)
    highest_bid = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="highest_bid")
    description = models.CharField(max_length=500)
    image = models.CharField(max_length=500)
    lister = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist")
    number_of_bids = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    isActive = models.BooleanField(default=True)
    
    def __str__(self):
        return self.item
    
    def imageDefault():
        return "https://media.istockphoto.com/id/917901978/photo/gavel-on-auction-word.jpg?s=612x612&w=0&k=20&c=e5mnLUG2UEg6y8zfO1zc7Gi4Ed8PEEeV3eGeYOKxKBI="

class Comment(models.Model):
    comment = models.CharField(max_length=200, null=True)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="commenter")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, related_name="listing")
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return f"{self.commenter} comment on {self.listing}"
