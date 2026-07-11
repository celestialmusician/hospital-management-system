from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib import messages
import threading

from .forms import DoctorAdminLoginForm, PatientLoginForm
from .models import Profile, OTP
from hospital_project.utility import send_email
from patients.models import Patient



class DoctorAdminLoginView(View):

    template = "accounts/login.html"
    form_class = DoctorAdminLoginForm

    def get(self, request, *args, **kwargs):

        form = self.form_class()

        return render(
            request,
            self.template,
            {
                "form": form,
            },
        )

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)

        error = None

        if form.is_valid():

            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = authenticate(
                username=email,
                password=password,
            )

            if user:

                print("========== LOGIN DEBUG ==========")
                print("Email :", user.email)
                print("Role  :", user.role)
                print("================================")

                login(request, user)

                if user.role == "Doctor":
                    return redirect("doctor-dashboard")

                return redirect("home")

            error = "Invalid Email or Password"

        return render(
            request,
            self.template,
            {
                "form": form,
                "error": error,
            },
        )




class DoctorAdminLogoutView(View):

    def get(self, request, *args, **kwargs):

        logout(request)

        return redirect("doctor-admin-login")




class PatientLoginView(View):

    template = "accounts/patient-login.html"
    form_class = PatientLoginForm

    def get(self, request, *args, **kwargs):

        form = self.form_class()

        return render(
            request,
            self.template,
            {
                "form": form,
            },
        )

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)

        if not form.is_valid():

            return render(
                request,
                self.template,
                {
                    "form": form,
                },
            )

        email = form.cleaned_data["email"]

        user = Profile.objects.filter(
            email=email,
            role="Patient",
        ).first()

        if not user:

            username = email.split("@")[0]

            user = Profile.objects.create(
                username=username,
                email=email,
                first_name=username,
                role="Patient",
            )

        # Dummy password (OTP login only)
            user.set_password("patient123")
            user.save()

        otp_obj, created = OTP.objects.get_or_create(
            profile=user
        )

        otp = otp_obj.generate_otp()

        request.session["patient_email"] = user.email

        template = "emails/otp.html"

        subject = "Hospital Management System - OTP"

        context = {
            "user": user.first_name or user.username,
            "otp": otp,
        }

        try:

            thread = threading.Thread(
                target=send_email,
                args=(
                    user.email,
                    template,
                    subject,
                    context,
                ),
            )

            thread.start()

        except Exception as e:

            print(e)

            messages.error(
                request,
                "Unable to send OTP email."
            )

            return render(
                request,
                self.template,
                {
                    "form": form,
                },
            )

        messages.success(
            request,
            "OTP has been sent to your email."
        )

        return redirect("verify-otp")
    

class VerifyOTPView(View):

    template = "accounts/verify_otp.html"

    def get(self, request, *args, **kwargs):

        if not request.session.get("patient_email"):

            messages.error(
                request,
                "Please login first."
            )

            return redirect("patient-login")

        return render(
            request,
            self.template,
        )

    def post(self, request, *args, **kwargs):

        email = request.session.get("patient_email")

        if not email:

            messages.error(
                request,
                "Session expired. Please login again."
            )

            return redirect("patient-login")

        otp = request.POST.get("otp", "").strip()

        try:

            user = Profile.objects.get(
                email=email,
                role="Patient",
            )

            otp_record = OTP.objects.get(
                profile=user,
            )

        except (Profile.DoesNotExist, OTP.DoesNotExist):

            messages.error(
                request,
                "Invalid user."
            )

            return redirect("patient-login")

        if str(otp_record.otp).strip() == str(otp).strip():

            # Create Patient record if it doesn't already exist
            Patient.objects.get_or_create(
                email=user.email,
                defaults={
                    "name": user.first_name or user.username,
                },
            )

            request.session["patient_logged_in"] = True
            request.session["patient_email"] = user.email
            request.session["patient_id"] = user.id

            messages.success(
                request,
                f"Welcome {user.first_name or user.username}!"
            )

            return redirect("patient_home")

        messages.error(
            request,
            "Invalid OTP. Please try again."
        )

        return render(
            request,
            self.template,
        )



class PatientLogoutView(View):

    def get(self, request, *args, **kwargs):

        request.session.flush()

        logout(request)

        messages.success(
            request,
            "Logged out successfully."
        )

        return redirect("patient-login")