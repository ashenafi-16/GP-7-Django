from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Post(models.Model):
    id = models.AutoField(primary_key=True)  
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')  # Related to the user
    content = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Post by {self.user.username}: {self.content[:50]}..."

class Comment(models.Model):
    id = models.AutoField(primary_key=True)  
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_comments')  
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='user_comments') 
    content = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.user.username}: {self.content[:50]}..."

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
    
    def __str__(self):
        return f"{self.user.username} liked Post {self.post.id}"
    
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')  # prevent duplicate follows

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"