# import json
from django.forms.models import model_to_dict
# from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from products.models import Product
from products.serializers import ProductSerializer

@api_view(['POST'])
def api_home(request, *args, **kwargs):


    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.data
        print(data)
        return Response(data)
    else:
        return Response("Error")