from django.urls import path, include
from .views import UserProfileView, UserRegistrationAPIView, UserLoginAPIView, LogoutAPIView

urlpatterns = [
    # path('accounts/', include('allauth.urls')),
    path('profile/', UserProfileView.as_view()),
    path('sign_up/', UserRegistrationAPIView.as_view()),
    path('sign_in/', UserLoginAPIView.as_view()),
    path('sign_out/', LogoutAPIView.as_view()),
]