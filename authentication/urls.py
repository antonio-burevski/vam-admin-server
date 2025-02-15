from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import register_user, verify_otp, login_user, refresh_token, get_user_profile

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('login/', login_user, name='login'),
    path('refresh/', refresh_token, name='token_refresh'),  # Custom refresh token endpoint
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Simple JWT obtain pair
    path('user-profile/', get_user_profile, name='user_profile'),  # Protected user profile endpoint
]
