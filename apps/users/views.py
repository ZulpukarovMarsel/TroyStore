from django.shortcuts import render
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .serializers import UserProfileSerializer
from rest_framework.views import APIView
from apps.products.services import get_favorite_products, is_event_in_favorites
from apps.products.serializers import ProductPhotoSerializer
# Create your views here.
class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)


    def get_object(self):
        return self.request.user

class FavoritesAPIView(APIView):
    permission_classes = permissions.IsAuthenticated

    def get(self, request, format=None):
        user = request.user
        products = get_favorite_products(user)

        serialized_products = ProductPhotoSerializer(products, many=True)
        data = serialized_products.data

        for products_data in data:
            product_id = products_data.get('id')
            products_data['selected'] = is_event_in_favorites(user, product_id)
        return data

