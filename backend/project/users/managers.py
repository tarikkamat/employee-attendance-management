from django.contrib.auth.base_user import BaseUserManager

from project.db.managers import BaseManager


class UserManager(BaseUserManager, BaseManager):
    def _create_user(self, email, password, is_active, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('The given email is not valid')
        user = self.model(email=email, is_active=is_active, is_staff=is_staff, is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, is_active=True, is_staff=False, is_superuser=False, **extra_fields)

    def create_from_api(self, email, password, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, is_active=True, is_staff=True, is_superuser=True, **extra_fields)
        user.save(using=self._db)
        return user
