from collections import OrderedDict

from rest_framework.fields import SkipField

from models import IserviceUser
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    This class serializes a user models.
    """
    class Meta:
        model = IserviceUser
        fields = ('name', 'email', 'picture', 'phone', 'password')

    def create(self, validated_data):
        """
        Creates a new model on database from validated data.
        """
        return IserviceUser.create_user(**validated_data)

    def to_representation(self, instance):
        return {
            'name': instance.name,
            'email': instance.email,
            'phone': str(instance.phone),
            'picture': instance.picture
        }
