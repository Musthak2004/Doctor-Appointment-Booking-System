from django.db import models

from appointments.models import Appointment


class Payment(models.Model):

    class Method(models.TextChoices):
        CARD = "CARD", "Card"
        PAYPAL = "PAYPAL", "PayPal"
        BANK = "BANK", "Bank Transfer"
        CASH = "CASH", "Cash"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        COMPLETED = "COMPLETED", "Completed"
        FAILED = "FAILED", "Failed"
        REFUNDED = "REFUNDED", "Refunded"

    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name="payment",
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    payment_method = models.CharField(
        max_length=20,
        choices=Method.choices,
    )

    transaction_id = models.CharField(
        max_length=255,
        unique=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )

    paid_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def __str__(self):
        return f"Payment #{self.id} ({self.amount} - {self.get_status_display()})"
