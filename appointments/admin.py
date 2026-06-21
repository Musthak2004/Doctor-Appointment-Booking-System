from django.contrib import admin

from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "patient",
        "doctor",
        "appointment_date",
        "appointment_time",
        "status",
        "created_at",
    )

    list_select_related = ("patient", "doctor__user")

    search_fields = (
        "patient__email",
        "patient__username",
        "doctor__user__email",
        "doctor__user__username",
    )

    list_filter = (
        "status",
        "appointment_date",
        "doctor",
    )

    list_editable = ("status",)

    date_hierarchy = "appointment_date"

    ordering = ("-appointment_date", "appointment_time")

    readonly_fields = ("created_at", "updated_at")

    actions = ("mark_confirmed", "mark_cancelled")

    @admin.action(description="Mark selected appointments as confirmed")
    def mark_confirmed(self, request, queryset):
        queryset.update(status=Appointment.Status.CONFIRMED)

    @admin.action(description="Mark selected appointments as cancelled")
    def mark_cancelled(self, request, queryset):
        queryset.update(status=Appointment.Status.CANCELLED)