from django.urls import path
from .views import DoctorListView, DoctorDetailView, DoctorCreateView, DoctorUpdateView

app_name = "doctors"

urlpatterns = [
    path("", DoctorListView.as_view(), name="doctor_list"),
    path("create/", DoctorCreateView.as_view(), name="doctor_create"),
    path("update/", DoctorUpdateView.as_view(), name="doctor_update"),
    path("<int:pk>/", DoctorDetailView.as_view(), name="doctor_detail"),
]