from django.urls import path
from .views import PatientHomeView,EditPatientProfileView, PatientProfileView

urlpatterns = [
    path(
        "home/",
        PatientHomeView.as_view(),
        name="patient_home",
    ),

    path(
    "profile/",
    PatientProfileView.as_view(),
    name="patient_profile",
),

path(
    "profile/edit/",
    EditPatientProfileView.as_view(),
    name="edit_patient_profile",
),
]