from django.db import models

class Artist(models.Model):
    artistName = models.CharField(max_length=50)
    members = models.CharField(max_length=200, null=True)
    artistImage = models.ImageField()

    instagram = models.URLField()
    twitter = models.URLField()
    youtube = models.URLField()

    debutDate = models.DateField()
    color = models.CharField(max_length=30)
    fanName = models.CharField(max_length=30)
    agency = models.CharField(max_length=30)

    def __str__(self):
        return self.artistName
