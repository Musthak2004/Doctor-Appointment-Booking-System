from django import forms

from .models import Payment


class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = (
            "appointment",
            "amount",
            "payment_method",
        )
        widgets = {
            "appointment": forms.Select(
                attrs={"class": "form__input form__select"}
            ),
            "amount": forms.NumberInput(
                attrs={"step": "0.01", "min": "0", "class": "form__input"}
            ),
            "payment_method": forms.Select(
                attrs={"class": "form__input form__select"}
            ),
        }
        labels = {
            "payment_method": "Payment Method",
        }

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")
        return amount
