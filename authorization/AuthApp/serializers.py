from rest_framework import serializers

from django.contrib.auth import authenticate

from .models import User

class RegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'token']

    def create(self, validated_data):
        
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email is None:
            raise serializers.ValidationError('Email is required')
        if password is None:
            raise serializers.ValidationError('Password is required')

        user = authenticate(username=email, password=password)

        # user with provided credentials  not found
        if user is None:
            raise serializers.ValidationError('User with provided credentials not found')
        
        # check if user is_active
        if user.is_active!=True:
            raise serializers.ValidationError("User is deactivated")

        return {
            'email':user.email,
            'username':user.username,
            'token':user.token
        }