from models import IserviceUser
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = IserviceUser
        fields = ('first_name', 'last_name', 'email', 'picture')
