from django import forms

from .models import Payment


class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = (
            "payment_method",
        )
        widgets = {
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
