from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Product, UserFavoriteProduct

class FavoritesTestCase(TestCase):
    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Создаем продукт
        self.product = Product.objects.create(title='Test Product')

        # Создаем API-клиент
        self.client = APIClient()

        # Логинимся под созданным пользователем
        self.client.login(username='testuser', password='testpass')

