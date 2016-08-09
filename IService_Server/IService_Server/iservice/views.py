from copy import copy

from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.views import ObtainJSONWebToken
from IService_Server.iservice.models import IserviceUser, Service, City, State, _save_new_state, \
    _save_new_city, PhoneNumber, Tag
from IService_Server.iservice.serializers import UserSerializer, ServiceSerializer
from rest_framework.permissions import BasePermission, IsAuthenticatedOrReadOnly

SAFE_METHODS = ('POST', 'HEAD', 'OPTIONS')


class IsAuthenticatedOrCreate(BasePermission):
    """
    The request is authenticated as a user, or is a create request.
    """

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated()
        )


class UserViewSet(ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = IserviceUser.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticatedOrCreate,)

    def get_queryset(self):
        dic = self.request.query_params

        if 'email' in dic.keys():
            return IserviceUser.objects.filter(email=dic['email'])
        else:
            return IserviceUser.objects.all()


class LoginView(ObtainJSONWebToken):
    """
    Allow the user login in system
    """


class ServiceViewSet(ModelViewSet):
    """
    API endpoint that allows services to be viewed or edited.
    """
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        data = copy(request.data)
        data[u'user'] = request.user
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        """
        This method remove a service of an user.
        """
        user_services = Service.objects.filter(user=request.user)
        instance = self.get_object()
        if instance in user_services:
            self.perform_destroy(instance)
            return Response({'message': 'Service was removed with success.'},
                            status=status.HTTP_204_NO_CONTENT)
        return Response({'message': "Service not found on user's services."},
                        status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        This method updates a service.
        """
        service = self.get_object()
        data = request.data

        if service.user.email != request.user.email:
            return Response({'message': 'Access Denied!'}, status=status.HTTP_403_FORBIDDEN)

        if 'name' in data:
            service.name = data['name']

        if 'description' in data:
            service.description = data['description']

        if 'category' in data:
            service.category = data['category']

        if 'city' in data and 'state' in data and 'uf' in data:
            try:
                state_data = State.objects.get(name=data['state'])
            except State.DoesNotExist:
                state_data = _save_new_state(data['uf'], data['state'])
            try:
                city_data = City.objects.get(name=data['city'], state=state_data)
                service.city_db = city_data
            except City.DoesNotExist:
                service.city_db = _save_new_city(state_data, data['city'])

        service.save()

        if 'phones' in data:
            PhoneNumber.objects.filter(service=service).delete()
            for phone_number in data['phones']:
                phone = PhoneNumber(phone=str(phone_number), user=None, service=service)
                phone.service = service
                phone.save()

        if 'tags' in data:
            Tag.objects.filter(service=service).delete()
            for tag in data['tags']:
                tag_db = Tag(tag=tag, service=service)
                tag_db.save()

        serializer = self.get_serializer(service)

        return Response(serializer.data)

    def get_queryset(self):
        dic = self.request.query_params
        query = {}

        if 'city' in dic.keys() and 'state' in dic.keys():

            try:
                state_db = State.objects.get(uf=dic['state'].upper())
            except State.DoesNotExist:
                return None

            query['name'] = dic['city']
            query['state'] = state_db

            try:
                city_db = City.objects.get(**query)
            except City.DoesNotExist:
                return None

            return Service.objects.filter(city_db=city_db)
        elif 'self'in dic.keys():
            user = self.request.user
            return Service.objects.filter(user=user)
        elif 'favorites' in dic.keys():
            user = IserviceUser.objects.get(pk=self.request.user.pk)
            return user.favorites_services
        else:
            return Service.objects.all()


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def categories(request):
    lista = [
        "ALIMENTACAO",
        "ANIMAIS",
        "AULAS",
        "AUTOMOTIVO",
        "BELEZA_E_BEM_ESTAR",
        "CASA_E_CONSTRUCAO",
        "COMUNICACAO_E_ARTES",
        "CONSULTORIA",
        "DELIVERY",
        "EVENTOS_E_MUSICA",
        "SAUDE",
        "TECNOLOGIA",
        "TRANSPORTE",
        "SEGURANCA",
        "OUTROS"]

    return Response(lista, status=status.HTTP_200_OK)


@api_view(['POST'])
@renderer_classes((JSONRenderer,))
def favorite_service(request):
    """
    This function adds a service into user authenticated favorite list.
    """
    data = request.data
    try:
        user = IserviceUser.objects.get(pk=int(data['user']))
        service = Service.objects.get(pk=int(data['service']))
        user.add_favorite_service(service)
        return Response({'message': 'Service added with success'}, status=status.HTTP_200_OK)
    except MultiValueDictKeyError:
        return Response({'message': 'Invalid params'},
                        status=status.HTTP_400_BAD_REQUEST)
    except IserviceUser.DoesNotExist:
        return Response({'message': 'User Not Found'}, status=status.HTTP_404_NOT_FOUND)
    except Service.DoesNotExist:
        return Response({'message': 'Service Not Found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@renderer_classes((JSONRenderer,))
def undo_favorite_service(request):
    """
    This function adds a service into user authenticated favorite list.
    """
    data = request.data
    try:
        user = IserviceUser.objects.get(pk=int(data['user']))
        service = Service.objects.get(pk=int(data['service']))

        if service in user.favorites_services.all():
            user.favorites_services.remove(service)
            return Response({'message': 'Service removed with success'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': "Service isn't a favorite service"},
                            status=status.HTTP_400_BAD_REQUEST)
    except MultiValueDictKeyError:
        return Response({'message': 'Invalid params'},
                        status=status.HTTP_400_BAD_REQUEST)
    except IserviceUser.DoesNotExist:
        return Response({'message': 'User Not Found'}, status=status.HTTP_404_NOT_FOUND)
    except Service.DoesNotExist:
        return Response({'message': 'Service Not Found'}, status=status.HTTP_404_NOT_FOUND)
