from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    refresh_token = models.CharField(max_length=255, blank=True, null=True)
    refresh_token_expiration = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user.username

class ModulePermissions(models.Model):
    # Placeholder model
    pass

class UserJitPermission(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('revoked', 'Revoked'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jit_permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    granted_at = models.DateTimeField(default=timezone.now)
    expiration = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def is_expired(self):
        """
        Method to check if the permission has expired based on the expiration time.
        This checks if the current time is past the expiration time.
        """
        if self.status != 'expired' and timezone.now() > self.expiration:
            # If the current time is past expiration, set the status to 'expired'
            self.status = 'expired'
            self.save()  # Save the updated status
            return True
        return False

    def revoke(self):
        """
        Method to manually revoke a permission before expiration.
        """
        self.status = 'revoked'
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.permission.codename} ({self.status})"
