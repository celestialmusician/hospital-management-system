from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Profile, OTP


@admin.register(Profile)
class ProfileAdmin(UserAdmin):

    list_display = (
        "username",
        "email",
        "role",
        "is_staff",
        "is_active",
    )

    list_filter = (
        "role",
        "is_staff",
        "is_active",
    )

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )

    ordering = (
        "username",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Hospital Information",
            {
                "fields": (
                    "role",
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Hospital Information",
            {
                "fields": (
                    "role",
                )
            },
        ),
    )


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):

    list_display = (
        "profile",
        "otp",
        "created_at",
    )