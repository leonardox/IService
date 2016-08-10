from models import IserviceUser, PhoneNumber, Tag, Service, State, City, Evaluation
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


class UserSerializer(serializers.ModelSerializer):
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
        favorites = []

        for phone in instance.phonenumber_set.all():
            phones.append(PhoneSerializer(phone).data['phone'])

        for service in instance.favorites_services.all():
            favorites.append(service.id)

        return {
            'id': instance.id,
            'name': instance.name,
            'email': instance.email,
            'phone': phones,
            'picture': instance.picture,
            "favorites": favorites
        }


class StateSerializer(serializers.ModelSerializer):
    """
    This class serializes a state.
    """
    class Meta:
        model = State
        fields = ('uf', 'name')


class CitySerializer(serializers.ModelSerializer):
    """
    This class serializes a city.
    """
    class Meta:
        model = City
        fields = ('name', 'state')

    def to_representation(self, instance):
        return {
            'name': instance.name,
            'state': StateSerializer(instance.state).data
        }


class ServiceSerializer(serializers.ModelSerializer):
    """
    This class serializes a service
    """
    tags = serializers.ListField()
    phones = serializers.ListField()
    city = serializers.CharField()
    uf = serializers.CharField()
    state = serializers.CharField()

    class Meta:
        model = Service
        fields = ('name', 'description', 'tags', 'category', 'phones', 'user', 'city', 'uf',
                  'state')

    def create(self, validated_data):
        """
        Creates a new model on database from validated data.
        """
        return Service.create_service(**validated_data)

    def to_representation(self, instance):
        phones = []
        tags = []
        for phone in instance.phonenumber_set.all():
            phones.append(PhoneSerializer(phone).data['phone'])
        for tag in instance.tag_set.all():
            tags.append(TagSerializer(tag).data['tag'])

        avg = 0.0
        evaluations = Evaluation.objects.filter(service=instance)
        for evaluation in evaluations:
            avg += evaluation.note

        avg = (avg / len(evaluations))

        return {
            'id': instance.id,
            'name': instance.name,
            'description': instance.description,
            'phones': phones,
            'category': instance.category,
            'tags': tags,
            'user': UserSerializer(instance.user).data,
            'city': CitySerializer(instance.city_db).data,
            'average': avg
        }


class EvaluationSerializer(serializers.ModelSerializer):
    """
    This class serializes a city.
    """
    class Meta:
        model = Evaluation
        fields = ('id', 'user', 'service', 'note', 'comment')
