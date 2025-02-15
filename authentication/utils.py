import datetime

from rest_framework_simplejwt.tokens import RefreshToken


def create_access_token(user):
    """
    Generates an access token using the JWT refresh token
    """
    refresh = RefreshToken.for_user(user)

    # Set custom expiration time for the access token (e.g., 15 minutes)
    refresh.set_exp(lifetime=datetime.timedelta(minutes=15))  # Adjust as needed

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
