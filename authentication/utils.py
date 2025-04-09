import datetime

from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

from authentication.models import UserJitPermission


def create_access_token(user):
    """
    Generates an access token using the JWT refresh token
    """
    refresh = RefreshToken.for_user(user)

    # Set custom expiration time for the access token (e.g., 15 minutes)
    refresh.set_exp(lifetime=datetime.timedelta(minutes=15))

    access_token = str(refresh.access_token)

    return access_token


def create_refresh_token(user):
    """
    Generates a refresh token for the user
    """
    refresh = RefreshToken.for_user(user)

    # Set custom expiration time for the refresh token (e.g., 7 days)
    refresh.set_exp(lifetime=datetime.timedelta(days=7))  # Adjust as needed

    refresh_token = str(refresh)

    return refresh_token


def create_access_token_from_refresh(refresh_token_value):
    """
    Generates an access token using the provided refresh token
    """
    try:
        refresh_token = RefreshToken(refresh_token_value)
        access_token = str(refresh_token.access_token)
        return access_token
    except Exception as e:
        raise Exception("Invalid refresh token") from e


def check_permission(request, permission_codename):
    # Check if the user has the regular permission
    if request.user.has_perm(permission_codename):
        return Response({"message": "Success"}, status=status.HTTP_200_OK)

    # If the user doesn't have the regular permission, check for JIT permission
    try:
        jit_permission = UserJitPermission.objects.get(
            user=request.user,
            permission__codename=permission_codename,
            status='active'
        )

        # Check if the JIT permission is expired
        if jit_permission.status == 'expired':
            return Response({"message": "Permission Expired"}, status=status.HTTP_403_FORBIDDEN)

        # If the JIT permission is active and valid
        return Response({"message": "Success"}, status=status.HTTP_200_OK)

    except UserJitPermission.DoesNotExist:
        # If no JIT permission exists or permission is expired
        return Response({"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
