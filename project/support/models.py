from django.db import models
from django.utils import timezone
from enum import Enum

class SupportStatus(Enum):
    in_progress='진행중'
    complete='완료'

class Support(models.Model):
    artist = models.ForeignKey('artist.Artist', on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    body = models.TextField()
    regTime = models.DateTimeField(auto_now=True)
    image = models.ImageField()
    deadline = models.DateTimeField()
    fundraising = models.IntegerField()
    account = models.CharField(max_length=14)
    bank = models.CharField(max_length=10)
    status = models.CharField(choices=[(status.value, status.name) for status in SupportStatus], default=SupportStatus.in_progress.value, max_length=5)

class SupportFormStatus(Enum):
    waiting = '대기'
    auto_check = '확인'
    self_check = '확인'
    cancel='취소'

class SupportForm(models.Model):
    support = models.ForeignKey(Support, on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    depositor = models.CharField(max_length=10)
    credit = models.IntegerField()
    creditTime = models.DateTimeField()
    status = models.CharField(choices=[(status.value, status.name) for status in SupportFormStatus], default=SupportFormStatus.waiting.value, max_length=5)

# class Block(models.Model):


# class Bank(models.Model):
