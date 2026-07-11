from django.urls import path

from .views import (
    DoctorAdminLoginView,
    DoctorAdminLogoutView,
    PatientLoginView,
    VerifyOTPView,
    PatientLogoutView,
)

urlpatterns = [

    
    path(
        "login/",
        DoctorAdminLoginView.as_view(),
        name="doctor-admin-login",
    ),

    path(
        "logout/",
        DoctorAdminLogoutView.as_view(),
        name="doctor-admin-logout",
    ),

    path(
        "patient-login/",
        PatientLoginView.as_view(),
        name="patient-login",
    ),

    path(
        "verify-otp/",
        VerifyOTPView.as_view(),
        name="verify-otp",
    ),

    path(
        "patient-logout/",
        PatientLogoutView.as_view(),
        name="patient-logout",
    ),

]