from django.shortcuts import render
from django.views import View

from doctors.models import Doctor,Category,Availability
from patients.models import Patient
from appointments.models import Appointment, Prescription



class HomeView(View):

    template_name = "dashboard/home.html"

    def get(self, request):

        doctors = Doctor.objects.filter(active_status=True)
        categories = Category.objects.filter(active_status=True)

        context = {
            "doctors": doctors,
            "categories": categories,
        }

        return render(request, self.template_name, context)
    
class ContactView(View):

    template_name = "dashboard/contact.html"

    def get(self, request):

        return render(
            request,
            self.template_name,
        )