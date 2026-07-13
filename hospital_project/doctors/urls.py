from django.urls import path

from .views import (
    DashboardView,
    DoctorListView,
    DoctorDetailView,
    AvailabilityListView,
    DoctorProfileView,
    DoctorProfileUpdateView,
)

urlpatterns = [

    path(
        "dashboard/",
        DashboardView.as_view(),
        name="doctor-dashboard",
    ),

    path(
        "",
        DoctorListView.as_view(),
        name="doctor_list",
    ),

    path(
        "<int:pk>/",
        DoctorDetailView.as_view(),
        name="doctor_detail",
    ),

    path(
        "availability/",
        AvailabilityListView.as_view(),
        name="availability-list",
    ),


    path(
        "profile/",
        DoctorProfileView.as_view(),
        name="doctor-profile",
    ),

    path(
        "profile/edit/",
        DoctorProfileUpdateView.as_view(),
        name="doctor-profile-edit",
    ),
]