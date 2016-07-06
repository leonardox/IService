from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class IserviceUser(User):
    """
    This class represents a system user.
    """

    name = models.CharField(max_length=100)
    picture = models.CharField(null=True, max_length=150)
    phone = PhoneNumberField(null=True)

    @staticmethod
    def create_user(**kwargs):
        """
        This fuction inserts an user on database.
        :param kwargs:
        :return: User instance.
        """
        user = IserviceUser()
        user.name = kwargs['name']
        user.email = kwargs['email']
        user.phone = kwargs['phone']
        user.picture = kwargs['picture']
        user.set_password(kwargs['password'])
        user.username = user.email
        user.save()
        return user
