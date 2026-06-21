from django.urls import path

from .views import (
    PrescriptionCreateView,
    PrescriptionDetailView,
    PrescriptionListView,
)

app_name = "prescriptions"

urlpatterns = [

    path(
        "",
        PrescriptionListView.as_view(),
        name="prescription_list"
    ),

    path(
        "create/<int:appointment_id>/",
        PrescriptionCreateView.as_view(),
        name="prescription_create"
    ),

    path(
        "<int:pk>/",
        PrescriptionDetailView.as_view(),
        name="prescription_detail"
    ),
]
