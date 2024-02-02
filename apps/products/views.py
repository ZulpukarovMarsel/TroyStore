from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from .serializers import *
from services import get_all_products


class ProductModelViewSet(viewsets.ModelViewSet):
    queryset = get_all_products()
    serializer_class = ProductSerializer
    lookup_field = 'id'

class ProductsAPIView(viewsets.ModelViewSet):
    queryset = get_all_products()
    serializer_class = ProductsSerializer
    lookup_field = 'id'