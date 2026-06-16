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
            return super().dispatch(request, *args, **kwargs)
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

    def get_object(self, queryset=None):
        return self.request.user.patient_profile

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Patient.DoesNotExist:
            return redirect("patients:patient_create")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Patient.DoesNotExist:
            return redirect("patients:patient_create")
        return super().post(request, *args, **kwargs)


class PatientDetailView(LoginRequiredMixin, DetailView):

    model = Patient
    template_name = "patients/patient_detail.html"

    def get_object(self, queryset=None):
        return self.request.user.patient_profile

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Patient.DoesNotExist:
            return redirect("patients:patient_create")
        return super().get(request, *args, **kwargs)
