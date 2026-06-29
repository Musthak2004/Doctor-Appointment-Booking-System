from django.core.exceptions import ValidationError
from django.db import models
from accounts.models import CustomUser


class Specialization(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Specialization"
        verbose_name_plural = "Specializations"

    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="doctor_profile"
    )

    specialization = models.ForeignKey(
        Specialization,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    license_number = models.CharField(
        max_length=100,
        unique=True
    )

    experience_years = models.PositiveIntegerField(
        default=0
    )

    qualification = models.CharField(
        max_length=255,
        blank=True
    )

    hospital_name = models.CharField(
        max_length=255,
        blank=True
    )

    consultation_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )

    bio = models.TextField(
        blank=True
    )

    profile_picture = models.ImageField(
        upload_to="doctors/profiles/",
        blank=True,
    )

    is_verified = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"

    def __str__(self):
        return self.user.username


class DoctorAvailability(models.Model):
    class Day(models.TextChoices):
        MONDAY = "mon", "Monday"
        TUESDAY = "tue", "Tuesday"
        WEDNESDAY = "wed", "Wednesday"
        THURSDAY = "thu", "Thursday"
        FRIDAY = "fri", "Friday"
        SATURDAY = "sat", "Saturday"
        SUNDAY = "sun", "Sunday"

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="availability"
    )

    day = models.CharField(
        max_length=10,
        choices=Day.choices
    )

    start_time = models.TimeField()

    end_time = models.TimeField()

    is_available = models.BooleanField(
        default=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        unique_together = ("doctor", "day", "start_time")
        ordering = ["doctor", "day", "start_time"]
        verbose_name = "Doctor Availability"
        verbose_name_plural = "Doctor Availabilities"

    def clean(self):
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time.")

    def __str__(self):
        return f"{self.doctor.user.username} - {self.day}"
