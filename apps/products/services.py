from .models import Product, ProductPhoto
from apps.users.models import UserFavoriteProduct
from apps.users.exceptions import AlreadyInFavoritesError, ProductNotFoundError


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

def add_product_to_favorites(user, product_id):
    try:
        product = Product.objects.get(id=product_id)
        if not UserFavoriteProduct.objects.filter(user=user, product_id=product_id).exists():
            UserFavoriteProduct.objects.create(user=user, product=product)
            return product
        else:
            raise AlreadyInFavoritesError()
    except Product.DoesNotExist:
        raise ProductNotFoundError()

def remove_product_from_favorites(user, product_id):
    UserFavoriteProduct.objects.filter(user=user, product_id=product_id).delete()

