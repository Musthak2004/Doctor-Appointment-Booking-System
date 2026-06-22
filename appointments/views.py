from django.db import models
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
)

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.urls import reverse_lazy

from .models import Appointment
from .forms import AppointmentForm


class AppointmentCreateView(
    LoginRequiredMixin,
    CreateView
):

    model = Appointment

    form_class = AppointmentForm

    template_name = (
        "appointments/appointment_form.html"
    )

    success_url = reverse_lazy(
        "appointments:appointment_list"
    )

    def get_initial(self):
        initial = super().get_initial()
        doctor_pk = self.request.GET.get("doctor")
        if doctor_pk:
            initial["doctor"] = doctor_pk
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

class AppointmentListView(
    LoginRequiredMixin,
    ListView
):

    model = Appointment

    template_name = (
        "appointments/appointment_list.html"
    )

    context_object_name = (
        "appointments"
    )

    def get_queryset(self):

        return Appointment.objects.filter(
            patient=self.request.user
        ).select_related(
            "doctor__user", "doctor__specialization"
        ).prefetch_related(
            "payment"
        )

class DoctorAppointmentListView(
    LoginRequiredMixin,
    ListView
):

    model = Appointment

    template_name = (
        "appointments/appointment_list.html"
    )

    context_object_name = (
        "appointments"
    )

    def get_queryset(self):
        return Appointment.objects.filter(
            doctor__user=self.request.user
        ).select_related(
            "patient", "doctor__specialization"
        ).prefetch_related(
            "payment"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_doctor_view"] = True
        return context


class AppointmentDetailView(
    LoginRequiredMixin,
    DetailView
):

    model = Appointment

    template_name = (
        "appointments/appointment_detail.html"
    )

    context_object_name = (
        "appointment"
    )

    def get_queryset(self):
        return Appointment.objects.filter(
            models.Q(patient=self.request.user) |
            models.Q(doctor__user=self.request.user)
        ).select_related(
            "doctor__user", "patient"
        ).prefetch_related(
            "review", "payment"
        )

