from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField("first name", max_length=200)
    last_name = models.CharField("last name", max_length=200)
    friends = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField("created", auto_now_add=True)
    updated = models.DateTimeField("updated", auto_now=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="from_user", unique=False
    )
    to_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="to_user", unique=False
    )
    accepted = models.BooleanField("accepted", null=True)
    created = models.DateTimeField("created", auto_now_add=True)
    updated = models.DateTimeField("updated", auto_now=True)
