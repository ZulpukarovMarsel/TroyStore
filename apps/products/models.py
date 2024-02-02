from django.db import models

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


# class ProductSize(models.Model):
#

class Photo(models.Model):
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
