from .models import Product, ProductPhoto, Cart, UserFavoriteProduct
from apps.users.exceptions import AlreadyInFavoritesError, ProductNotFoundError

class ProductService:
    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_product_photo():
        return ProductPhoto.objects.all()

class UserFavoritesService:
    @staticmethod
    def get_class_favorites():
        return UserFavoriteProduct.objects.all()

    @staticmethod
    def get_favorite_products(user):
        favorites_products = UserFavoriteProduct.objects.filter(user=user, product=Product)
        product_ids = favorites_products.values_list('product_id', flat=True)
        products = Product.objects.filter(pk__in=product_ids)
        return products
    @staticmethod
    def is_product_in_favorites(user, product_id):
        return UserFavoriteProduct.objects.filter(user=user, product_id=product_id).exists()

    @staticmethod
    def add_product_to_favorites(user, product_id):
        try:
            product = Product.objects.get(id=product_id)
            if not UserFavoritesService.is_product_in_favorites(user, product_id):
                UserFavoriteProduct.objects.create(user=user, product=product)
                return product
            else:
                raise AlreadyInFavoritesError()
        except Product.DoesNotExist:
            raise ProductNotFoundError()

    @staticmethod
    def remove_product_from_favorites(user, product_id):
        UserFavoriteProduct.objects.filter(user=user, product_id=product_id).delete()

class CartService:
    @staticmethod
    def get_class_cart():
        return Cart.objects.all()

    @staticmethod
    def add_to_cart(user, product_id, quantity=1):
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=user)
        product = Product.objects.get(id=product_id)

        cart_item, created = cart.items.get_or_create(product=product)

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return cart_item

    @staticmethod
    def remove_from_cart(user, product_id):
        try:
            cart = Cart.objects.get(user=user)
            product = Product.objects.get(pk=product_id)
            cart_item = cart.items.get(product=product)
            cart_item.delete()

        except Cart.DoesNotExist or Product.DoesNotExist or Cart.DoesNotExist:
            pass

    @staticmethod
    def get_cart_total(user):
        try:
            cart = Cart.objects.get(user=user)
            cart_items = cart.items.all()
            total = sum(item.product.price * item.quantity for item in cart_items)
            return total
        except Cart.DoesNotExist:
            return 0
