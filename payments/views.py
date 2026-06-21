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

from .models import Payment
from .forms import PaymentForm


class PaymentCreateView(
    LoginRequiredMixin,
    CreateView
):

    model = Payment

    form_class = PaymentForm

    template_name = (
        "payments/payment_form.html"
    )

    success_url = reverse_lazy(
        "appointments:appointment_list"
    )

    def dispatch(self, request, *args, **kwargs):
        self.appointment = get_object_or_404(
            Appointment.objects.select_related("doctor"),
            pk=self.kwargs["appointment_id"],
            patient=request.user,
        )
        if hasattr(self.appointment, "payment"):
            messages.warning(
                request, "This appointment already has a payment."
            )
            return HttpResponseRedirect(
                reverse_lazy("payments:payment_detail", kwargs={
                    "pk": self.appointment.payment.pk
                })
            )
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        return {
            "amount": self.appointment.doctor.consultation_fee,
        }

    def form_valid(self, form):
        form.instance.appointment = self.appointment
        form.instance.amount = self.appointment.doctor.consultation_fee
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["appointment"] = self.appointment
        return context


class PaymentDetailView(
    LoginRequiredMixin,
    DetailView
):

    model = Payment

    template_name = (
        "payments/payment_detail.html"
    )

    context_object_name = "payment"

    def get_queryset(self):
        return Payment.objects.filter(
            appointment__patient=self.request.user
        ).select_related(
            "appointment__doctor__user"
        )


class PaymentListView(
    LoginRequiredMixin,
    ListView
):

    model = Payment

    template_name = (
        "payments/payment_list.html"
    )

    context_object_name = "payments"

    def get_queryset(self):
        return Payment.objects.filter(
            appointment__patient=self.request.user
        ).select_related(
            "appointment__doctor__user"
        )
