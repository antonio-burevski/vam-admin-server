from django.contrib.auth.models import User, Permission
from rest_framework import serializers
from authentication.models import UserProfile


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)  # `create_user` hashes the password
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["phone_number", "address"]


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)  # 👈 Allow missing profiles
    groups = serializers.StringRelatedField(many=True)
    permissions = serializers.SerializerMethodField()  # 👈 Custom method for permissions

    class Meta:
        model = User
        fields = ["id", "username", "email", "profile", "groups", "permissions"]

    def get_permissions(self, obj):
        return obj.user_permissions.values_list("codename", flat=True)  # 👈 Fix the error

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # 👇 Ensure 'profile' key is present, even if the user has no profile
        if "profile" not in representation:
            representation["profile"] = None

        return representation
