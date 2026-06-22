from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):

    class Meta:

        model = Review

        fields = (
            "rating",
            "comment",
        )

        widgets = {
            "rating": forms.Select(
                attrs={"class": "form__input form__select"}
            ),
            "comment": forms.Textarea(
                attrs={"rows": 4, "class": "form__input", "placeholder": "Share your experience with this doctor..."}
            ),
        }

        labels = {
            "rating": "Rating",
            "comment": "Your Review",
        }

        help_texts = {
            "comment": "Tell others about your experience with this doctor.",
        }