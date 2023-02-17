from django.contrib.auth.models import AbstractUser, UserManager, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_("email address"), max_length=150, validators=[validators.EmailValidator,], unique=True)

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"