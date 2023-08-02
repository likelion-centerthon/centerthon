from django.db import models
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
    balanceAmt = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class SupportFormStatus(Enum):
    waiting = '대기'
    auto_check = '확인'
    self_check = '확인'
    cancel='취소'

class SupportForm(models.Model):
    support = models.ForeignKey(Support, on_delete=models.CASCADE, related_name="form")
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    depositor = models.CharField(max_length=10)
    credit = models.IntegerField()
    creditTime = models.DateTimeField()
    status = models.CharField(choices=[(status.value, status.name) for status in SupportFormStatus], default=SupportFormStatus.waiting.value, max_length=5)

    def __str__(self):
        return self.depositor

# class Block(models.Model):


class AccountType(Enum):
    deposit='입금'
    withdraw='출금'

class Bank(models.Model):
    support = models.ForeignKey(Support, on_delete=models.CASCADE, related_name='supportBank')
    inoutType = models.CharField(max_length=5, choices=[(account.value, account.name) for account in AccountType], default=AccountType.deposit.value, null=True)
    depositor = models.CharField(max_length=10, null=True)
    credit = models.IntegerField(null=True)
    creditTime = models.DateTimeField(null=True)
    printedContent = models.CharField(max_length=20)
    balanceAmt = models.IntegerField(null=True)

    def __str__(self):
        return self.printedContent