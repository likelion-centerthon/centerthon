from enum import Enum
from django.utils import timezone

from django.db import models

from artist.models import Artist
from django.contrib.auth import get_user_model
User = get_user_model()
class Category(Enum):
    artist = '가수'
    free = '자유'

class Post(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=10, choices=[(status.value, status.name) for status in Category], default=Category.artist.value)

    title = models.CharField(max_length=50)
    contents = models.TextField(max_length=1000)
    regTime = models.DateTimeField(timezone.now())

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    contents = models.TextField(max_length=200)
    regTime = models.DateTimeField(timezone.now())
