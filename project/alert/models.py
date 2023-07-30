from django.utils import timezone

from django.db import models

from django.contrib.auth import get_user_model
User = get_user_model()

class Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=300, null=True)
    openChatURL = models.URLField(null=True)
    regTime = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)
