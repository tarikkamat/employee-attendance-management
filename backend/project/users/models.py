from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from project.db.models import BaseModel
from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    hire_date = models.DateField(null=True, blank=True)
    annual_leave_days = models.DecimalField(max_digits=4, decimal_places=1, default=15)

    # PermissionsMixin fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # AbstractBaseUser fields
    USERNAME_FIELD = 'email'

    objects = UserManager()
