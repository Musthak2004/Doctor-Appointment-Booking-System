from django import forms

from .models import Prescription, PrescriptionItem


class PrescriptionForm(forms.ModelForm):

    class Meta:
        model = Prescription
        fields = (
            "diagnosis",
            "notes",
        )
        widgets = {
            "diagnosis": forms.Textarea(
                attrs={"rows": 3, "class": "form__input"}
            ),
            "notes": forms.Textarea(
                attrs={"rows": 3, "class": "form__input"}
            ),
        }
        labels = {
            "diagnosis": "Diagnosis",
            "notes": "Additional Notes",
        }
        help_texts = {
            "notes": "Optional notes about the prescription.",
        }


class PrescriptionItemForm(forms.ModelForm):

    class Meta:
        model = PrescriptionItem
        fields = (
            "medicine_name",
            "dosage",
            "frequency",
            "duration",
            "instructions",
        )
        widgets = {
            "medicine_name": forms.TextInput(
                attrs={"class": "form__input", "placeholder": "e.g. Amoxicillin"}
            ),
            "dosage": forms.TextInput(
                attrs={"class": "form__input", "placeholder": "e.g. 500mg"}
            ),
            "frequency": forms.TextInput(
                attrs={"class": "form__input", "placeholder": "e.g. 3 times a day"}
            ),
            "duration": forms.TextInput(
                attrs={"class": "form__input", "placeholder": "e.g. 7 days"}
            ),
            "instructions": forms.Textarea(
                attrs={"rows": 2, "class": "form__input", "placeholder": "e.g. Take after meals"}
            ),
        }
        labels = {
            "medicine_name": "Medicine",
            "dosage": "Dosage",
            "frequency": "Frequency",
            "duration": "Duration",
            "instructions": "Instructions",
        }
