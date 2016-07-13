from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.views import ObtainJSONWebToken
from IService_Server.iservice.models import IserviceUser
from IService_Server.iservice.serializers import UserSerializer
from rest_framework.permissions import BasePermission


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
