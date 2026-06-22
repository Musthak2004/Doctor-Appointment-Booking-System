from django.urls import path
from .views import (
    DoctorListView, DoctorDetailView, DoctorCreateView, DoctorUpdateView,
    AvailabilityListView, AvailabilityCreateView, AvailabilityDeleteView,
)

app_name = "doctors"

urlpatterns = [
    path("", DoctorListView.as_view(), name="doctor_list"),
    path("create/", DoctorCreateView.as_view(), name="doctor_create"),
    path("update/", DoctorUpdateView.as_view(), name="doctor_update"),
    path("<int:pk>/", DoctorDetailView.as_view(), name="doctor_detail"),
    path("availability/", AvailabilityListView.as_view(), name="availability_list"),
    path("availability/create/", AvailabilityCreateView.as_view(), name="availability_create"),
    path("availability/<int:pk>/delete/", AvailabilityDeleteView.as_view(), name="availability_delete"),
]