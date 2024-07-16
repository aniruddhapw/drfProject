from rest_framework import generics,mixins
from .models import Product
from .serializers import ProductSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from api.mixins import StaffEditorPermissionMixin

class ProductCreateAPIView(StaffEditorPermissionMixin,generics.ListCreateAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    # commented beacuse authentication classes are added as default in settings.py
    # authentication_classes=[authentication.SessionAuthentication, TokenAuthentication]
    # permission_classes=[permissions.IsAdminUser,IsStaffEditorPermisson]

    def perform_create(self, serializer):
        title=serializer.validated_data.get('title')
        content=serializer.validated_data.get('content') or None
        if content is None:
            content=title
        serializer.save(content=content)
        
product_create_view=ProductCreateAPIView.as_view()

class ProductDetailAPIView(StaffEditorPermissionMixin,generics.RetrieveAPIView):
    queryset= Product.objects.all()
    serializer_class=ProductSerializer
    #lookup_field='pk'

product_detail_view=ProductDetailAPIView.as_view()

class ProductUpdateAPIView(StaffEditorPermissionMixin,generics.UpdateAPIView):
    queryset= Product.objects.all()
    serializer_class=ProductSerializer
    lookup_field='pk'

    def perform_update(self,serilizer):
        instance = serilizer.save()
        if not instance.content:
            instance.content=instance.title

product_update_view=ProductUpdateAPIView.as_view()

class ProductDestroyAPIView(StaffEditorPermissionMixin,generics.DestroyAPIView):
    queryset= Product.objects.all()
    serializer_class=ProductSerializer
    lookup_field='pk'

    def perform_update(self,instance):
        #instance
        super().perform_destroy(instance)

product_destroy_view=ProductDestroyAPIView.as_view()

class ProductMixinView(mixins.CreateModelMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,generics.GenericAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    lookup_field='pk'

    def get(self,request,*args,**kwargs):
        pk=kwargs.get("pk")
        if pk is not None:
            return self.retrieve(request,*args,**kwargs) 
        return self.list(request,*args,**kwargs)
    
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)



product_mixin_view=ProductMixinView.as_view()


@api_view(['GET','POST'])
def product_alt_view(request,pk=None,*args,**kwargs):
    method=request.method
    print(method)
    if method=="GET":
        if pk is not None:
            #detail view
            print(pk)
            obj=get_object_or_404(Product,pk=pk)
            data=ProductSerializer(obj,many=False).data
            return Response(data)
        #list view
        queryset=Product.objects.all()
        print("hello")
        data=ProductSerializer(queryset,many=True).data
        print(data)
        return Response(data)
    if method=="POST":
        serializer=ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title=serializer.validated_data.get('title')
            content=serializer.validated_data.get('content') or None
            if content is None:
                content=title
                serializer.save(content=content)
            print(serializer.data)
            return Response(serializer.data)
        return Response({"invalid":"not good data"},status=400)

