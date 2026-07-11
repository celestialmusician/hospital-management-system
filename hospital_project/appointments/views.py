from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib import messages
from django.utils import timezone

from doctors.models import Doctor, Availability
from patients.models import Patient
from .models import Appointment, Prescription


class BookAppointmentView(View):

    template_name = "appointments/book_appointment.html"

    def get(self, request, doctor_id):

        doctor = get_object_or_404(
            Doctor,
            id=doctor_id,
        )

        available_dates = Availability.objects.filter(
            doctor=doctor,
            date__gte=timezone.now().date(),
        ).order_by("date")

        context = {
            "doctor": doctor,
            "available_dates": available_dates,
        }

        return render(
            request,
            self.template_name,
            context,
        )

    def post(self, request, doctor_id):

        doctor = get_object_or_404(
            Doctor,
            id=doctor_id,
        )

        email = request.session.get("patient_email")

        if not email:

            messages.error(
                request,
                "Please log in first."
            )

            return redirect("patient-login")

        patient, created = Patient.objects.get_or_create(
            email=email,
            defaults={
                "name": email.split("@")[0],
            },
        )

        date = request.POST.get("date")

        time_slot = request.POST.get(
            "time_slot",
            "",
        )

        appointment_exists = Appointment.objects.filter(
            patient=patient,
            doctor=doctor,
            date=date,
            time_slot=time_slot,
        ).exists()

        if appointment_exists:

            messages.warning(
                request,
                "Appointment already booked."
            )

            return redirect("my_appointments")

        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            date=date,
            time_slot=time_slot,
        )

        messages.success(
            request,
            "Appointment booked successfully."
        )

        return redirect("my_appointments")


class MyAppointmentsView(View):

    template_name = "appointments/my_appointments.html"

    def get(self, request):

        email = request.session.get("patient_email")

        if not email:

            return redirect("patient-login")

        patient = Patient.objects.filter(
            email=email,
        ).first()

        appointments = []

        if patient:

            appointments = Appointment.objects.filter(
                patient=patient,
            )

        return render(
            request,
            self.template_name,
            {
                "appointments": appointments,
            },
        )


class DoctorAppointmentsView(View):

    template_name = "appointments/doctor_appointments.html"

    def get(self, request):

        if not request.user.is_authenticated:

            return redirect("doctor-admin-login")

        doctor = Doctor.objects.filter(
            profile=request.user,
        ).first()

        appointments = []

        if doctor:

            appointments = Appointment.objects.filter(
                doctor=doctor,
            )

        return render(
            request,
            self.template_name,
            {
                "appointments": appointments,
            },
        )


class AddPrescriptionView(View):

    template_name = "appointments/add_prescription.html"

    def get(self, request, appointment_id):

        appointment = get_object_or_404(
            Appointment,
            id=appointment_id,
        )

        return render(
            request,
            self.template_name,
            {
                "appointment": appointment,
            },
        )

    def post(self, request, appointment_id):

        appointment = get_object_or_404(
            Appointment,
            id=appointment_id,
        )

        Prescription.objects.update_or_create(
            appointment=appointment,
            defaults={
                "medicines": request.POST.get(
                    "medicines",
                    "",
                ),
                "dosage": request.POST.get(
                    "dosage",
                    "",
                ),
                "notes": request.POST.get(
                    "notes",
                    "",
                ),
                "follow_up_date": request.POST.get(
                    "follow_up_date"
                ) or None,
            },
        )

        appointment.status = "Completed"

        appointment.save()

        messages.success(
            request,
            "Prescription added successfully."
        )

        return redirect("doctor_appointments")
    
class MyPrescriptionsView(View):

    template_name = "appointments/my_prescriptions.html"

    def get(self, request):

        email = request.session.get("patient_email")

        if not email:
            return redirect("patient-login")

        patient = Patient.objects.filter(email=email).first()

        prescriptions = Prescription.objects.filter(
            appointment__patient=patient
        ).select_related(
            "appointment",
            "appointment__doctor",
        )

        return render(
            request,
            self.template_name,
            {
                "prescriptions": prescriptions,
            },
        )
    
class CancelAppointmentView(View):

    def get(self, request, pk):

        email = request.session.get("patient_email")

        if not email:
            return redirect("patient-login")

        patient = Patient.objects.filter(email=email).first()

        appointment = get_object_or_404(
            Appointment,
            pk=pk,
            patient=patient,
        )

        if appointment.status == "Upcoming":

            appointment.status = "Cancelled"

            appointment.save()

            messages.success(
                request,
                "Appointment cancelled successfully."
            )

        else:

            messages.warning(
                request,
                "This appointment cannot be cancelled."
            )

        return redirect("my_appointments")