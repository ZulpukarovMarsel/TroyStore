from rest_framework import serializers
from apps.products.models import *

class ProductPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductPhoto
        fields = '__all__'


class ProductsSerializer(serializers.ModelSerializer):
    product_photos = ProductPhotoSerializer(many=True, read_only=True, label='фото')
    class Meta:
        model = Product
        fields = ('title', 'price', 'product_photos')


class ProductSerializer(serializers.ModelSerializer):
    product_photos = ProductPhotoSerializer(many=True, read_only=True, label='фото')

    class Meta:
        model = Product
        fields = ('title', 'description', 'price', 'available', 'category', 'product_photos')