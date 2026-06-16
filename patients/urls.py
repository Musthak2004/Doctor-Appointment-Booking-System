from django.urls import path
from .views import (
    PatientCreateView,
    PatientUpdateView,
    PatientDetailView
)

app_name = "patients"

urlpatterns = [
    path("create/", PatientCreateView.as_view(), name="patient_create"),
    path("profile/", PatientDetailView.as_view(), name="patient_detail"),
    path("update/", PatientUpdateView.as_view(), name="patient_update"),
]