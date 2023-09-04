from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    content = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    number_of_likes = models.IntegerField(default=0)
