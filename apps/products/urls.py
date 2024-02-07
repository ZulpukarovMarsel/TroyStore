from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'products', ProductsViewSet, basename='products')
router.register(r'favorites', FavoritesViewSet, basename='favorites')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'product/photo', PhotoViewSet, basename='product-photo')

urlpatterns = [
    path('', include(router.urls))
]
