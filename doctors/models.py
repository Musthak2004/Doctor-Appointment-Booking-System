from django.db import models
from accounts.models import CustomUser


class Specialization(models.Model):

    name = models.CharField(max_length=100, unique=True)

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

    def __str__(self):
        return self.user.username
    
class DoctorAvailability(models.Model):

    DAYS = (
        ("mon", "Monday"),
        ("tue", "Tuesday"),
        ("wed", "Wednesday"),
        ("thu", "Thursday"),
        ("fri", "Friday"),
        ("sat", "Saturday"),
        ("sun", "Sunday"),
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="availability"
    )

    day = models.CharField(
        max_length=10,
        choices=DAYS
    )

    start_time = models.TimeField()

    end_time = models.TimeField()

    is_available = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.doctor.user.username} - {self.day}"

    class Meta:
        unique_together = ("doctor", "day", "start_time")

