from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from .serializers import *
from apps.products.services import get_all_products, get_all_product_photo


class ProductModelViewSet(viewsets.ModelViewSet):
    queryset = get_all_products()
    serializer_class = ProductSerializer
    lookup_field = 'id'

class ProductsModelViewSet(viewsets.ModelViewSet):
    queryset = get_all_products()
    serializer_class = ProductsSerializer

class PhotoModelViewSet(viewsets.ModelViewSet):
    queryset = get_all_product_photo()
    serializer_class = ProductPhotoSerializer
