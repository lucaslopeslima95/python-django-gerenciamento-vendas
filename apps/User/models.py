from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=255)
    is_deleted = models.BooleanField(default=True)

    def __str__(self):
        return self.username
