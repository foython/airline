from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'admin'),
        (2, 'agent'),
        (3, 'client'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default='3')

