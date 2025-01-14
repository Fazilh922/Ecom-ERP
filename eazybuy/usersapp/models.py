from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
