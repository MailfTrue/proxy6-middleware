from rest_framework import serializers
from .models import User, Token


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'balance')
        read_only_fields = ('username', 'balance')


class CreateUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        # call create_user on user object. Without this
        # the password will be stored in plain text.
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email',)
        extra_kwargs = {'password': {'write_only': True}}


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = "id", "key", "created", "user_id"
        read_only_fields = 'key',
