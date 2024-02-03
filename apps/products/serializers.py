from rest_framework import serializers
from apps.products.models import *

class ProductPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductPhoto
        exclude = '__all__'


class ProductsSerializer(serializers.ModelSerializer):
    product_photos = ProductPhotoSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        exclude = ['title', 'price', 'product_photos']


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        exclude = ['', 'price']