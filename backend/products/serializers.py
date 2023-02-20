from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Product
from .validators import validate_no_hello, unique_product_title
from api.serializers import UserPublicSerializer


# class ProductInLineSerializer(serializers.Serializer):
#     url = serializers.HyperlinkedIdentityField(
#         view_name='product-detail',
#         lookup_field='pk',
#         read_only=True
#     )
#     title = serializers.CharField(read_only=True)

class ProductSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    # related_product = ProductInLineSerializer(source='user.product_set.all', read_only=True, many=True)
    # my_user_data = serializers.SerializerMethodField(read_only=True)
    my_discount = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail',
        lookup_field='pk',
    )
    # email = serializers.EmailField(write_only=True)
    title = serializers.CharField(validators=[validate_no_hello, unique_product_title])
    class Meta:
        model = Product
        fields = [
            'user',
            'url',
            'edit_url',
            'pk',
            'title',
            'content',
            'price',
            'sale_price',
            'my_discount',
            'public',
            # 'related_product',
        ]

    def validate(self, attrs):
        #custom validation
        return attrs
    # def get_my_user_data(self, obj):
        # return {'username': obj.user.username}

    # def validate_title(self, value):
    #     qs = Product.objects.filter(title__iexact=value)
    #     if qs.exists():
    #         raise serializers.ValidationError(f"{value} is already taken")
    #     return value


    # def create(self, validate_data):
    #     obj = super().create(validate_data)
    #     return obj
    def get_edit_url(self, obj):
        # return f"api/product/{obj.pk}/"
        request = self.context.get('request')

        if request is None:
            return None


        return reverse("product-edit", kwargs={'pk': obj.pk}, request=request)


    def get_my_discount(self, obj):
        if not hasattr(obj, 'id'):
            return None
        if not isinstance(obj, Product):
            return None

        return obj.get_discount()
