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

    def test_add_to_favorite(self):
        # Запрашиваем API для добавления продукта в избранное
        response = self.client.post(f'/api/v1/favorites/{self.product.id}/')

        # Проверяем, что запрос завершился успешно
        self.assertEqual(response.status_code, 200)

        # Проверяем, что продукт добавлен в избранное для пользователя
        self.assertTrue(UserFavoriteProduct.objects.filter(user=self.user, product=self.product).exists())

    def test_remove_from_favorite(self):
        # Добавляем продукт в избранное для пользователя
        UserFavoriteProduct.objects.create(user=self.user, product=self.product)

        # Запрашиваем API для удаления продукта из избранного
        response = self.client.delete(f'/api/v1/favorites/{self.product.id}/')

        # Проверяем, что запрос завершился успешно
        self.assertEqual(response.status_code, 200)

        # Проверяем, что продукт удален из избранного для пользователя
        self.assertFalse(UserFavoriteProduct.objects.filter(user=self.user, product=self.product).exists())
