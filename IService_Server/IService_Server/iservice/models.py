from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class IserviceUser(User):
    """
    This class represents a system user.
    """

    picture = models.CharField(max_length=150)
