from django.db import models
from .constans import CM_DIRECTIONS, RUS_DIMENSION, EUR_DIMENSION, US_DIMENSION
# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField(default=0)
    available = models.BooleanField(default=True)
    category = models.ManyToManyField(Category, related_name='products')

    def __str__(self):
        return f'Название:{self.title}, В налиичи{self.available}'


class ProductSize(models.Model):
    product = models.ForeignKey(Product, related_name='product_sizes', on_delete=models.CASCADE)
    cm = models.IntegerField(choices=CM_DIRECTIONS, blank=True, verbose_name="Размер ноги в cm")
    rus = models.IntegerField(choices=RUS_DIMENSION, blank=True, verbose_name="Размер ноги в rus")
    eur = models.IntegerField(choices=EUR_DIMENSION, blank=True, verbose_name="Размер ноги в eur")
    us = models.IntegerField(choices=US_DIMENSION,blank=True, verbose_name="Размер ноги в us")


class ProductPhoto(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to='/media/photo_product')

    def __str__(self):
        return f'Фото продукта {self.product.title}'

class Delivery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='delivery')
    description = models.TextField()

    def __str__(self):
        return f'Доставка продукта {self.product.title}'

class ProductCharacteristic(models.Model):
    product = models.ForeignKey(Product, related_name='characteristics', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}: {self.value} for {self.product.title}'
