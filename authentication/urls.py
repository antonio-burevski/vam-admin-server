from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import register_user, verify_otp, login_user, refresh_token, get_user_profile, dashboard, products, account, \
    settings, add_new_product, delete_product, update_product, add_new_discount, update_discount, delete_discount, \
    update_account, update_settings, request_permission

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('login/', login_user, name='login'),
    path('refresh/', refresh_token, name='token_refresh'),  # Custom refresh token endpoint
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Simple JWT obtain pair
    path('user-profile/', get_user_profile, name='user_profile'),
    path('request-permission/', request_permission, name='request_permission'),
    path('dashboard/', dashboard, name='dashboard'),
    path('products/', products, name='products'),
    path('account/', account, name='account'),
    path('settings/', settings, name='settings'),
    path('add-new-product/', add_new_product, name='add_new_product'),
    path('update-product/', update_product, name='update_product'),
    path('delete-product/', delete_product, name='delete_product'),
    path('add-new-discount/', add_new_discount, name='add_new_discount'),
    path('update-discount/', update_discount, name='update_discount'),
    path('delete-discount/', delete_discount, name='delete_discount'),
    path('update-account/', update_account, name='update_account'),
    path('update-settings/', update_settings, name='update_settings'),
]
