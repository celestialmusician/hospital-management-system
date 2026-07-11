from django.db import models
import uuid


class BaseClass(models.Model):

    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
    )

    active_status = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract = True


class Patient(BaseClass):

    name = models.CharField(
        max_length=100,
    )

    email = models.EmailField(
        unique=True,
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
    )

    age = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True,
    )

    address = models.TextField(
        blank=True,
    )

    photo = models.ImageField(
        upload_to="patient_photos/",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name