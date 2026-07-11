from django.db import models
from django.contrib.auth.models import AbstractUser
import random


class RoleChoices(models.TextChoices):

    ADMIN = "Admin", "Admin"
    PATIENT = "Patient", "Patient"
    DOCTOR = "Doctor", "Doctor"


class Profile(AbstractUser):

    role = models.CharField(
        max_length=10,
        choices=RoleChoices.choices,
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "Profiles"


class OTP(models.Model):

    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name="otp_record",
    )

    otp = models.CharField(max_length=4)

    created_at = models.DateTimeField(
        auto_now=True,
    )

    def generate_otp(self):

        self.otp = str(random.randint(1000, 9999))

        self.save()

        return self.otp

    def __str__(self):

        return f"{self.profile.email} - {self.otp}"

    class Meta:

        verbose_name_plural = "OTP Records"