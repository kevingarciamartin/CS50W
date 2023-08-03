from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image


class User(AbstractUser):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    
    def __str__(self):
        return self.username
    
class Category(models.Model):
    category_name = models.CharField(max_length=64)
    
    def __str__(self):
        return self.category_name
    
class Listing(models.Model):
    item = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.CharField(max_length=500)
    image = models.CharField(max_length=500, null=True)
    lister = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watchlist")
    timestamp = models.DateTimeField(auto_now_add=True)
    isActive = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.item}: ${self.price}"

class Bid(models.Model):
    highest_bid = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, related_name="highest_bid")
    highest_bidder = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="highest_bidder")
    number_of_bids = models.IntegerField(default=0)

class Comment(models.Model):
    pass
