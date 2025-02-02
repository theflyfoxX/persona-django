from django.db import models
from django.contrib.auth.models import User
from app.models.post_model import Post

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who liked the post
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')  # Post being liked

    class Meta:
        unique_together = ('user', 'post')  # Ensure one like per user per post

    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"
