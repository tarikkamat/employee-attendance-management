from django.conf import settings
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


class UserSession(BaseModel):
    fk_user_id = models.ForeignKey(User, db_column="fk_user_id", on_delete=models.CASCADE, related_name="sessions")
    total_work_minutes = models.PositiveIntegerField(default=0)
    late_minutes = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def calculate_late_minutes(self):
        work_start_time = settings.COMPANY_SETTINGS.get("WORK_START_HOURS")
        if self.created_at.hour > work_start_time:
            return (self.created_at.hour - work_start_time) * 60 + self.created_at.minute
        return 0

    def calculate_total_work_minutes(self):
        return (self.updated_at - self.created_at).total_seconds() / 60

    def save(self, *args, **kwargs):
        self.total_work_minutes = self.calculate_total_work_minutes()
        super().save(*args, **kwargs)
