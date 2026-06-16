from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect

from .models import Doctor
from .forms import DoctorForm


class DoctorListView(ListView):

    model = Doctor
    template_name = "doctors/doctor_list.html"
    context_object_name = "doctors"

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


class DoctorCreateView(LoginRequiredMixin, CreateView):

    model = Doctor
    form_class = DoctorForm
    template_name = "doctors/doctor_form.html"
    success_url = reverse_lazy("doctors:doctor_list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        try:
            request.user.doctor_profile
            return redirect("doctors:doctor_detail", pk=request.user.doctor_profile.pk)
        except Doctor.DoesNotExist:
            return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DoctorUpdateView(LoginRequiredMixin, UpdateView):

    model = Doctor
    form_class = DoctorForm
    template_name = "doctors/doctor_form.html"
    success_url = reverse_lazy("doctors:doctor_list")

    def get_object(self, queryset=None):
        try:
            return self.request.user.doctor_profile
        except Doctor.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj is None:
            return redirect("doctors:doctor_create")
        self.object = obj
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj is None:
            return redirect("doctors:doctor_create")
        self.object = obj
        return super().post(request, *args, **kwargs)