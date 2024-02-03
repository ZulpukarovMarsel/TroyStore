from .models import Product, ProductPhoto


def get_all_products():
    return Product.objects.all()
def get_all_product_photo():
    return ProductPhoto.objects.all()



def get_user():
    return U