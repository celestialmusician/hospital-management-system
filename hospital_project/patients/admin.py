from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "email",
        "phone",
        "age",
        "gender",
        "active_status",
    )

    search_fields = (
        "name",
        "email",
        "phone",
    )

    list_filter = (
        "gender",
        "active_status",
    )