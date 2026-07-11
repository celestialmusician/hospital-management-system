from django import forms
from .models import Patient


class PatientProfileForm(forms.ModelForm):

    class Meta:

        model = Patient

        fields = [
            "name",
            "phone",
            "age",
            "gender",
            "address",
            "photo",
        ]

        widgets = {

            "name": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "phone": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "age": forms.NumberInput(
                attrs={"class": "form-control"}
            ),

            "gender": forms.Select(
                attrs={"class": "form-select"}
            ),

            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),

            "photo": forms.FileInput(
                attrs={"class": "form-control"}
            ),
        }