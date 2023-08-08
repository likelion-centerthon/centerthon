from django.utils import timezone

from django.db import models

from artist.models import Artist
from user.models import User


class UserWorking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    startDay = models.DateField(null=True)
    likeDays = models.IntegerField(default=0)
    postRecord = models.IntegerField(default=0)
    commentRecord = models.IntegerField(default=0)
    meetingHost = models.IntegerField(default=0)
    meetingGuest = models.IntegerField(default=0)
    supportHost = models.IntegerField(default=0)
    supportGuest = models.IntegerField(default=0)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.user.userName