from django.urls import path, include
from rest_framework import routers
from .views import ProductsViewSet, FavoritesViewSet, CartViewSet, PhotoViewSet

urlpatterns = [
    path('products/', ProductsViewSet.as_view({'get': 'list'}), name='products'),
    path('product/<int:id>/', ProductsViewSet.as_view({'get': 'retrieve'}), name='product'),
    path('favorites/', FavoritesViewSet.as_view({'get': 'list', 'post': 'create'}), name='favorites-list'),
    path('favorites/<int:pk>/', FavoritesViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}), name='favorite-detail'),
    #     path('products/', ProductsViewSet.as_view({'get': 'list'}), name='products'),
    #     path('product/<int:id>/', ProductsViewSet.as_view({'get': 'retrieve'}), name='product'),
]
