from django.test import TestCase
from django.urls import reverse
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


class ReviewListViewTest(TestCase):
    def setUp(self):
        self.patient = CustomUser.objects.create_user(
            username="revlist", email="revlist@test.com", password="testpass123",
        )
        doctor_user = CustomUser.objects.create_user(
            username="revlistdr", email="revlistdr@test.com",
            password="testpass123", user_type="DOCTOR",
        )
        self.doctor = Doctor.objects.create(
            user=doctor_user, license_number="MED-REVLIST", consultation_fee=100,
        )
        self.appointment = Appointment.objects.create(
            patient=self.patient, doctor=self.doctor,
            appointment_date="2026-08-01", appointment_time="10:00",
        )
        self.review = Review.objects.create(
            patient=self.patient, doctor=self.doctor,
            appointment=self.appointment, rating=4, comment="Good",
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("reviews:review_list"))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('reviews:review_list')}",
        )

    def test_list_shows_patient_reviews(self):
        self.client.login(email="revlist@test.com", password="testpass123")
        response = self.client.get(reverse("reviews:review_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Good")
        self.assertTemplateUsed(response, "reviews/review_list.html")

    def test_list_only_shows_own_reviews(self):
        other = CustomUser.objects.create_user(
            username="revlist2", email="revlist2@test.com", password="testpass123",
        )
        other_appt = Appointment.objects.create(
            patient=other, doctor=self.doctor,
            appointment_date="2026-08-10", appointment_time="10:00",
        )
        Review.objects.create(
            patient=other, doctor=self.doctor,
            appointment=other_appt, rating=3, comment="Other",
        )
        self.client.login(email="revlist@test.com", password="testpass123")
        response = self.client.get(reverse("reviews:review_list"))
        self.assertEqual(len(response.context["reviews"]), 1)


class ReviewDetailViewTest(TestCase):
    def setUp(self):
        self.patient = CustomUser.objects.create_user(
            username="revdet", email="revdet@test.com", password="testpass123",
        )
        doctor_user = CustomUser.objects.create_user(
            username="revdetdr", email="revdetdr@test.com",
            password="testpass123", user_type="DOCTOR",
        )
        doctor = Doctor.objects.create(
            user=doctor_user, license_number="MED-REVDET", consultation_fee=100,
        )
        appointment = Appointment.objects.create(
            patient=self.patient, doctor=doctor,
            appointment_date="2026-09-01", appointment_time="10:00",
        )
        self.review = Review.objects.create(
            patient=self.patient, doctor=doctor,
            appointment=appointment, rating=5, comment="Excellent",
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse("reviews:review_detail", args=[self.review.pk])
        )
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('reviews:review_detail', args=[self.review.pk])}",
        )

    def test_shows_review_detail(self):
        self.client.login(email="revdet@test.com", password="testpass123")
        response = self.client.get(
            reverse("reviews:review_detail", args=[self.review.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Excellent")
        self.assertTemplateUsed(response, "reviews/review_detail.html")

    def test_404_for_other_patient(self):
        other = CustomUser.objects.create_user(
            username="revdet2", email="revdet2@test.com", password="testpass123",
        )
        self.client.login(email="revdet2@test.com", password="testpass123")
        response = self.client.get(
            reverse("reviews:review_detail", args=[self.review.pk])
        )
        self.assertEqual(response.status_code, 404)


class ReviewCreateViewTest(TestCase):
    def setUp(self):
        self.patient = CustomUser.objects.create_user(
            username="revcreate", email="revcreate@test.com",
            password="testpass123",
        )
        doctor_user = CustomUser.objects.create_user(
            username="revcreatedr", email="revcreatedr@test.com",
            password="testpass123", user_type="DOCTOR",
        )
        self.doctor = Doctor.objects.create(
            user=doctor_user, license_number="MED-REVCREATE",
            consultation_fee=100,
        )
        self.appointment = Appointment.objects.create(
            patient=self.patient, doctor=self.doctor,
            appointment_date="2026-10-01", appointment_time="10:00",
        )
        self.url = reverse(
            "reviews:review_create",
            kwargs={"appointment_id": self.appointment.pk},
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={self.url}",
        )

    def test_logged_in_patient_can_access(self):
        self.client.login(email="revcreate@test.com", password="testpass123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reviews/review_form.html")

    def test_creates_review_successfully(self):
        self.client.login(email="revcreate@test.com", password="testpass123")
        response = self.client.post(self.url, data={
            "rating": 4,
            "comment": "Great doctor!",
        })
        self.assertEqual(Review.objects.count(), 1)
        review = Review.objects.first()
        self.assertEqual(review.patient, self.patient)
        self.assertEqual(review.doctor, self.doctor)
        self.assertEqual(review.appointment, self.appointment)
        self.assertRedirects(
            response,
            reverse("reviews:review_detail", args=[review.pk]),
        )

    def test_duplicate_review_redirects(self):
        Review.objects.create(
            patient=self.patient, doctor=self.doctor,
            appointment=self.appointment, rating=5, comment="First",
        )
        self.client.login(email="revcreate@test.com", password="testpass123")
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            reverse(
                "reviews:review_detail",
                kwargs={"pk": self.appointment.review.pk},
            ),
        )

    def test_nonexistent_appointment_returns_404(self):
        self.client.login(email="revcreate@test.com", password="testpass123")
        bad_url = reverse(
            "reviews:review_create",
            kwargs={"appointment_id": 99999},
        )
        response = self.client.get(bad_url)
        self.assertEqual(response.status_code, 404)

    def test_wrong_patient_cannot_review(self):
        other = CustomUser.objects.create_user(
            username="revcreate2", email="revcreate2@test.com",
            password="testpass123",
        )
        self.client.login(email="revcreate2@test.com", password="testpass123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)
