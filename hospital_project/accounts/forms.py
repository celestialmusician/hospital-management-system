from django import forms


class DoctorAdminLoginForm(forms.Form):

    email = forms.EmailField(
    widget=forms.EmailInput(
        attrs={
            "class": "form-control",
            "placeholder": "Enter your email address",
            "autocomplete": "email",
            "required": "required",
        }
    )
)

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "required": "required",
            }
        )
    )


class PatientLoginForm(forms.Form):

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "required": "required",
            }
        )
    )

    def clean_email(self):

        email = self.cleaned_data.get("email")

        allowed_domains = [
            "gmail.com",
            "yahoo.com",
            "outlook.com",
            "mailinator.com",
        ]

        domain = email.split("@")[1]

        if domain not in allowed_domains:
            raise forms.ValidationError(
                "Invalid email domain."
            )

        return email