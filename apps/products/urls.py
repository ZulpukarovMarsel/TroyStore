from django.urls import path, include
from rest_framework import routers
from .views import ProductsViewSet, FavoritesViewSet, CartViewSet, PhotoViewSet

urlpatterns = [
    path('products/', ProductsViewSet.as_view({'get': 'list'}), name='products'),
    path('product/<int:id>/', ProductsViewSet.as_view({'get': 'retrieve'}), name='product'),
    # path('favorites/', FavoritesViewSet.as_view(), name='favorites-list'),
    # path('favorites/<int:pk>/', FavoritesViewSet.as_view(), name='favorite-detail'),
    path('favorites/', FavoritesViewSet.as_view(), name='favorites-list'),
    path('favorites/<int:pk>/', FavoritesViewSet.as_view(), name='favorite-detail'),
    #     path('products/', ProductsViewSet.as_view({'get': 'list'}), name='products'),
    #     path('product/<int:id>/', ProductsViewSet.as_view({'get': 'retrieve'}), name='product'),
]
