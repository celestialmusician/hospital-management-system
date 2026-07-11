from django.db import models


class Appointment(models.Model):

    STATUS_CHOICES = (
        ("Upcoming", "Upcoming"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    )

    patient = models.ForeignKey(
        "patients.Patient",
        on_delete=models.CASCADE,
        related_name="appointments",
    )

    doctor = models.ForeignKey(
        "doctors.Doctor",
        on_delete=models.CASCADE,
        related_name="appointments",
    )

    date = models.DateField()

    time_slot = models.CharField(
        max_length=50,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Upcoming",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.patient.name} - {self.doctor.name}"


class Prescription(models.Model):

    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name="prescription",
    )

    medicines = models.TextField()

    dosage = models.TextField()

    notes = models.TextField(
        blank=True,
    )

    follow_up_date = models.DateField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Prescription - {self.appointment.patient.name}"