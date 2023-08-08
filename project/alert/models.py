from django.db import models
from artist.models import Artist
from user.models import User


class Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    message = models.CharField(max_length=300, null=True)
    openChatURL = models.URLField(null=True)
    regTime = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.user.userName