from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from authentication.models import UserProfile, UserJitPermission


class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all(), message="Username already taken.")]
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all(), message="Email already registered.")]
    )
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["phone_number", "address"]


class UserJitPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserJitPermission
        fields = ['permission', 'status', 'granted_at', 'expiration']

    def to_representation(self, instance):
        # Check if the permission is expired
        if instance.is_expired() and instance.status != 'expired':
            instance.status = 'expired'
            instance.save()  # Update the status in the database

        return super().to_representation(instance)


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)
    groups = serializers.StringRelatedField(many=True)
    permissions = serializers.SerializerMethodField()
    jit_permissions = UserJitPermissionSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "profile", "groups", "permissions", "jit_permissions"]

    def get_permissions(self, obj):
        user_permissions = set(obj.user_permissions.values_list("codename", flat=True))

        group_permissions = set(obj.groups.values_list("permissions__codename", flat=True))

        jit_permissions = set(
            obj.jit_permissions.filter(status='active').values_list("permission__codename", flat=True))

        return list(user_permissions.union(group_permissions, jit_permissions))

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if "profile" not in representation:
            representation["profile"] = None

        if "jit_permissions" not in representation:
            representation["jit_permissions"] = []

        return representation
