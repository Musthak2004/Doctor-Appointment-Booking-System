from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from doctors.models import Doctor
from appointments.models import Appointment
from .models import Payment
from .forms import PaymentForm

CustomUser = get_user_model()


class PaymentModelTest(TestCase):
    def setUp(self):
        patient = CustomUser.objects.create_user(
            username="paypat", email="paypat@test.com", password="testpass123",
        )
        doctor_user = CustomUser.objects.create_user(
            username="paydr", email="paydr@test.com", password="testpass123",
            user_type="DOCTOR",
        )
        doctor = Doctor.objects.create(
            user=doctor_user, license_number="MED-PAY", consultation_fee=200,
        )
        self.appointment = Appointment.objects.create(
            patient=patient, doctor=doctor,
            appointment_date="2026-08-15", appointment_time="10:00",
        )
        self.payment = Payment.objects.create(
            appointment=self.appointment,
            amount=200.00,
            payment_method=Payment.Method.CARD,
            transaction_id="TXN-001",
        )

    def test_payment_creation(self):
        self.assertEqual(self.payment.amount, 200.00)
        self.assertEqual(self.payment.payment_method, "CARD")
        self.assertEqual(self.payment.transaction_id, "TXN-001")

    def test_payment_str(self):
        self.assertIn(str(self.payment.id), str(self.payment))
        self.assertIn("200.0", str(self.payment))

    def test_default_status(self):
        self.assertEqual(self.payment.status, Payment.Status.PENDING)

    def test_transaction_id_unique(self):
        with self.assertRaises(Exception):
            Payment.objects.create(
                appointment=self.appointment,
                amount=200.00,
                payment_method=Payment.Method.CASH,
                transaction_id="TXN-001",
            )


class PaymentFormTest(TestCase):
    def test_valid_form(self):
        form = PaymentForm(data={"payment_method": "CARD"})
        self.assertTrue(form.is_valid())

    def test_missing_payment_method_invalid(self):
        form = PaymentForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("payment_method", form.errors)

    def test_form_fields(self):
        form = PaymentForm()
        self.assertIn("payment_method", form.fields)


class PaymentCreateViewTest(TestCase):
    def setUp(self):
        self.patient = CustomUser.objects.create_user(
            username="paycreate", email="paycreate@test.com", password="testpass123",
        )
        doctor_user = CustomUser.objects.create_user(
            username="paycreatedr", email="paycreatedr@test.com",
            password="testpass123", user_type="DOCTOR",
        )
        self.doctor = Doctor.objects.create(
            user=doctor_user, license_number="MED-PAYC", consultation_fee=150,
        )
        self.appointment = Appointment.objects.create(
            patient=self.patient, doctor=self.doctor,
            appointment_date="2026-09-01", appointment_time="10:00",
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse("payments:payment_create", args=[self.appointment.pk])
        )
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('payments:payment_create', args=[self.appointment.pk])}",
        )

    def test_create_payment(self):
        self.client.login(email="paycreate@test.com", password="testpass123")
        response = self.client.post(
            reverse("payments:payment_create", args=[self.appointment.pk]),
            {"payment_method": "PAYPAL"},
        )
        self.assertRedirects(response, reverse("appointments:appointment_list"))
        self.assertTrue(
            Payment.objects.filter(appointment=self.appointment).exists()
        )
        payment = Payment.objects.get(appointment=self.appointment)
        self.assertEqual(payment.amount, 150.00)

    def test_dispatch_redirects_if_payment_exists(self):
        Payment.objects.create(
            appointment=self.appointment,
            amount=150.00,
            payment_method="CARD",
            transaction_id="TXN-EXIST",
        )
        self.client.login(email="paycreate@test.com", password="testpass123")
        response = self.client.get(
            reverse("payments:payment_create", args=[self.appointment.pk])
        )
        existing = Payment.objects.get(appointment=self.appointment)
        self.assertRedirects(
            response,
            reverse("payments:payment_detail", args=[existing.pk]),
        )

    def test_404_for_other_patient(self):
        other = CustomUser.objects.create_user(
            username="otherpay", email="otherpay@test.com", password="testpass123",
        )
        self.client.login(email="otherpay@test.com", password="testpass123")
        response = self.client.get(
            reverse("payments:payment_create", args=[self.appointment.pk])
        )
        self.assertEqual(response.status_code, 404)


class PaymentDetailViewTest(TestCase):
    def setUp(self):
        self.patient = CustomUser.objects.create_user(
            username="paydet", email="paydet@test.com", password="testpass123",
        )
        doctor_user = CustomUser.objects.create_user(
            username="paydetdr", email="paydetdr@test.com",
            password="testpass123", user_type="DOCTOR",
        )
        doctor = Doctor.objects.create(
            user=doctor_user, license_number="MED-PAYD", consultation_fee=100,
        )
        appointment = Appointment.objects.create(
            patient=self.patient, doctor=doctor,
            appointment_date="2026-10-01", appointment_time="10:00",
        )
        self.payment = Payment.objects.create(
            appointment=appointment,
            amount=100.00,
            payment_method="CASH",
            transaction_id="TXN-DET",
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse("payments:payment_detail", args=[self.payment.pk])
        )
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('payments:payment_detail', args=[self.payment.pk])}",
        )

    def test_shows_payment_detail(self):
        self.client.login(email="paydet@test.com", password="testpass123")
        response = self.client.get(
            reverse("payments:payment_detail", args=[self.payment.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "TXN-DET")
        self.assertTemplateUsed(response, "payments/payment_detail.html")

    def test_404_for_other_patient(self):
        other = CustomUser.objects.create_user(
            username="otherdet", email="otherdet@test.com", password="testpass123",
        )
        self.client.login(email="otherdet@test.com", password="testpass123")
        response = self.client.get(
            reverse("payments:payment_detail", args=[self.payment.pk])
        )
        self.assertEqual(response.status_code, 404)


class PaymentListViewTest(TestCase):
    def setUp(self):
        self.patient = CustomUser.objects.create_user(
            username="paylist", email="paylist@test.com", password="testpass123",
        )
        doctor_user = CustomUser.objects.create_user(
            username="paylistdr", email="paylistdr@test.com",
            password="testpass123", user_type="DOCTOR",
        )
        doctor = Doctor.objects.create(
            user=doctor_user, license_number="MED-PAYL", consultation_fee=100,
        )
        appointment = Appointment.objects.create(
            patient=self.patient, doctor=doctor,
            appointment_date="2026-11-01", appointment_time="10:00",
        )
        self.payment = Payment.objects.create(
            appointment=appointment,
            amount=100.00,
            payment_method="BANK",
            transaction_id="TXN-LIST",
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("payments:payment_list"))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('payments:payment_list')}",
        )

    def test_list_shows_patient_payments(self):
        self.client.login(email="paylist@test.com", password="testpass123")
        response = self.client.get(reverse("payments:payment_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "paylistdr@test.com")
        self.assertTemplateUsed(response, "payments/payment_list.html")

    def test_list_only_shows_own_payments(self):
        other = CustomUser.objects.create_user(
            username="paylist2", email="paylist2@test.com", password="testpass123",
        )
        other_doctor = CustomUser.objects.create_user(
            username="paylistdr2", email="paylistdr2@test.com",
            password="testpass123", user_type="DOCTOR",
        )
        other_doc = Doctor.objects.create(
            user=other_doctor, license_number="MED-PAYL2", consultation_fee=100,
        )
        other_appt = Appointment.objects.create(
            patient=other, doctor=other_doc,
            appointment_date="2026-11-02", appointment_time="11:00",
        )
        Payment.objects.create(
            appointment=other_appt, amount=100.00,
            payment_method="CARD", transaction_id="TXN-OTHER",
        )
        self.client.login(email="paylist@test.com", password="testpass123")
        response = self.client.get(reverse("payments:payment_list"))
        self.assertEqual(len(response.context["payments"]), 1)


class DoctorPaymentListViewTest(TestCase):
    def setUp(self):
        self.patient = CustomUser.objects.create_user(
            username="dp", email="dp@test.com", password="testpass123",
        )
        self.doctor_user = CustomUser.objects.create_user(
            username="dpdr", email="dpdr@test.com", password="testpass123",
            user_type="DOCTOR",
        )
        self.doctor = Doctor.objects.create(
            user=self.doctor_user, license_number="MED-DP", consultation_fee=100,
        )
        appointment = Appointment.objects.create(
            patient=self.patient, doctor=self.doctor,
            appointment_date="2026-12-01", appointment_time="10:00",
        )
        self.payment = Payment.objects.create(
            appointment=appointment, amount=100.00,
            payment_method="CARD", transaction_id="TXN-DP",
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("payments:doctor_payment_list"))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('payments:doctor_payment_list')}",
        )

    def test_list_shows_doctor_payments(self):
        self.client.login(email="dpdr@test.com", password="testpass123")
        response = self.client.get(reverse("payments:doctor_payment_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "dpdr@test.com")

    def test_is_doctor_view_context(self):
        self.client.login(email="dpdr@test.com", password="testpass123")
        response = self.client.get(reverse("payments:doctor_payment_list"))
        self.assertTrue(response.context["is_doctor_view"])
