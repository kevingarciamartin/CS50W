from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)
    
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "followers": self.followers,
            "following": self.following,
        }
            
    def __str__(self):
        return self.username


class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    content = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    
    def serialize(self):
        return {
            "id": self.id,
            "poster": self.poster,
            "content": self.content,
            "timestamp": self.timestamp.strftime('%d %b %Y %H:%M:%S'),
            "likes": self.likes,
        }
    
    def __str__(self):
        return f"Post {self.id} made by {self.poster} on {self.timestamp.strftime('%d %b %Y %H:%M:%S')}"
 
    
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_following")
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_followed")
    
    def __str__(self):
        return f"{self.follower} followed {self.followed}"
