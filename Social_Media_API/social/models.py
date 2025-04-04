from django.db import models

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils import timezone
User = get_user_model()


class Post(models.Model):
    id = models.AutoField(primary_key=True)  
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    video = models.FileField(upload_to='posts/videos/', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True) 
    likes_count = models.PositiveIntegerField(default=0) 
    comments_count = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)  

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Post by {self.user.username}: {self.content[:50]}..."


class Comment(models.Model):
    id = models.AutoField(primary_key=True)  
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')  
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments') 
    content = models.TextField()  
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.user.username}: {self.content[:50]}..."
    