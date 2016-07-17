from copy import copy

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.views import ObtainJSONWebToken
from IService_Server.iservice.models import IserviceUser, Service
from IService_Server.iservice.serializers import UserSerializer, ServiceSerializer
from rest_framework.permissions import BasePermission, IsAuthenticated

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
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (IsAuthenticatedOrCreate,)


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
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        data = copy(request.data)
        data[u'user'] = request.user
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
