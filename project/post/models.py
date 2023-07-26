from datetime import timezone
from enum import Enum

from django.db import models

from project.artist.models import Artist
from project.user.models import User

class Category(Enum):
    artist = '가수'
    free = '자유'

class Post(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(choices=[(status.value, status.name) for status in Category], default=Category.artist.value)

    title = models.CharField(max_length=50)
    contents = models.TextField(max_length=1000)
    regTime = models.DateTimeField(timezone.now())
