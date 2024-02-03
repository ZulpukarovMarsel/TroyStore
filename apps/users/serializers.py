from rest_framework import serializers
from django.contrib.auth.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.firstname = validated_data.get('username', instance.username)
        instance.firstname = validated_data.get('first_name', instance.firstname)
        instance.firstname = validated_data.get('first_name', instance.firstname)
        instance.lastname = validated_data.get('last_name', instance.lastname)
        instance.save()
        return instance
