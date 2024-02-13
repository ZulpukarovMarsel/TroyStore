from rest_framework import viewsets
from .serializers import *
from apps.products.serializers import ProductPhotoSerializer
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import generics, permissions, status, filters
from .services import *
from rest_framework.decorators import action
from rest_framework.views import APIView


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = ProductService.get_all_products()
    serializer_class = ProductsSerializer
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = ProductService.get_all_products()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)
        return queryset


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = ProductService.get_all_product_photo()
    serializer_class = ProductPhotoSerializer


# class FavoritesViewSet(viewsets.ModelViewSet):
#     queryset = UserFavoritesService.get_class_favorites()
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = FavoriteSerializer
#
#     @action(detail=False, methods=['get'])
#     def get_favorite(self, request):
#         user = request.user
#         favorite_products = UserFavoritesService.get_favorite_products(user)
#
#         serialized_favorite_products = FavoriteSerializer(favorite_products, many=True)
#         data = serialized_favorite_products.data
#
#         for product_data in data:
#             product_data['selected'] = True  # Помечаем продукты как избранные, поскольку это запрос на избранные продукты пользователя
#
#         return Response(data)
#
#     @action(detail=False, methods=['post'])
#     def add_to_favorite(self, request, product_id):
#         user = request.user
#         try:
#             product = UserFavoritesService.add_product_to_favorites(user, product_id)
#             return Response({'message': 'Продукт добавлено в избранное'}, status=status.HTTP_200_OK)
#         except NotFound as e:
#             return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
#         except AlreadyInFavoritesError:
#             return Response({'message': 'Продукт уже в избранном'}, status=status.HTTP_400_BAD_REQUEST)
#         except:
#             return Response({'message': 'Невозможно добавить продукт в избранное'}, status=status.HTTP_400_BAD_REQUEST)
#
#     @action(detail=True, methods=['delete'])
#     def remove_from_favorite(self, request, product_id):
#         user = request.user
#         UserFavoritesService.remove_product_from_favorites(user, product_id)
#         return Response({'message': 'Продукт удалено из избранного'}, status=status.HTTP_200_OK)

class FavoritesViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        products = UserFavoritesService.get_favorite_products(user)

        serialized_products = FavoriteSerializer(products, many=True)  # Используйте FavoriteSerializer
        data = serialized_products.data

        for product_data in data:
            product_id = product_data.get('id')
            product_data['selected'] = UserFavoritesService.is_product_in_favorites(user, product_id)
        return Response(data)

    def post(self, request, product_id):
        user = request.user
        try:
            product = UserFavoritesService.add_product_to_favorites(user, product_id)
            return Response({'message': 'Продукт добавлен в избранное'}, status=status.HTTP_200_OK)
        except NotFound as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except AlreadyInFavoritesError:
            return Response({'message': 'Продукт уже в избранном'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'message': 'Невозможно добавить продукт в избранное'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        user = request.user
        UserFavoritesService.remove_product_from_favorites(user, product_id)
        return Response({'message': 'Продукт удален из избранного'}, status=status.HTTP_200_OK)


class CartViewSet(viewsets.ModelViewSet):
    queryset = CartService.get_class_cart()
    serializer_class = CartSerializer
    permission_classes = (permissions.IsAuthenticated,)

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
