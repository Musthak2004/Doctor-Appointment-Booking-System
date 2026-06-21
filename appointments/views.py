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
            "doctor__user"
        )

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
            patient=self.request.user
        ).select_related(
            "doctor__user", "patient"
        )

