from rest_framework import serializers
from django.contrib.auth import get_user_model

user = get_user_model()
class UserProductInLineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail',
        lookup_field='pk',
        read_only=True
    )
    title = serializers.CharField(read_only=True)

class UserPublicSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    # not_real = serializers.CharField(read_only=True)

    # class Meta:
    #     model = user
    #     fields = '__all__'


    # other_products = serializers.SerializerMethodField(read_only=True)
    #
    # def get_other_products(self, obj):
    #
    #     user = obj
    #     my_product_qs = user.product_set.all()[:5]
    #     return UserProductInLineSerializer(my_product_qs, many=True, context=self.context).data
