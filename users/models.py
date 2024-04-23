from random import choice
from string import digits, ascii_uppercase

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from users.managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model.
    """
    password = None
    phone_number = PhoneNumberField(
        unique=True,
        verbose_name=_('phone number'),
    )
    referral_code = models.CharField(
        max_length=6,
        unique=True,
        blank=True,
        null=True,
        verbose_name=_('referral_code'),
    )
    referrals = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        verbose_name=_('referrals'),
    )
    referred_code = models.CharField(
        max_length=6,
        blank=True,
        null=True,
        verbose_name=_('referred_code'),
    )
    pass_code = models.CharField(
        max_length=4,
        blank=True,
        null=True,
        verbose_name=_('pass code'),
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name=_('staff status'),
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('date joined'),
    )

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


@receiver(pre_save, sender=User)
def generate_random_referral(sender, instance, **kwargs):
    """
    Signal for generate random referral code (format "1A6AB5") before saving.
    If number already exists, will be generated new.
    """
    if not instance.referral_code:
        unique_number_generated = False
        while not unique_number_generated:
            random_referral = ''.join(choice(digits + ascii_uppercase) for _ in range(6))
            if not User.objects.filter(referral_code=random_referral).exists():
                instance.referral_code = random_referral
                unique_number_generated = True
