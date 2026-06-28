from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect

from .models import Patient
from .forms import PatientForm


class PatientCreateView(LoginRequiredMixin, CreateView):

    model = Patient
    form_class = PatientForm
    template_name = "patients/patient_form.html"
    success_url = reverse_lazy("patients:patient_detail")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.user_type != "PATIENT":
            return redirect("home")
        try:
            request.user.patient_profile
            return redirect("patients:patient_detail")
        except Patient.DoesNotExist:
            return super().dispatch(request, *args, **kwargs)


class PatientUpdateView(LoginRequiredMixin, UpdateView):

    model = Patient
    form_class = PatientForm
    template_name = "patients/patient_form.html"
    success_url = reverse_lazy("patients:patient_detail")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        try:
            self.object = self.request.user.patient_profile
        except Patient.DoesNotExist:
            return redirect("patients:patient_create")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.object


class PatientDetailView(LoginRequiredMixin, DetailView):

    model = Patient
    template_name = "patients/patient_detail.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        try:
            self.object = self.request.user.patient_profile
        except Patient.DoesNotExist:
            return redirect("patients:patient_create")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.object
