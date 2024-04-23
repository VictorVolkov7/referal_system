from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user manager for handling users with phone number authentication.
    """

    def create_user(self, phone, **extra_fields):
        """
        Create and return a regular user with the given phone number.
        """
        if not phone:
            raise ValueError(_('The phone number must be set'))
        user = self.model(phone=phone, **extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, **extra_fields):
        """
        Create and return a superuser with the given phone number.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone, **extra_fields)
