from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import View

from .models import Doctor, Category, Availability

from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from appointments.models import Appointment, Prescription

@method_decorator(never_cache, name="dispatch")


class DashboardView(View):

    template_name = "doctors/dashboard.html"

    def get(self, request):

        if not request.user.is_authenticated:

            return redirect("doctor-admin-login")

        doctor = get_object_or_404(
            Doctor,
            profile=request.user,
        )

        appointments = Appointment.objects.filter(
            doctor=doctor,
        ).select_related(
            "patient",
        ).order_by("-date")

        prescriptions = Prescription.objects.filter(
            appointment__doctor=doctor,
        ).select_related(
            "appointment",
            "appointment__patient",
        ).order_by("-appointment__date")

        total_patients = appointments.values(
            "patient"
        ).distinct().count()

        upcoming = appointments.filter(
            status="Upcoming",
        ).count()

        completed = appointments.filter(
            status="Completed",
        ).count()

        cancelled = appointments.filter(
            status="Cancelled",
        ).count()

        context = {

            "doctor": doctor,

            "appointments": appointments,

            "prescriptions": prescriptions,

            "total_patients": total_patients,

            "total_appointments": appointments.count(),

            "total_prescriptions": prescriptions.count(),

            "upcoming": upcoming,

            "completed": completed,

            "cancelled": cancelled,

        }

        return render(
            request,
            self.template_name,
            context,
        )


class DoctorListView(View):

    template_name = "doctors/doctor_list.html"

    def get(self, request):

        category_id = request.GET.get("category")
        search = request.GET.get("search")

        categories = Category.objects.all().order_by("name")

        doctors = Doctor.objects.select_related(
            "category"
        ).filter(
            active_status=True
        )

        if category_id:
            doctors = doctors.filter(category_id=category_id)

        if search:
            doctors = doctors.filter(
                name__icontains=search
            )

        context = {
            "categories": categories,
            "doctors": doctors,
            "selected_category": category_id,
            "search": search,
        }

        return render(
            request,
            self.template_name,
            context,
        )


class DoctorDetailView(View):

    template_name = "doctors/doctor_detail.html"

    def get(self, request, pk):

        doctor = get_object_or_404(
            Doctor,
            pk=pk,
            active_status=True,
        )

        availability = Availability.objects.filter(
            doctor=doctor,
            active_status=True,
        ).order_by("date", "start_time")

        context = {
            "doctor": doctor,
            "availability": availability,
        }

        return render(
            request,
            self.template_name,
            context,
        )


class AvailabilityListView(View):

    template_name = "doctors/availability_list.html"

    def get(self, request):

        availability = Availability.objects.select_related(
            "doctor"
        ).filter(
            active_status=True
        ).order_by(
            "date",
            "start_time",
        )

        return render(
            request,
            self.template_name,
            {
                "availability": availability,
            },
        )