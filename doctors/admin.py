from django.contrib import admin
from .models import Doctor, Specialization, DoctorAvailability, DoctorReview


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "specialization",
        "hospital_name",
        "experience_years",
        "consultation_fee",
        "is_verified",
    )

    list_editable = ("is_verified",)

    list_filter = (
        "specialization",
        "is_verified",
    )

    list_select_related = ("user", "specialization")

    search_fields = (
        "user__username",
        "license_number",
    )


@admin.register(DoctorAvailability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = (
        "doctor",
        "day",
        "start_time",
        "end_time",
        "is_available",
    )

    list_editable = ("is_available",)

    list_filter = ("day",)

    list_select_related = ("doctor__user",)


@admin.register(DoctorReview)
class DoctorReviewAdmin(admin.ModelAdmin):
    list_display = (
        "doctor",
        "patient",
        "rating",
        "created_at",
    )

    list_filter = ("rating",)

    list_select_related = ("doctor__user", "patient")

    search_fields = (
        "doctor__user__username",
        "patient__username",
    )

    date_hierarchy = "created_at"