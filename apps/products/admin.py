from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'available', 'created_at', 'updated_at']
    list_filter = ['price', 'available', 'created_at', 'updated_at', 'category']
    search_fields = ['title']
@admin.register(ProductPhoto)
class ProductPhotoAdmin(admin.ModelAdmin):
    list_display = ['product', 'photo']

@admin.register(ProductCharacteristic)
class ProductCharacteristicAdmin(admin.ModelAdmin):
    list_display = ['product', 'name', 'value']

@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ['product', 'cm', 'rus', 'eur', 'us']
@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['product', 'description']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['date_created', 'user']
    filter_horizontal = ['items']

@admin.register(UserFavoriteProduct)
class UserFavoriteProductAdmin(admin.ModelAdmin):
    list_display = ['date_created', 'user', 'product']