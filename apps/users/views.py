from django.db import IntegrityError
from django.http import JsonResponse
from requests import Response
from rest_framework import generics, permissions, status
from apps.users.models import User
from .serializers import UserProfileSerializer
from django.shortcuts import get_object_or_404
from apps.users.serializers import UserRegistrationSerailizer
from .services import GetLoginResponseService


class UserRegistrationAPIView(generics.CreateAPIView):
    """ API for user registrations """

    serializer_class = UserRegistrationSerailizer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                user = User.objects.create_user(
                                                       email=serializer.validated_data["email"],
                                                       password=serializer.validated_data["password"],
                                                       )
                return Response(data=GetLoginResponseService.get_login_response(user, request))

            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response(
                data={"detail": "Пользователь с данной электронной почтой существует!",
                      "erro": status.HTTP_409_CONFLICT})


# Create your views here.
class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        if self.request.user.is_staff or self.request.user.is_authenticated \
                and self.request.user.pk == self.kwargs['user_pk']:
            return get_object_or_404(
                User, pk=self.kwargs['user_pk']).profile

    def destroy(self, request, *args, **kwargs):
        return JsonResponse(
            {'message': 'DELETE method not allowed for Profile'})

