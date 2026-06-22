from django.db import models
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
)

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)

from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages

from appointments.models import Appointment

from .models import Prescription
from .forms import PrescriptionForm


class PrescriptionCreateView(
    LoginRequiredMixin,
    CreateView
):

    model = Prescription

    form_class = PrescriptionForm

    template_name = (
        "prescriptions/prescription_form.html"
    )

    def dispatch(self, request, *args, **kwargs):
        self.appointment = get_object_or_404(
            Appointment.objects.select_related("doctor__user"),
            pk=self.kwargs["appointment_id"],
            doctor__user=request.user,
        )
        if hasattr(self.appointment, "prescription"):
            messages.info(
                request, "This appointment already has a prescription."
            )
            return HttpResponseRedirect(
                reverse_lazy("prescriptions:prescription_detail", kwargs={
                    "pk": self.appointment.prescription.pk
                })
            )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.appointment = self.appointment
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "prescriptions:prescription_detail",
            kwargs={"pk": self.object.pk}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["appointment"] = self.appointment
        return context


class PrescriptionDetailView(
    LoginRequiredMixin,
    DetailView
):

    model = Prescription

    template_name = (
        "prescriptions/prescription_detail.html"
    )

    context_object_name = (
        "prescription"
    )

    def get_queryset(self):
        return Prescription.objects.filter(
            models.Q(appointment__patient=self.request.user) |
            models.Q(appointment__doctor__user=self.request.user)
        ).select_related(
            "appointment__doctor__user",
            "appointment"
        ).prefetch_related(
            "items"
        )


class PrescriptionListView(
    LoginRequiredMixin,
    ListView
):

    model = Prescription

    template_name = (
        "prescriptions/prescription_list.html"
    )

    context_object_name = (
        "prescriptions"
    )

    def get_queryset(self):
        return Prescription.objects.filter(
            appointment__patient=self.request.user
        ).select_related(
            "appointment__doctor__user",
        ).prefetch_related(
            "items"
        )


class DoctorPrescriptionListView(
    LoginRequiredMixin,
    ListView
):

    model = Prescription

    template_name = (
        "prescriptions/prescription_list.html"
    )

    context_object_name = (
        "prescriptions"
    )

    def get_queryset(self):
        return Prescription.objects.filter(
            appointment__doctor__user=self.request.user
        ).select_related(
            "appointment__patient",
        ).prefetch_related(
            "items"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_doctor_view"] = True
        return context
