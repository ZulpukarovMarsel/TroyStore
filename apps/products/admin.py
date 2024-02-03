from django.contrib import admin
from .models import Product, ProductPhoto, ProductSize, ProductCharacteristic, Category
# Register your models here.

admin.site.register(Product)
admin.site.register(ProductPhoto)
admin.site.register(ProductSize)
admin.site.register(ProductCharacteristic)
admin.site.register(Category)
