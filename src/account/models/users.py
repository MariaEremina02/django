from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

from ..managers import UserManager

from config.models import BaseModel

class CustomUser(AbstractUser, PermissionsMixin, BaseModel):
    phone = models.CharField(max_length=255, unique=True, null=True, blank = True)
    first_name = models.CharField(max_length=64, null=True, blank = True)
    last_name = models.CharField(max_length=64, null=True, blank = True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    email = models.EmailField(max_length=64, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"

    class Meta:
        ordering = ["-id", "-created_at"]
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"
