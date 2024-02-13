from datetime import timezone

from django.db import IntegrityError
from django.http import JsonResponse
from rest_framework import generics, permissions, status, response, exceptions
from django.contrib.auth import authenticate, hashers
from apps.users.models import User, PasswordResetToken
from .serializers import *
from django.shortcuts import get_object_or_404
from apps.users.serializers import UserRegistrationSerailizer, UserLoginSerializer, LogoutSerializer
from .services import GetLoginResponseService
from rest_framework_simplejwt.tokens import RefreshToken


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
                return response.Response(data=GetLoginResponseService.get_login_response(user, request))

            else:
                return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return response.Response(
                data={"detail": "Пользователь с данной электронной почтой существует!",
                      "status": status.HTTP_409_CONFLICT})

class UserLoginAPIView(generics.CreateAPIView):
    """ API for user sign in """

    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)
        if not user:
            raise exceptions.AuthenticationFailed

        return response.Response(
            data=GetLoginResponseService.get_login_response(user, request)
        )

class LogoutAPIView(generics.CreateAPIView):
    """ API for user logout """

    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            token = RefreshToken(serializer.validated_data['refresh'])
            token.blacklist()
            return response.Response(data={"detail": "Success", "status": status.HTTP_200_OK})
        except Exception as e:
            return response.Response(data={"error": f"{e}"}, status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset

class PasswordResetNewPasswordAPIView(generics.CreateAPIView):
    """ API для сброса пароля """

    serializer_class = PasswordResetNewPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        password_reset_token = get_object_or_404(PasswordResetToken,
                                                 code=request.data['code'])

        serializer.is_valid(raise_exception=True)
        user = password_reset_token.user
        password = serializer.validated_data["password"]
        user.password = hashers.make_password(password)
        user.save()

        password_reset_token.delete()

        return response.Response(
            data={"detail": "Пароль успешно сброшен."}, status=status.HTTP_200_OK)

class PasswordResetCodeAPIView(generics.CreateAPIView):
    """ API для введения токена """

    serializer_class = PasswordResetCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            code = serializer.validated_data["code"]
            reset_code = PasswordResetToken.objects.get(
                code=code, time__gt=timezone.now()
            )
        except Exception as e:
            return response.Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data={
                    "error": f"Недействительный код для сброса пароля или время истечения кода закончилось.{e}"},
            )
        return response.Response(
            data={"detail": "success", "code": f"{code}"}, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

