from django.http import JsonResponse
from django.shortcuts import render
from requests import Response
from rest_framework import generics, permissions, status
from django.contrib.auth.models import User
from rest_framework.exceptions import NotFound
from apps.users.exceptions import AlreadyInFavoritesError
from .serializers import UserProfileSerializer
from rest_framework.views import APIView
from apps.products.services import get_favorite_products, is_event_in_favorites, add_product_to_favorites, \
    remove_product_from_favorites
from apps.products.serializers import ProductPhotoSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

UserModel = get_user_model()


# Create your views here.
class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        if self.request.user.is_staff or self.request.user.is_authenticated \
                and self.request.user.pk == self.kwargs['user_pk']:
            return get_object_or_404(
                UserModel, pk=self.kwargs['user_pk']).profile

    def destroy(self, request, *args, **kwargs):
        return JsonResponse(
            {'message': 'DELETE method not allowed for Profile'})



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


class AddToFavoritesAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, product_id, format=None):
        user = request.user
        try:
            product = add_product_to_favorites(user, product_id)
            return Response({'message': 'Продукт добавлено в избранное'}, status=status.HTTP_200_OK)
        except NotFound as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except AlreadyInFavoritesError:
            return Response({'message': 'Продукт уже в избранном'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'message': 'Невозможно добавить продукт в избранное'}, status=status.HTTP_400_BAD_REQUEST)


class RemoveFromFavoritesAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, product_id, format=None):
        user = request.user
        remove_product_from_favorites(user, product_id)
        return Response({'message': 'Продукт удалено из избранного'}, status=status.HTTP_200_OK)
