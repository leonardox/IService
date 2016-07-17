from models import IserviceUser, PhoneNumber, Tag, Service
from rest_framework import serializers


class PhoneSerializer(serializers.HyperlinkedModelSerializer):
    """
    This class serializes a phone number.
    """
    class Meta:
        model = PhoneNumber
        fields = ['phone']


class TagSerializer(serializers.HyperlinkedModelSerializer):
    """
    This class serializes a phone number.
    """
    class Meta:
        model = Tag
        fields = ['tag']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    This class serializes a user models.
    """
    phone = serializers.ListField()

    class Meta:
        model = IserviceUser
        fields = ('name', 'email', 'picture', 'phone', 'password')

    def create(self, validated_data):
        """
        Creates a new model on database from validated data.
        """
        return IserviceUser.create_user(**validated_data)

    def to_representation(self, instance):
        phones = []
        for phone in instance.phonenumber_set.all():
            phones.append(PhoneSerializer(phone).data)

        return {
            'id': instance.id,
            'name': instance.name,
            'email': instance.email,
            'phone': phones,
            'picture': instance.picture
        }


class ServiceSerializer(serializers.ModelSerializer):
    """
    This class serializes a service
    """
    tags = serializers.ListField()
    phones = serializers.ListField()

    class Meta:
        model = Service
        fields = ('name', 'description', 'tags', 'category', 'phones', 'user')

    def create(self, validated_data):
        """
        Creates a new model on database from validated data.
        """
        return Service.create_service(**validated_data)

    def to_representation(self, instance):
        phones = []
        tags = []
        for phone in instance.phonenumber_set.all():
            phones.append(PhoneSerializer(phone).data)
        for tag in instance.tag_set.all():
            tags.append(TagSerializer(tag).data)

        return {
            'name': instance.name,
            'description': instance.description,
            'phones': phones,
            'category': instance.category,
            'tags': tags,
            'user': UserSerializer(instance.user).data
        }