from django.db import models
from .constans import CM_DIRECTIONS, RUS_DIMENSION, EUR_DIMENSION, US_DIMENSION
from apps.users.models import User

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    category = models.ManyToManyField(Category, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return f'Название:{self.title}, В налиичи{self.available}'


class ProductSize(models.Model):
    product = models.ForeignKey(Product, related_name='product_sizes', on_delete=models.CASCADE)
    cm = models.IntegerField(choices=CM_DIRECTIONS, blank=True, verbose_name="Размер ноги в cm")
    rus = models.IntegerField(choices=RUS_DIMENSION, blank=True, verbose_name="Размер ноги в rus")
    eur = models.IntegerField(choices=EUR_DIMENSION, blank=True, verbose_name="Размер ноги в eur")
    us = models.IntegerField(choices=US_DIMENSION,blank=True, verbose_name="Размер ноги в us")

    class Meta:
        verbose_name = "Размер"
        verbose_name_plural = "Размеры"


class ProductPhoto(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to='photo_product')

    class Meta:
        verbose_name = "Фото продукты"
        verbose_name_plural = "Фото продуктов"

    def __str__(self):
        return f'Фото продукта {self.product.title}'

class Delivery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='delivery')
    description = models.TextField()

    class Meta:
        verbose_name = "Доставка"
        verbose_name_plural = "Доставка"

    def __str__(self):
        return f'Доставка продукта {self.product.title}'

class ProductCharacteristic(models.Model):
    product = models.ForeignKey(Product, related_name='characteristics', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    class Meta:
        verbose_name = "характеристика продукта"
        verbose_name_plural = "характеристика продуктов"

    def __str__(self):
        return f'{self.name}: {self.value} for {self.product.title}'

class Cart(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"

    def __str__(self):
        return f'Корзина-{self.items}'

    def add_amount(self):
        amount = self.product.price * self.product.quantity
        profile = self.user.profile
        profile.total_price = profile.total_price + amount
        profile.save()
        return True

class UserFavoriteProduct(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"
        unique_together = ('user', 'product')
    def __str__(self):
        return f"{self.user} - {self.product.title}"
