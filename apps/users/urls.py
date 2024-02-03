from django.urls import path, include
from .views import UserProfileView

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('profile/', UserProfileView.as_view())
]