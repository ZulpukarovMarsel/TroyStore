from rest_framework import serializers
from apps.products.models import *

class ProductsSerializer(serializers.ModelSerializer):
    # product_photos = ProductPhotoSerializer(many=True, read_only=True, label='фото')
    class Meta:
        model = Product
        fields = ('title', 'price')


class ProductPhotoSerializer(serializers.ModelSerializer):
    product = ProductsSerializer(read_only=True)
    class Meta:
        model = ProductPhoto
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

