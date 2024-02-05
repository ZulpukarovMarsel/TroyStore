from .models import Product, ProductPhoto
from apps.users.models import UserFavoriteProduct

def get_all_products():
    return Product.objects.all()
def get_all_product_photo():
    return ProductPhoto.objects.all()

def get_favorite_products(user):
    favorites_products = UserFavoriteProduct.objects.filter(user=user, product=Product)
    product_ids = favorites_products.values_list('product_id', flat=True)
    products = Product.objects.filter(pk__in=product_ids)
    return products

def is_event_in_favorites(user, event_id):
    try:
        favorite_event = UserFavoriteProduct.objects.get(user=user, event_id=event_id)
        return True
    except UserFavoriteProduct.DoesNotExist:
        return False