import datetime
import random

from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import UserProfile
from .serializers import UserRegistrationSerializer, UserSerializer
from .utils import create_refresh_token, create_access_token, create_access_token_from_refresh


@api_view(['POST'])
@permission_classes([AllowAny])  # Ensures no authentication is required
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save(is_active=False)

        # Generate a 6-digit OTP
        otp = random.randint(100000, 999999)

        # Store OTP in cache for 5 minutes
        cache.set(f"otp_{user.email}", otp, timeout=300)

        # Send OTP via email
        send_mail(
            'Your OTP Code',
            f'Your OTP code is: {otp}. It will expire in 5 minutes.',
            settings.DEFAULT_FROM_EMAIL,  # Use from settings
            [user.email],
            fail_silently=False,
        )

        return Response({"message": "OTP sent to your email. Verify to activate your account."},
                        status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])  # Ensures no authentication is required
def verify_otp(request):
    email = request.data.get('email')
    otp_entered = request.data.get('otp')

    # Retrieve the OTP from cache
    otp_stored = cache.get(f"otp_{email}")

    if otp_stored and str(otp_stored) == str(otp_entered):
        try:
            user = get_user_model().objects.get(email=email)
            user.is_active = True
            user.save()

            # Remove OTP from cache
            cache.delete(f"otp_{email}")

            return Response({"message": "Account verified successfully!"}, status=status.HTTP_200_OK)
        except get_user_model().DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"error": "Invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])  # Ensures no authentication is required
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # Authenticate the user
    user = authenticate(username=username, password=password)

    if not user:
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

    # Create tokens
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    # Check if user has an associated UserProfile
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    # Store the refresh token in the UserProfile
    user_profile.refresh_token = refresh_token
    user_profile.refresh_token_expiration = timezone.now() + datetime.timedelta(days=7)  # Set expiration date
    user_profile.save()

    return Response({
        "access_token": access_token,
        "refresh_token": refresh_token,
    }, status=status.HTTP_200_OK)


# Token Refresh View (Refresh access token using refresh token)
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Authentication required for token refresh
def refresh_token(request):
    refresh_token_value = request.data.get('refresh_token')

    if not refresh_token_value:
        return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Retrieve the stored refresh token from the user profile
        user = request.user

        # Get the associated UserProfile
        user_profile = UserProfile.objects.get(user=user)

        # Check if the provided refresh token matches the one stored in the database
        if user_profile.refresh_token != refresh_token_value:
            return Response({"detail": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST)

        # Generate a new access token using the provided refresh token
        new_access_token = create_access_token_from_refresh(refresh_token_value)
        return Response({"access_token": new_access_token}, status=status.HTTP_200_OK)

    except UserProfile.DoesNotExist:
        return Response({"detail": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Authentication required for accessing profile
def get_user_profile(request):
    try:
        # Get the current authenticated user
        user = request.user

        # Serialize the user with the nested profile and groups/permissions
        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
