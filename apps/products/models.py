from django.db import models

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField(default=0)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f'Название:{self.title}, В налиичи{self.available}'

class Photo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to='/media/photo_product')

    def __str__(self):
        return f'Photo for {self.product.title}'

