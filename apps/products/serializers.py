from rest_framework import serializers
from apps.products.models import *
from rest_framework.fields import IntegerField

class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'

class ProductCharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCharacteristic
        fields = '__all__'

class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = '__all__'

class ProductPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhoto
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFavoriteProduct
        fields = '__all__'

class ProductsSerializer(serializers.ModelSerializer):
    # views = IntegerField(read_only=True)
    product_photos = ProductPhotoSerializer(read_only=True)
    delivery = DeliverySerializer(read_only=True)
    product_characteristics = ProductCharacteristicSerializer(read_only=True)
    product_size = ProductSizeSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'product_photos', 'delivery', 'product_characteristics', 'product_size', 'title', 'price',
                  'quantity', 'available', 'category')
        depth = 1
