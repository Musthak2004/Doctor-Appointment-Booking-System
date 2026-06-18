from django import forms
from .models import Doctor, DoctorAvailability


class DoctorForm(forms.ModelForm):

    class Meta:

        model = Doctor

        fields = (
            "specialization",
            "license_number",
            "experience_years",
            "qualification",
            "hospital_name",
            "consultation_fee",
            "bio",
            "profile_picture",
        )

        widgets = {
            "experience_years": forms.NumberInput(attrs={"min": 0}),
            "consultation_fee": forms.NumberInput(attrs={"min": 0, "step": "0.01"}),
            "bio": forms.Textarea(attrs={"rows": 4, "placeholder": "Tell patients about your background and expertise..."}),
            "profile_picture": forms.FileInput(),
        }

    def clean_consultation_fee(self):
        fee = self.cleaned_data.get("consultation_fee")
        if fee is not None and fee < 0:
            raise forms.ValidationError("Consultation fee cannot be negative.")
        return fee

    def clean_experience_years(self):
        years = self.cleaned_data.get("experience_years")
        if years is not None and years < 0:
            raise forms.ValidationError("Experience years cannot be negative.")
        return years


class AvailabilityForm(forms.ModelForm):

    class Meta:

        model = DoctorAvailability

        fields = (
            "day",
            "start_time",
            "end_time",
            "is_available",
        )

        widgets = {
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "end_time": forms.TimeInput(attrs={"type": "time"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("End time must be after start time.")
        return cleaned_data

