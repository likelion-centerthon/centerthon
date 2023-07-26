from datetime import timezone

from django.db import models

from project.post.models import Post
from project.user.models import User


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    contents = models.TextField(max_length=200)
    regTime = models.DateTimeField(timezone.now())
