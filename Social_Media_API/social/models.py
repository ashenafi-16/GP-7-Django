from django.db import models
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
    updated_at = models.DateTimeField(auto_now=True)  
    likes_count = models.PositiveIntegerField(default=0)  
    comments_count = models.PositiveIntegerField(default=0)  

    class Meta:
        ordering = ['-created_at']  # Posts will be ordered by creation date in descending order

    def __str__(self):
        return f"Post by {self.user.username}: {self.content[:50]}..."

    def update_like_count(self):
        """Update likes count for the post."""
        self.likes_count = self.likes.count()  # Automatically updates count based on related Like objects
        self.save()

    def update_comment_count(self):
        """Update comments count for the post."""
        self.comments_count = self.comments.count()  # Automatically updates count based on related Comment objects
        self.save()


class Comment(models.Model):
    id = models.AutoField(primary_key=True)  
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')  
    content = models.TextField()  
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)  # Allow nested comments
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']  # Comments will be ordered by creation date in ascending order

    def __str__(self):
        return f"Comment by {self.user.username}: {self.content[:50]}..."

    def save(self, *args, **kwargs):
        """Override save to update the comment count of the post."""
        super().save(*args, **kwargs)  # Save the comment
        self.post.update_comment_count()  # Update the comment count of the related post


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # Prevent duplicate likes by the same user for the same post

    def __str__(self):
        return f"{self.user.username} liked Post {self.post.id}"

    def save(self, *args, **kwargs):
        """Override save to update the like count of the post."""
        super().save(*args, **kwargs)  # Save the like
        self.post.update_like_count()  # Update the like count of the related post


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')  # Prevent duplicate follows between the same users

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
