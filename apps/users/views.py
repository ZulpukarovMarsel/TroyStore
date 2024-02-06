from django.http import JsonResponse
from rest_framework import generics, permissions, status
from django.contrib.auth.models import User
from .serializers import UserProfileSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

UserModel = get_user_model()


# Create your views here.
class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        if self.request.user.is_staff or self.request.user.is_authenticated \
                and self.request.user.pk == self.kwargs['user_pk']:
            return get_object_or_404(
                UserModel, pk=self.kwargs['user_pk']).profile

    def destroy(self, request, *args, **kwargs):
        return JsonResponse(
            {'message': 'DELETE method not allowed for Profile'})

