from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class CustomUser(AbstractUser):

    email = models.EmailField(
        unique=True
    )

    USER_TYPES = (
        ("PATIENT", "Patient"),
        ("DOCTOR", "Doctor"),
        ("ADMIN", "Admin"),
    )

    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPES,
        default="PATIENT",
        db_index=True
    )

    phone_number = models.CharField(
        max_length=15,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    @property
    def has_doctor_profile(self):
        return hasattr(self, 'doctor_profile')

    @property
    def has_patient_profile(self):
        return hasattr(self, 'patient_profile')

    @property
    def safe_doctor_profile(self):
        try:
            return self.doctor_profile
        except ObjectDoesNotExist:
            return None

    @property
    def safe_patient_profile(self):
        try:
            return self.patient_profile
        except ObjectDoesNotExist:
            return None