from django.contrib import messages

from django.shortcuts import render, redirect
from django.views import View

from doctors.models import Category

from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from .forms import PatientProfileForm
from .models import Patient

from doctors.models import Doctor
from appointments.models import Appointment, Prescription

    
@method_decorator(never_cache, name="dispatch")

class PatientHomeView(View):

    template_name = "patients/patient_home.html"

    def get(self, request):

        if not request.session.get("patient_logged_in"):
            return redirect("home")

        patient_email = request.session.get("patient_email")

        categories = Category.objects.filter(active_status=True)

        doctors = Doctor.objects.all()[:6]

        upcoming_appointments = Appointment.objects.filter(
            patient__email=patient_email
        ).order_by("date", "time")

        prescriptions = Prescription.objects.filter(
            appointment__patient__email=patient_email
        ).order_by("-id")

        context = {
            "patient_email": patient_email,
            "categories": categories,
            "doctors": doctors,
            "upcoming_appointments": upcoming_appointments,
            "prescriptions": prescriptions,

            "reports": [],
            "notifications": [],
            "medical_history": [],
        }

        return render(
            request,
            self.template_name,
            context,
        )

    template_name = "patients/patient_home.html"

    def get(self, request):

        if not request.session.get("patient_logged_in"):
            return redirect("home")

        categories = Category.objects.filter(
            active_status=True
        )

        context = {
            "patient_email": request.session.get("patient_email"),
            "categories": categories,
        }

        return render(
            request,
            self.template_name,
            context,
        )
    
class PatientProfileView(View):

    template_name = "patients/profile.html"

    def get(self, request):

        email = request.session.get("patient_email")

        if not email:
            return redirect("patient-login")

        patient = Patient.objects.filter(email=email).first()

        return render(
            request,
            self.template_name,
            {
                "patient": patient,
            },
        )


class EditPatientProfileView(View):

    template_name = "patients/edit_profile.html"

    def get(self, request):

        email = request.session.get("patient_email")

        if not email:
            return redirect("patient-login")

        patient, created = Patient.objects.get_or_create(
            email=email,
            defaults={
                "name": email.split("@")[0],
            },
        )

        form = PatientProfileForm(instance=patient)

        return render(
            request,
            self.template_name,
            {
                "form": form,
            },
        )

    def post(self, request):

        email = request.session.get("patient_email")

        if not email:
            return redirect("patient-login")

        patient, created = Patient.objects.get_or_create(
            email=email,
            defaults={
                "name": email.split("@")[0],
            },
        )

        form = PatientProfileForm(
            request.POST,
            request.FILES,
            instance=patient,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Profile Updated Successfully."
            )

            return redirect("patient_profile")

        return render(
            request,
            self.template_name,
            {
                "form": form,
            },
        )