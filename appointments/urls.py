from django.urls import path

from .views import (
    AppointmentCreateView,
    AppointmentListView,
    AppointmentDetailView,
)

app_name = "appointments"

urlpatterns = [

    path(
        "",
        AppointmentListView.as_view(),
        name="appointment_list"
    ),

    path(
        "create/",
        AppointmentCreateView.as_view(),
        name="appointment_create"
    ),

    path(
        "<int:pk>/",
        AppointmentDetailView.as_view(),
        name="appointment_detail"
    ),
]