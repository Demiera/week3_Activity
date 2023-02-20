from rest_framework import generics, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from api.mixins import StaffEditorPermissionMixin, UserQuerySetMixin
from .models import Product
from .serializers import ProductSerializer



class ProductListCreateAPIView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.ListCreateAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # def perform_create(self, serializer):
    #     # serializer.save(user=self.request.user)
    #     # email = serializer.validated_data.pop('email')
    #     title = serializer.validated_data.get('title')
    #     content = serializer.validated_data.get('content') or None
    #     if content is None:
    #         content = title
    #     serializer.save(user=self.request.user, content=content)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        request = self.request
        user = request.user

        if not user.is_authenticated:
            return Product.objects.none()
        if user.is_superuser:
            return qs

        print(request.user)
        return qs.filter(user=request.user)

class ProductDetailAPIView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.RetrieveAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductUpdateAPIView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.RetrieveUpdateAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        if self.request.user.is_superuser:
            instance = serializer.save()
        elif self.request.user == Product.user:
            instance = serializer.save()

class ProductDeleteAPIView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.RetrieveDestroyAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        if self.request.user.is_superuser:
            super().perform_destroy(instance)
        elif self.request.user == Product.user:
            super().perform_destroy(instance)




#sample sa mixinView
class ProductMixinView(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    generics.GenericAPIView
    ):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = 'this is a cool stuff'
        serializer.save(content=content)








#sample sa funtion api view
@api_view(['GET', 'POST'])
def product_alt_view(request, pk=None, *args, **kwargs):
    method = request.method

    if method == 'GET':
        if pk is not None:
            obj = get_object_or_404(Product, pk=pk)
            data = ProductSerializer(obj, many=False).data
            return Response(data)
        queryset = Product.objects.all()
        data = ProductSerializer(queryset, many=True).data
        return Response(data)

    if method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content') or None
            if content is None:
                content = title
            serializer.save(content=content)
            print(serializer.data)
            return Response(serializer.data)

        return Response({"Invalid": "your data is not valid"}, status=400)


