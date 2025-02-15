from django.contrib.auth.models import User
from rest_framework import serializers
from authentication.models import UserProfile


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)  # `create_user` hashes the password
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()  # Nested user profile data
    groups = serializers.StringRelatedField(many=True)  # Serialize related groups (names)
    permissions = serializers.StringRelatedField(many=True)  # Serialize related permissions (names)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile', 'groups', 'permissions']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation
