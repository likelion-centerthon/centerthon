from enum import Enum

from django.db import models

class Category(Enum):
    KPOP = 'KPOP'
    트로트 = '트로트'
    발라드 = '발라드'
    기타 = '기타'


class Artist(models.Model):
    category = models.CharField(max_length=10, choices=[(status.value, status.name) for status in Category], default=Category.기타.value)
    artistName = models.CharField(max_length=50, null=False)
    members = models.CharField(max_length=200, null=True)
    artistImage = models.ImageField(null=False)

    instagram = models.URLField()
    twitter = models.URLField()
    youtube = models.URLField()

    debutDate = models.DateField()
    color = models.CharField(max_length=30)
    fanName = models.CharField(max_length=30)
    agency = models.CharField(max_length=30)



    def __str__(self):
        return self.artistName

