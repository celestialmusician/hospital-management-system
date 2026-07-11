from django.shortcuts import render, get_object_or_404
from django.views.generic import View

from .models import Doctor, Category, Availability

from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache


@method_decorator(never_cache, name="dispatch")
class DashboardView(View):

    template_name = "doctors/dashboard.html"

    def get(self, request):

        total_doctors = Doctor.objects.count()
        total_categories = Category.objects.count()
        total_availability = Availability.objects.count()

        context = {
            "total_doctors": total_doctors,
            "total_categories": total_categories,
            "total_availability": total_availability,
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