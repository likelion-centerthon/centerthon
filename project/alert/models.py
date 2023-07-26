from django.utils import timezone

from django.db import models

from django.contrib.auth import get_user_model
User = get_user_model()

class Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=300)
    openChatURL = models.URLField(null=True)
    regTime = models.DateTimeField(timezone.now())
    is_read = models.BooleanField(default=False)
