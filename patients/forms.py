from django import forms
from .models import Patient


class PatientForm(forms.ModelForm):

    class Meta:
        model = Patient

        fields = (
            "date_of_birth",
            "gender",
            "blood_group",
            "address",
            "emergency_contact",
            "medical_history",
        )