from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "gender",
        "blood_group",
        "emergency_contact",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
        "blood_group",
    )

    list_filter = (
        "gender",
        "blood_group",
    )

    ordering = ("-created_at",)