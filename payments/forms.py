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


