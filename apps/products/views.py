from django.http import Http404
from rest_framework import viewsets
from .serializers import *
from apps.products.serializers import ProductPhotoSerializer
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import generics, permissions, status, filters
from .services import *
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination


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


class FavoritesViewSet(viewsets.ModelViewSet):
    queryset = UserFavoritesService.get_class_favorites()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        user = self.request.user
        products = UserFavoritesService.get_favorite_products(user)
        return products

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Пагинируем результат
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)

        # Сериализуем пагинированные данные
        serializer = self.serializer_class(page, many=True)
        data = serializer.data

        user = self.request.user
        for product_data in data:
            product_id = product_data.get("product_id")
            product_data['selected'] = UserFavoritesService.is_product_in_favorites(user, product_id)

        # Возвращаем только список продуктов
        return Response(data)

    def perform_create(self, serializer):
        user = self.request.user
        product_id = self.request.data.get('product_id')

        try:
            product = UserFavoritesService.add_product_to_favorites(user, product_id)
        except Http404:
            raise serializers.ValidationError({'message': 'Продукт не найден'})
        except AlreadyInFavoritesError:
            raise serializers.ValidationError({'message': 'Продукт уже в избранном'})
        except Exception as e:
            raise serializers.ValidationError({'message': str(e)})

    def perform_destroy(self, instance):
        user = self.request.user
        product_id = instance.product_id

        try:
            UserFavoritesService.remove_product_from_favorites(user, product_id)
        except Http404:
            raise serializers.ValidationError({'message': 'Продукт не найден'})
        except Exception as e:
            raise serializers.ValidationError({'message': str(e)})


# class FavoritesViewSet(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get(self, request):
#         user = request.user
#         products = UserFavoritesService.get_favorite_products(user)
#
#         serialized_products = FavoriteSerializer(products, many=True)  # Используйте FavoriteSerializer
#         data = serialized_products.data
#
#         for product_data in data:
#             product_id = product_data.get('id')
#             product_data['selected'] = UserFavoritesService.is_product_in_favorites(user, product_id)
#         return Response(data)
#
#     def post(self, request, product_id):
#         user = request.user
#         try:
#             product = UserFavoritesService.add_product_to_favorites(user, product_id)
#             return Response({'message': 'Продукт добавлен в избранное'}, status=status.HTTP_200_OK)
#         except NotFound as e:
#             return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)
#         except AlreadyInFavoritesError:
#             return Response({'message': 'Продукт уже в избранном'}, status=status.HTTP_400_BAD_REQUEST)
#         except:
#             return Response({'message': 'Невозможно добавить продукт в избранное'}, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, product_id):
#         user = request.user
#         UserFavoritesService.remove_product_from_favorites(user, product_id)
#         return Response({'message': 'Продукт удален из избранного'}, status=status.HTTP_200_OK)


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
