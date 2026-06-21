import datetime

from django import forms

from doctors.models import Doctor, DoctorAvailability
from .models import Appointment


WEEKDAY_MAP = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]


class AppointmentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.instance.patient = self.user
        self.fields["doctor"].queryset = (
            Doctor.objects.filter(is_verified=True)
            .select_related("user")
            .order_by("user__first_name")
        )

    class Meta:
        model = Appointment
        fields = (
            "doctor",
            "appointment_date",
            "appointment_time",
            "reason",
        )
        labels = {
            "appointment_date": "Date",
            "appointment_time": "Time",
            "reason": "Reason for visit",
        }
        help_texts = {
            "reason": "Briefly describe your symptoms or reason for the appointment (optional).",
        }
        widgets = {
            "appointment_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "appointment_time": forms.TimeInput(
                attrs={"type": "time"}
            ),
            "reason": forms.Textarea(
                attrs={"rows": 4}
            ),
        }

    def clean_appointment_date(self):
        date = self.cleaned_data["appointment_date"]
        if date < datetime.date.today():
            raise forms.ValidationError("Appointment date cannot be in the past.")
        return date

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("appointment_date")
        time = cleaned_data.get("appointment_time")
        doctor = cleaned_data.get("doctor")

        if not (date and time and doctor):
            return cleaned_data

        if date == datetime.date.today() and time < datetime.datetime.now().time():
            raise forms.ValidationError(
                "Appointment time cannot be in the past for today's date."
            )

        day_code = WEEKDAY_MAP[date.weekday()]
        available = DoctorAvailability.objects.filter(
            doctor=doctor,
            day=day_code,
            is_available=True,
            start_time__lte=time,
            end_time__gt=time,
        ).exists()
        if not available:
            raise forms.ValidationError(
                f"The doctor is not available on {date:%A} at {time}."
            )

        return cleaned_data