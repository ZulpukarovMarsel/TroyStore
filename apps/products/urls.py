from django.urls import path, include
from .views import *

urlpatterns = [
    path('products/', ProductsModelViewSet.as_view({'get': 'list'}), name="products"),
    path('product/<int:id>/', ProductModelViewSet.as_view({'get': 'retrieve'}), name="product"),
    path('photo', PhotoModelViewSet.as_view({'get': 'list'}))
]