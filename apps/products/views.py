from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from .serializers import *
from apps.products.serializers import ProductPhotoSerializer
from rest_framework.exceptions import NotFound
from apps.users.exceptions import AlreadyInFavoritesError
from django.shortcuts import render
from requests import Response
from rest_framework import generics, permissions, status
from .services import *

class ProductsViewSet(viewsets.ModelViewSet):
    queryset = ProductService.get_all_products()
    serializer_class = ProductsSerializer
    lookup_field = 'id'


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = ProductService.get_all_product_photo()
    serializer_class = ProductPhotoSerializer


class FavoritesViewSet(viewsets.ModelViewSet):
    queryset = UserFavoritesService.get_class_favorites()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FavoriteSerializer
    def get_favorite(self, request):
        user = request.user
        products = UserFavoritesService.get_favorite_products(user)

        serialized_products = ProductPhotoSerializer(products, many=True)
        data = serialized_products.data

        for products_data in data:
            product_id = products_data.get('id')
            products_data['selected'] = UserFavoritesService.is_event_in_favorites(user, product_id)
        return data

    def add_to_favorite(self, request, product_id):
        user = request.user
        try:
            product = UserFavoritesService.add_product_to_favorites(user, product_id)
            return Response({'message': 'Продукт добавлено в избранное'}, status=status.HTTP_200_OK)
        except NotFound as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except AlreadyInFavoritesError:
            return Response({'message': 'Продукт уже в избранном'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'message': 'Невозможно добавить продукт в избранное'}, status=status.HTTP_400_BAD_REQUEST)

    def remove_from_favorite(self, request, product_id):
        user = request.user
        UserFavoritesService.remove_product_from_favorites(user, product_id)
        return Response({'message': 'Продукт удалено из избранного'}, status=status.HTTP_200_OK)


class CartViewSet(viewsets.ModelViewSet):
    queryset = CartService.get_class_cart()
    serializer_class = CartSerializer

    def add_to_cart(self, request, *args, **kwargs):
        user = self.request.user
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        cart_item = CartService.add_to_cart(user, product_id, quantity, quantity)

        serializer = CartSerializer(cart_item.cart)

        return Response(serializer.data)

    def remove_from_cart(self, request, *args, **kwargs):
        user = self.request.user
        product_id = request.data.get('product_id')

        CartService.remove_from_cart(user, product_id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_cart_total(self, request, *args, **kwargs):
        user = self.request.user
        total = CartService.get_cart_total(user)

        return Response({'total': total})