from django.contrib.auth import authenticate
from rest_framework import serializers
from account.models import User, send_activation_code 

# from .utils import send_activation_code


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True)
    password_confirm = serializers.CharField(min_length=6, write_only=True)
    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirm')

    def validate(self, validated_data):
        # print(validated_data)
        password = validated_data.get('password')
        password_confirm = validated_data.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Passwords do not match')
        return validated_data


    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = User.objects.create_user(email=email, password=password)
        send_activation_code(email=user.email, activation_code=user.activation_code)
        return user