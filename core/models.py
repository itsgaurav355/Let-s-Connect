from django.db import models
from django.contrib.auth import get_user_model
import uuid 
from datetime import datetime
from django.db.models import Q

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank = True)
    profileimg = models.ImageField(upload_to = 'profile_image',default='blank_user.png')
    location = models.CharField(max_length=100 , blank = True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key= True,default= uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    noOfLikes = models.IntegerField(default=0)

    def __str__(self):
        return self.user

class LikePost(models.Model):
    post_id = models.CharField(max_length = 500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class Followers(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user

class Review(models.Model):
    name = models.TextField(max_length = 500)
    email= models.TextField(max_length =100)
    desc = models.TextField()

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ('timestamp',)

    def __str__(self):
        return f'{self.sender} to {self.receiver}: {self.content}'
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}: {self.message}'
