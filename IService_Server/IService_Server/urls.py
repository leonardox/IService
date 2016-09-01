"""IService_Server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.7/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers

from IService_Server.iservice import views
from IService_Server.iservice.utils import clean_table
from IService_Server.iservice.views import LoginView, favorite_service, undo_favorite_service,\
    get_recommendation
from IService_Server.iservice.views import categories

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'services', views.ServiceViewSet)
router.register(r'evaluation', views.EvaluationViewSet)


urlpatterns = [
    url(r'^login', LoginView.as_view(), name="login"),
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^categories', categories),
    url(r'^favorite-service', favorite_service),
    url(r'^undo-favorite-service', undo_favorite_service),
    url(r'^recommendation', get_recommendation),
    url(r'^admin/clean-table/', clean_table),
]
