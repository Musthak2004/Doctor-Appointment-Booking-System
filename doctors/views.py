from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect

from accounts.mixins import UserTypeRequiredMixin, ProfileExistsMixin, ProfileGetObjectMixin
from .models import Doctor, DoctorAvailability
from .forms import DoctorForm, AvailabilityForm


class DoctorListView(ListView):
    model = Doctor
    template_name = "doctors/doctor_list.html"
    context_object_name = "doctors"
    paginate_by = 20

    def get_queryset(self):
        return Doctor.objects.select_related("user", "specialization")


class DoctorDetailView(DetailView):
    model = Doctor
    template_name = "doctors/doctor_detail.html"
    context_object_name = "doctor"

    def get_queryset(self):
        return Doctor.objects.select_related(
            "user", "specialization"
        ).prefetch_related(
            "availability", "reviews"
        )


class DoctorCreateView(UserTypeRequiredMixin, CreateView):
    required_user_type = "DOCTOR"
    model = Doctor
    form_class = DoctorForm
    template_name = "doctors/doctor_form.html"
    success_url = reverse_lazy("doctors:doctor_list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.user_type != self.required_user_type:
            return redirect("home")
        try:
            request.user.doctor_profile
            return redirect("doctors:doctor_detail", pk=request.user.doctor_profile.pk)
        except Doctor.DoesNotExist:
            return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DoctorUpdateView(ProfileGetObjectMixin, UpdateView):
    profile_attr = "doctor_profile"
    redirect_to = "doctors:doctor_create"
    model = Doctor
    form_class = DoctorForm
    template_name = "doctors/doctor_form.html"
    success_url = reverse_lazy("doctors:doctor_list")


class AvailabilityListView(ProfileExistsMixin, ListView):
    profile_attr = "doctor_profile"
    redirect_to = "doctors:doctor_create"
    model = DoctorAvailability
    template_name = "doctors/availability_list.html"
    context_object_name = "availability_slots"

    def get_queryset(self):
        try:
            doctor = self.request.user.doctor_profile
            return DoctorAvailability.objects.filter(doctor=doctor)
        except Doctor.DoesNotExist:
            return DoctorAvailability.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["doctor"] = self.request.user.doctor_profile
        except Doctor.DoesNotExist:
            context["doctor"] = None
        return context


class AvailabilityCreateView(ProfileExistsMixin, CreateView):
    profile_attr = "doctor_profile"
    redirect_to = "doctors:doctor_create"
    model = DoctorAvailability
    form_class = AvailabilityForm
    template_name = "doctors/availability_form.html"
    success_url = reverse_lazy("doctors:availability_list")

    def form_valid(self, form):
        form.instance.doctor = self.request.user.doctor_profile
        return super().form_valid(form)


class AvailabilityDeleteView(ProfileExistsMixin, DeleteView):
    profile_attr = "doctor_profile"
    redirect_to = "doctors:doctor_create"
    model = DoctorAvailability
    template_name = "doctors/availability_confirm_delete.html"
    success_url = reverse_lazy("doctors:availability_list")

    def get_queryset(self):
        try:
            doctor = self.request.user.doctor_profile
            return DoctorAvailability.objects.filter(doctor=doctor)
        except Doctor.DoesNotExist:
            return DoctorAvailability.objects.none()
