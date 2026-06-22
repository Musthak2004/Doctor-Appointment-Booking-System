from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "patient",
        "doctor",
        "appointment",
        "rating",
        "created_at",
    )

    list_select_related = ("patient", "doctor__user", "appointment")

    list_filter = (
        "rating",
        "created_at",
    )

    search_fields = (
        "patient__username",
        "patient__email",
        "doctor__user__username",
    )

    date_hierarchy = "created_at"

    readonly_fields = ("created_at", "updated_at")

    ordering = (
        "-created_at",
    )