from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.account.constant import GenderType, RoleType
import datetime

# Create your models here.


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    role = models.PositiveSmallIntegerField(
        choices=RoleType.CHOICES, default=RoleType.ADMIN
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Otp(TimeStampModel):
    user = models.ForeignKey("User", related_name="user_otp", on_delete=models.CASCADE)
    otp = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        get_latest_by = ("created_at",)

    def __str__(self):
        return f"{self.otp}"

    @classmethod
    def has_latest_otp(cls, user):
        last_time = datetime.datetime.now() - datetime.timedelta(minutes=5)
        return cls.objects.filter(
            is_active=True, user=user, created_at__lte=last_time
        ).exists()


class UserProfile(TimeStampModel):
    user = models.ForeignKey("User", related_name="user_profile", on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=17, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=150, blank=True, null=True)
    gender = models.PositiveSmallIntegerField(
        choices=GenderType.CHOICES, blank=True, null=True
    )