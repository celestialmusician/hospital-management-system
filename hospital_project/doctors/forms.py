from django import forms
from .models import Doctor, Category, Availability


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = [
            "profile",
            "name",
            "photo",
            "contact_number",
            "category",
            "experience",
        ]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]


class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = [
            "doctor",
            "date",
            "start_time",
            "end_time",
        ]