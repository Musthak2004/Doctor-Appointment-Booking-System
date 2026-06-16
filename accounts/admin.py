from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    model = CustomUser

    list_display = (
        "id",
        "email",
        "username",
        "user_type",
        "phone_number",
        "is_staff",
        "is_active",
    )

    list_filter = (
        "user_type",
        "is_staff",
        "is_active",
    )

    search_fields = (
        "email",
        "username",
        "phone_number",
    )

    ordering = (
        "id",
    )

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal Info", {"fields": ("phone_number", "user_type")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username",
                "email",
                "user_type",
                "phone_number",
                "password1",
                "password2",
                "is_staff",
                "is_active",
            ),
        }),
    )