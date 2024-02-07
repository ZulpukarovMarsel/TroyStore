from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'products', ProductsViewSet)
router.register(r'favorites', FavoritesViewSet)
router.register(r'cart', CartViewSet)
router.register(r'product/photo', PhotoViewSet)


urlpatterns = [
    path('', include(router.urls))
    # path('products/', ProductsModelViewSet.as_view({'get': 'list'}), name="products"),
    # path('product/<int:id>/', ProductModelViewSet.as_view({'get': 'retrieve'}), name="product"),
    # path('photo/', PhotoModelViewSet.as_view({'get': 'list'})),
    # path('favorite/', FavoritesAPIView.as_view()),
    # path('favorite/', AddToFavoritesAPIView.as_view()),
    # path('favorite', RemoveFromFavoritesAPIView.as_view())
]
