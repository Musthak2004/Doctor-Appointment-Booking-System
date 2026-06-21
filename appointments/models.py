from django.db import models

from accounts.models import CustomUser
from doctors.models import Doctor


class Appointment(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"
        REJECTED = "REJECTED", "Rejected"

    patient = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="appointments",
        limit_choices_to={"user_type": "PATIENT"},
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="appointments",
        db_index=True,
    )

    appointment_date = models.DateField(
        db_index=True,
    )

    appointment_time = models.TimeField()

    reason = models.TextField(
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-appointment_date", "appointment_time"]
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"
        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "appointment_date", "appointment_time"],
                name="unique_doctor_appointment_slot",
            ),
        ]

    def __str__(self):
        return (
            f"{self.patient.email} -> "
            f"{self.doctor.user.email} "
            f"({self.appointment_date} {self.appointment_time})"
        )