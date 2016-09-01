"""
This file contains all auxiliary functions
"""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from IService_Server.iservice.models import IserviceUser, Service, Evaluation


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def clean_table(request):
    """
    This functions cleans all entries of a table.
    """
    dic = request.query_params

    if 'users' in dic.keys():

        IserviceUser.objects.all().delete()
        data = {"User table was cleaned."}

    elif 'services' in dic.keys():

        Service.objects.all().delete()
        data = {"Service table was cleaned."}

    elif 'evaluations' in dic.keys():

        Evaluation.objects.all().delete()
        data = {"Evaluation table was cleaned."}

    else:
        data = {"Table can't be cleaned"}

    return Response(data, status=status.HTTP_200_OK)
