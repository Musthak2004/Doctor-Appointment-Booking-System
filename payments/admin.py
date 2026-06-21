from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "appointment",
        "amount",
        "payment_method",
        "status",
        "paid_at",
        "created_at",
    )

    list_select_related = ("appointment",)

    list_filter = (
        "status",
        "payment_method",
    )

    list_editable = ("status",)

    search_fields = (
        "transaction_id",
        "appointment__id",
    )

    readonly_fields = ("created_at", "updated_at")

    ordering = ("-created_at",)

    actions = ("mark_completed", "mark_refunded")

    @admin.action(description="Mark selected payments as completed")
    def mark_completed(self, request, queryset):
        queryset.update(status=Payment.Status.COMPLETED)

    @admin.action(description="Mark selected payments as refunded")
    def mark_refunded(self, request, queryset):
        queryset.update(status=Payment.Status.REFUNDED)
