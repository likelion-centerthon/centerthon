from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from artist.models import Artist

class UserManager(BaseUserManager):
    def create_user(self, kakaoId, userName, age, gender, password=None, **extra_fields):
        user = self.model(
            kakaoId=kakaoId,
            userName=userName,
            age=age,
            gender=gender
        )
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        user.set_password(password)
        user.is_active = True
        user.save()
        return user

    def create_superuser(self, kakaoId, userName, password=None, **extra_fields):
        superuser = self.create_user(
            kakaoId=kakaoId,
            userName=userName,
            age=999,
            gender='none',
            password=password
        )
        superuser.is_admin = True
        superuser.is_superuser = True
        superuser.is_active = True
        superuser.is_staff = True
        superuser.save()
        return superuser

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    kakaoId=models.CharField(max_length=100, unique=True)
    userName=models.CharField(max_length=100)
    age=models.IntegerField(null=True)
    gender=models.CharField(max_length=10, null=True)
    phoneNumberRegex = RegexValidator(regex=r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$')
    phoneNumber = models.CharField(validators=[phoneNumberRegex], max_length=11, unique=True, null=True)
    subPhoneNumber=models.CharField(null=True, validators=[phoneNumberRegex], max_length=11)
    region=models.CharField(null=True, max_length=20)

    artists=models.ManyToManyField(Artist)

    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'kakaoId'
    REQUIRED_FIELDS = ['userName']

    def __str__(self):
        return self.userName
