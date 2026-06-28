from django.db import models
from accounts.models import CustomUser


class Patient(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="patient_profile"
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True
    )

    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"
        OTHER = "other", "Other"

    gender = models.CharField(
        max_length=10,
        choices=Gender.choices,
        blank=True
    )

    blood_group = models.CharField(
        max_length=5,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    emergency_contact = models.CharField(
        max_length=15,
        blank=True
    )

    medical_history = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Patient"
        verbose_name_plural = "Patients"

    def __str__(self):
        return self.user.username
