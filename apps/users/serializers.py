from rest_framework import serializers
from .models import User
from rest_framework.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email')

class PasswordResetNewPasswordSerializer(serializers.Serializer):
    code = serializers.IntegerField(min_value=1000, max_value=9999)
    password = serializers.CharField(
        style={"input_type": "password"}, min_length=4
    )


class PasswordResetCodeSerializer(serializers.Serializer):
    code = serializers.CharField()


class PasswordResetSearchUserSerializer(serializers.Serializer):
    email = serializers.CharField()

    def validate_email(self, email):
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return ValidationError(
                f"Пользователь с указанным адресом электронной почты не найден."
            )
        return email

class UserRegistrationSerailizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password")

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(
        style={"input_type": "password"}, help_text="min length 3", min_length=3
    )

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email')

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance
