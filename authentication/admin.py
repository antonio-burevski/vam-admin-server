from django.contrib import admin

from authentication.models import UserProfile, UserJitPermission

admin.site.register(UserProfile)
admin.site.register(UserJitPermission)
