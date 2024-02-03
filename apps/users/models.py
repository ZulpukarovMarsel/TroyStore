from django.contrib.auth.models import User
from django.db import models
from apps.products.models import Product
class UserFavoriteEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"

    def __str__(self):
        return f"{self.user.name} - {self.product.title}"
