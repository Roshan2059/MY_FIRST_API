# Create your models here.
import uuid as uuid_lib

from applications.account.managers import CustomUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class User(AbstractUser):
    uuid = models.UUIDField(default=uuid_lib.uuid4,editable=False)
    email = models.CharField(_('Email address'), max_length=250, unique=True)
    first_name = models.CharField(_('Firstname'), max_length=250)
    last_name = models.CharField(_('Lastname'), max_length=250)
    password = models.CharField(_('Password'), max_length=250)
    is_maintainer = models.BooleanField(_('Is Maintainer'), default=False)
    is_customer = models.BooleanField(_('Is Customer'), default=True)
    profile_image = models.FileField(
        upload_to="account/%Y/%m/%d/user/", null=True, blank=True, default=None)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Reset(models.Model):
    email = models.CharField(max_length=250)
    token = models.CharField(max_length=255, unique=True)
