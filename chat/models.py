from __future__ import unicode_literals
from django.utils.timezone import now
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    mobile_phone = models.CharField(max_length=255, null=False, blank=False, unique=True)
