from django.http import JsonResponse
from products.models import Product
from django.forms import model_to_dict
from rest_framework.decorators import api_view
from rest_framework.response import Response
from products.serializers import ProductSerializer

@api_view(['POST'])
def api_home(request,*args,**kwargs):
    serializer=ProductSerializer(data=request.data)
    if serializer.is_valid():
        instance= serializer.save()
        print(instance)
        data=serializer.data
        return Response(data)
   