from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from appointments.models import Appointment
from .models import Review
from .forms import ReviewForm


class ReviewListView(LoginRequiredMixin, ListView):

    model = Review
    template_name = "reviews/review_list.html"
    context_object_name = "reviews"

    def get_queryset(self):
        return Review.objects.filter(
            patient=self.request.user
        ).select_related(
            "doctor__user", "appointment"
        )


class ReviewCreateView(LoginRequiredMixin, CreateView):

    model = Review
    form_class = ReviewForm
    template_name = "reviews/review_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.appointment = get_object_or_404(
            Appointment.objects.select_related("doctor__user"),
            pk=self.kwargs["appointment_id"],
            patient=request.user,
        )
        if hasattr(self.appointment, "review"):
            messages.info(
                request, "You have already reviewed this appointment."
            )
            return HttpResponseRedirect(
                reverse_lazy("reviews:review_detail", kwargs={
                    "pk": self.appointment.review.pk
                })
            )
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        return {}

    def form_valid(self, form):
        form.instance.patient = self.request.user
        form.instance.doctor = self.appointment.doctor
        form.instance.appointment = self.appointment
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "reviews:review_detail",
            kwargs={"pk": self.object.pk}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["appointment"] = self.appointment
        return context


class ReviewDetailView(LoginRequiredMixin, DetailView):

    model = Review
    template_name = "reviews/review_detail.html"
    context_object_name = "review"

    def get_queryset(self):
        return Review.objects.filter(
            patient=self.request.user
        ).select_related(
            "doctor__user", "appointment"
        )
