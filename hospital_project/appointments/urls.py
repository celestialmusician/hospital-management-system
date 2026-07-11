from django.urls import path
from .views import (
    BookAppointmentView,
    MyAppointmentsView,
    DoctorAppointmentsView,
    AddPrescriptionView,
    MyPrescriptionsView,
    CancelAppointmentView,
)

urlpatterns = [
    path("book/<int:doctor_id>/", BookAppointmentView.as_view(), name="book_appointment"),

    path("my/", MyAppointmentsView.as_view(), name="my_appointments"),

    path("my/prescriptions/", MyPrescriptionsView.as_view(), name="my_prescriptions"),

    path("doctor/", DoctorAppointmentsView.as_view(), name="doctor_appointments"),

    path(
        "prescription/<int:appointment_id>/",

        AddPrescriptionView.as_view(),

        name="add_prescription",
    ),
    path(

        "cancel/<int:pk>/",

        CancelAppointmentView.as_view(),
        
        name="cancel_appointment",
    ),
]