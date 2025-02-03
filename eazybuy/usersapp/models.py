from django.contrib.auth.models import AbstractUser
from django.db import models
from .base import AbstractBaseModel


class CustomUser(AbstractUser,  AbstractBaseModel):
    is_customer = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    