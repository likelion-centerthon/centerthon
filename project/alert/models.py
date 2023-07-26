from datetime import timezone

from django.db import models

from project.user.models import User


class Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=300)
    openChatURL = models.URLField(null=True)
    regTime = models.DateTimeField(timezone.now())
