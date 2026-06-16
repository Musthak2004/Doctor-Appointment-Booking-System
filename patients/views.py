from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

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
    
class PatientUpdateView(LoginRequiredMixin, UpdateView):

    model = Patient
    form_class = PatientForm
    template_name = "patients/patient_form.html"

    def get_object(self):
        return self.request.user.patient_profile

class PatientDetailView(LoginRequiredMixin, DetailView):

    model = Patient
    template_name = "patients/patient_detail.html"

    def get_object(self):
        return self.request.user.patient_profile