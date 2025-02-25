from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import ModulePermissions


@receiver(post_migrate)
def create_permissions_and_groups(sender, **kwargs):
    content_type = ContentType.objects.get_for_model(ModulePermissions)
    permissions = [
        ('can_view_dashboard', 'Can view dashboard'),
        ('can_view_products', 'Can view products'),
        ('can_view_account', 'Can view account'),
        ('can_view_settings', 'Can view settings'),
        ('can_add_products', 'Can add products'),
        ('can_update_products', 'Can update products'),
        ('can_delete_products', 'Can delete products'),
        ('can_add_discounts', 'Can add discounts'),
        ('can_update_discounts', 'Can update discounts'),
        ('can_delete_discounts', 'Can delete discounts'),
        ('can_update_account', 'Can update account settings'),
        ('can_update_settings', 'Can update settings'),
    ]

    # Create each permission if it does not already exist
    for codename, name in permissions:
        Permission.objects.get_or_create(
            codename=codename,
            name=name,
            content_type=content_type
        )

    # Define groups and the associated permissions
    groups_permissions = {
        "Admin": [
            "can_view_dashboard", "can_view_products", "can_view_account", "can_view_settings",
            "can_add_products", "can_update_products", "can_delete_products",
            "can_add_discounts", "can_update_discounts", "can_delete_discounts",
            "can_update_account", "can_update_settings"
        ],
        "Manager": [
            "can_view_dashboard", "can_view_products", "can_view_account", "can_view_settings",
            "can_add_products", "can_update_products", "can_delete_products",
            "can_add_discounts", "can_update_discounts", "can_delete_discounts",
            "can_update_account"
        ],
        "Product Manager": [
            "can_view_dashboard", "can_view_products", "can_view_account",
            "can_add_products", "can_update_products", "can_delete_products",
            "can_add_discounts", "can_update_discounts", "can_delete_discounts"
        ],
        "Account Manager": [
            "can_view_dashboard", "can_view_account", "can_view_settings",
            "can_update_account", "can_update_settings"
        ],
        "Viewer": [
            "can_view_dashboard", "can_view_products", "can_view_account", "can_view_settings"
        ]
    }

    # Create the groups and assign the corresponding permissions
    for group_name, perm_codes in groups_permissions.items():
        group, created = Group.objects.get_or_create(name=group_name)

        # Assign permissions to the group
        for perm_code in perm_codes:
            permission = Permission.objects.get(codename=perm_code)
            group.permissions.add(permission)

        group.save()
