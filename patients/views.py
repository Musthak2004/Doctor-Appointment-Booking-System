from django.views.generic import CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import redirect

from accounts.mixins import UserTypeRequiredMixin, ProfileGetObjectMixin
from .models import Patient
from .forms import PatientForm


class PatientCreateView(UserTypeRequiredMixin, CreateView):
    required_user_type = "PATIENT"
    model = Patient
    form_class = PatientForm
    template_name = "patients/patient_form.html"
    success_url = reverse_lazy("patients:patient_detail")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.user_type != self.required_user_type:
            return redirect("home")
        try:
            request.user.patient_profile
            return redirect("patients:patient_detail")
        except Patient.DoesNotExist:
            return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PatientUpdateView(ProfileGetObjectMixin, UpdateView):
    profile_attr = "patient_profile"
    redirect_to = "patients:patient_create"
    model = Patient
    form_class = PatientForm
    template_name = "patients/patient_form.html"
    success_url = reverse_lazy("patients:patient_detail")


class PatientDetailView(ProfileGetObjectMixin, DetailView):
    profile_attr = "patient_profile"
    redirect_to = "patients:patient_create"
    model = Patient
    template_name = "patients/patient_detail.html"
