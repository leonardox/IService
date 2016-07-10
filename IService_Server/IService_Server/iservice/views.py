
from rest_framework import viewsets
from rest_framework_jwt.views import ObtainJSONWebToken
from IService_Server.iservice.models import IserviceUser
from IService_Server.iservice.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = IserviceUser.objects.all()
    serializer_class = UserSerializer


class LoginView(ObtainJSONWebToken):
    """
    Allow the user login in system
    """





