from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    # image = models.ImageField()
    item = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.item}: ${self.price}"
    

class Bid(models.Model):
    number_of_bids = models.IntegerField()

class Comment(models.Model):
    pass
