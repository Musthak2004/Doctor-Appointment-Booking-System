from django.urls import path

from .views import (
    PaymentCreateView,
    PaymentDetailView,
    PaymentListView,
)

app_name = "payments"

urlpatterns = [

    path(
        "",
        PaymentListView.as_view(),
        name="payment_list"
    ),

    path(
        "create/<int:appointment_id>/",
        PaymentCreateView.as_view(),
        name="payment_create"
    ),

    path(
        "<int:pk>/",
        PaymentDetailView.as_view(),
        name="payment_detail"
    ),
]
