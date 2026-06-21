from django.contrib import admin

from .models import Prescription, PrescriptionItem


class PrescriptionItemInline(admin.TabularInline):

    model = PrescriptionItem

    extra = 1

    fields = ("medicine_name", "dosage", "frequency", "duration", "instructions")


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "appointment",
        "created_at",
    )

    list_select_related = ("appointment",)

    list_filter = ("created_at",)

    search_fields = (
        "appointment__id",
        "diagnosis",
    )

    readonly_fields = ("created_at", "updated_at")

    inlines = [PrescriptionItemInline]

    ordering = ("-created_at",)
