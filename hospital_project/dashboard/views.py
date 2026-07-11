from django.shortcuts import render
from django.views import View

from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment, Prescription


class HomeView(View):

    template_name = "dashboard/home.html"

    def get(self, request):

        doctors = Doctor.objects.filter(
            active_status=True
        )[:6]

        context = {

            "total_doctors": Doctor.objects.count(),

            "total_patients": Patient.objects.count(),

            "total_appointments": Appointment.objects.count(),

            "total_prescriptions": Prescription.objects.count(),

            "doctors": doctors,

        }

        return render(
            request,
            self.template_name,
            context,
        )
    
class ContactView(View):

    template_name = "dashboard/contact.html"

    def get(self, request):

        return render(
            request,
            self.template_name,
        )