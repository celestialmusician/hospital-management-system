from django.contrib import admin
from .models import Category, Doctor, Availability


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "active_status",
    )

    search_fields = (
        "name",
    )


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "category",
        "experience",
        "contact_number",
        "active_status",
    )

    search_fields = (
        "name",
        "category__name",
    )

    list_filter = (
        "category",
    )


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):

    list_display = (
        "doctor",
        "date",
        "start_time",
        "end_time",
    )

    list_filter = (
        "date",
    )