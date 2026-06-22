from django.test import TestCase
from django.contrib.auth import get_user_model

from doctors.models import Doctor, Specialization
from appointments.models import Appointment
from .models import Review
from .forms import ReviewForm

CustomUser = get_user_model()


class ReviewModelTest(TestCase):

    def setUp(self):
        self.patient = CustomUser.objects.create_user(
            username="patient1",
            email="patient1@example.com",
            password="testpass123",
            user_type="PATIENT",
        )
        self.doctor_user = CustomUser.objects.create_user(
            username="drreview",
            email="review@example.com",
            password="testpass123",
            user_type="DOCTOR",
        )
        self.doctor = Doctor.objects.create(
            user=self.doctor_user,
            license_number="MED-REVIEW",
            consultation_fee=100.00,
        )
        self.appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date="2026-07-01",
            appointment_time="10:00",
        )
        self.review = Review.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment=self.appointment,
            rating=5,
            comment="Excellent doctor!",
        )

    def test_review_creation(self):
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.comment, "Excellent doctor!")

    def test_review_str(self):
        expected = "patient1 - drreview"
        self.assertEqual(str(self.review), expected)

    def test_one_review_per_appointment(self):
        with self.assertRaises(Exception):
            Review.objects.create(
                patient=self.patient,
                doctor=self.doctor,
                appointment=self.appointment,
                rating=4,
                comment="Duplicate review",
            )

    def test_rating_choices(self):
        valid_ratings = [1, 2, 3, 4, 5]
        for rating in valid_ratings:
            review = Review(
                patient=self.patient,
                doctor=self.doctor,
                appointment=Appointment.objects.create(
                    patient=self.patient,
                    doctor=self.doctor,
                    appointment_date=f"2026-07-0{rating}",
                    appointment_time="11:00",
                ),
                rating=rating,
                comment=f"Rating {rating}",
            )
            review.full_clean()

    def test_default_ordering(self):
        review2 = Review.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment=Appointment.objects.create(
                patient=self.patient,
                doctor=self.doctor,
                appointment_date="2026-07-10",
                appointment_time="10:00",
            ),
            rating=3,
            comment="Okay",
        )
        reviews = Review.objects.all()
        self.assertEqual(reviews[0], review2)
        self.assertEqual(reviews[1], self.review)

    def test_cascade_delete_patient(self):
        self.patient.delete()
        self.assertEqual(Review.objects.count(), 0)

    def test_cascade_delete_doctor(self):
        self.doctor.delete()
        self.assertEqual(Review.objects.count(), 0)

    def test_cascade_delete_appointment(self):
        self.appointment.delete()
        self.assertEqual(Review.objects.count(), 0)

    def test_related_names(self):
        self.assertIn(self.review, self.patient.reviews.all())
        self.assertIn(self.review, self.doctor.reviews.all())
        self.assertEqual(self.appointment.review, self.review)


class ReviewFormTest(TestCase):

    def test_valid_form(self):
        form = ReviewForm(data={
            "rating": 5,
            "comment": "Great doctor!",
        })
        self.assertTrue(form.is_valid())

    def test_empty_comment_valid(self):
        form = ReviewForm(data={
            "rating": 4,
            "comment": "",
        })
        self.assertTrue(form.is_valid())

    def test_missing_rating_invalid(self):
        form = ReviewForm(data={
            "comment": "No rating given",
        })
        self.assertFalse(form.is_valid())

    def test_invalid_rating_value(self):
        form = ReviewForm(data={
            "rating": 6,
            "comment": "Invalid",
        })
        self.assertFalse(form.is_valid())

    def test_form_fields(self):
        form = ReviewForm()
        self.assertIn("rating", form.fields)
        self.assertIn("comment", form.fields)
        self.assertNotIn("patient", form.fields)
        self.assertNotIn("doctor", form.fields)
        self.assertNotIn("appointment", form.fields)

    def test_form_widgets(self):
        form = ReviewForm()
        self.assertEqual(
            form.fields["comment"].widget.attrs.get("class"),
            "form__input",
        )
        self.assertEqual(
            form.fields["rating"].widget.attrs.get("class"),
            "form__input form__select",
        )
