from django.contrib import admin
from .models import Appointment, Prescription


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "patient",
        "doctor",
        "date",
        "time_slot",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "date",
        "doctor",
    )

    search_fields = (
        "patient__name",
        "patient__email",
        "doctor__name",
    )

    ordering = (
        "-created_at",
    )


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "appointment",
        "follow_up_date",
    )

    search_fields = (
        "appointment__patient__name",
        "appointment__doctor__name",
    )