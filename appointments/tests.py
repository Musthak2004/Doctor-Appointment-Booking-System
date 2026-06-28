import datetime

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from doctors.models import Doctor, Specialization, DoctorAvailability
from .models import Appointment
from .forms import AppointmentForm

CustomUser = get_user_model()


class AppointmentModelTest(TestCase):
    def setUp(self):
        self.patient = CustomUser.objects.create_user(
            username="patient1", email="patient@test.com", password="testpass123",
        )
        self.doctor_user = CustomUser.objects.create_user(
            username="dr1", email="dr@test.com", password="testpass123",
            user_type="DOCTOR",
        )
        self.doctor = Doctor.objects.create(
            user=self.doctor_user, license_number="MED-001", consultation_fee=100,
        )
        self.appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date="2026-08-01",
            appointment_time="10:00",
            reason="Checkup",
        )

    def test_appointment_creation(self):
        self.assertEqual(self.appointment.patient, self.patient)
        self.assertEqual(self.appointment.doctor, self.doctor)
        self.assertEqual(self.appointment.reason, "Checkup")

    def test_appointment_str(self):
        expected = f"{self.patient.email} -> {self.doctor_user.email} (2026-08-01 10:00)"
        self.assertEqual(str(self.appointment), expected)

    def test_default_status(self):
        self.assertEqual(self.appointment.status, Appointment.Status.PENDING)

    def test_unique_constraint_prevents_duplicate_slot(self):
        with self.assertRaises(Exception):
            Appointment.objects.create(
                patient=self.patient,
                doctor=self.doctor,
                appointment_date="2026-08-01",
                appointment_time="10:00",
            )


class AppointmentFormTest(TestCase):
    def setUp(self):
        self.patient = CustomUser.objects.create_user(
            username="formpatient", email="fp@test.com", password="testpass123",
        )
        self.doctor_user = CustomUser.objects.create_user(
            username="formdr", email="formdr@test.com", password="testpass123",
            user_type="DOCTOR",
        )
        self.doctor = Doctor.objects.create(
            user=self.doctor_user, license_number="MED-FORM", consultation_fee=100,
            is_verified=True,
        )
        DoctorAvailability.objects.create(
            doctor=self.doctor, day="mon", start_time="09:00", end_time="17:00",
        )
        self.future_monday = self._next_weekday(0)

    def _next_weekday(self, target_weekday):
        today = datetime.date.today()
        days_ahead = target_weekday - today.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return today + datetime.timedelta(days=days_ahead)

    def test_valid_form(self):
        date = self.future_monday
        form = AppointmentForm(
            data={
                "doctor": self.doctor.pk,
                "appointment_date": date.isoformat(),
                "appointment_time": "10:00",
                "reason": "Routine",
            },
        )
        self.assertTrue(form.is_valid())

    def test_past_date_invalid(self):
        past = timezone.localdate() - datetime.timedelta(days=1)
        form = AppointmentForm(
            data={
                "doctor": self.doctor.pk,
                "appointment_date": past.isoformat(),
                "appointment_time": "10:00",
            },
        )
        self.assertFalse(form.is_valid())
        self.assertIn("Appointment date cannot be in the past", str(form.errors))

    def test_doctor_not_available_invalid(self):
        wednesday = self._next_weekday(2)
        form = AppointmentForm(
            data={
                "doctor": self.doctor.pk,
                "appointment_date": wednesday.isoformat(),
                "appointment_time": "10:00",
            },
        )
        self.assertFalse(form.is_valid())
        self.assertIn("not available", str(form.errors))

    def test_missing_fields_invalid(self):
        form = AppointmentForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("doctor", form.errors)
        self.assertIn("appointment_date", form.errors)
        self.assertIn("appointment_time", form.errors)

    def test_form_fields(self):
        form = AppointmentForm()
        expected = {"doctor", "appointment_date", "appointment_time", "reason"}
        self.assertEqual(set(form.fields), expected)


class AppointmentCreateViewTest(TestCase):
    def setUp(self):
        self.patient = CustomUser.objects.create_user(
            username="createpatient", email="cp@test.com", password="testpass123",
        )
        self.doctor_user = CustomUser.objects.create_user(
            username="createdr", email="createdr@test.com", password="testpass123",
            user_type="DOCTOR",
        )
        self.doctor = Doctor.objects.create(
            user=self.doctor_user, license_number="MED-CREATE", consultation_fee=100,
            is_verified=True,
        )
        DoctorAvailability.objects.create(
            doctor=self.doctor, day="mon", start_time="09:00", end_time="17:00",
        )
        self.future_monday = self._next_weekday(0)

    def _next_weekday(self, target_weekday):
        today = datetime.date.today()
        days_ahead = target_weekday - today.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return today + datetime.timedelta(days=days_ahead)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("appointments:appointment_create"))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('appointments:appointment_create')}",
        )

    def test_logged_in_can_access_create(self):
        self.client.login(email="cp@test.com", password="testpass123")
        response = self.client.get(reverse("appointments:appointment_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "appointments/appointment_form.html")

    def test_get_initial_with_doctor_param(self):
        self.client.login(email="cp@test.com", password="testpass123")
        response = self.client.get(
            reverse("appointments:appointment_create") + f"?doctor={self.doctor.pk}"
        )
        self.assertEqual(response.status_code, 200)
        initial_doctor = response.context["form"].initial.get("doctor")
        self.assertEqual(initial_doctor, str(self.doctor.pk))

    def test_create_appointment(self):
        self.client.login(email="cp@test.com", password="testpass123")
        date = self.future_monday
        response = self.client.post(reverse("appointments:appointment_create"), {
            "doctor": self.doctor.pk,
            "appointment_date": date.isoformat(),
            "appointment_time": "10:00",
            "reason": "Test appointment",
        })
        self.assertRedirects(response, reverse("appointments:appointment_list"))
        self.assertTrue(
            Appointment.objects.filter(patient=self.patient, reason="Test appointment").exists()
        )

    def test_form_invalid_renders_form(self):
        self.client.login(email="cp@test.com", password="testpass123")
        response = self.client.post(reverse("appointments:appointment_create"), {
            "doctor": "",
            "appointment_date": "",
            "appointment_time": "",
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "appointments/appointment_form.html")


class AppointmentListViewTest(TestCase):
    def setUp(self):
        self.patient = CustomUser.objects.create_user(
            username="listpatient", email="lp@test.com", password="testpass123",
        )
        self.other_patient = CustomUser.objects.create_user(
            username="other", email="other@test.com", password="testpass123",
        )
        self.doctor_user = CustomUser.objects.create_user(
            username="listdr", email="listdr@test.com", password="testpass123",
            user_type="DOCTOR",
        )
        self.doctor = Doctor.objects.create(
            user=self.doctor_user, license_number="MED-LIST", consultation_fee=100,
        )
        self.appt = Appointment.objects.create(
            patient=self.patient, doctor=self.doctor,
            appointment_date="2026-09-01", appointment_time="09:00",
        )
        Appointment.objects.create(
            patient=self.other_patient, doctor=self.doctor,
            appointment_date="2026-09-01", appointment_time="10:00",
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("appointments:appointment_list"))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('appointments:appointment_list')}",
        )

    def test_list_shows_patient_appointments(self):
        self.client.login(email="lp@test.com", password="testpass123")
        response = self.client.get(reverse("appointments:appointment_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.appt.reason)

    def test_doctor_appointments_not_shown_in_patient_list(self):
        self.client.login(email="lp@test.com", password="testpass123")
        response = self.client.get(reverse("appointments:appointment_list"))
        self.assertEqual(len(response.context["appointments"]), 1)

    def test_empty_list(self):
        Appointment.objects.filter(patient=self.patient).delete()
        self.client.login(email="lp@test.com", password="testpass123")
        response = self.client.get(reverse("appointments:appointment_list"))
        self.assertEqual(response.status_code, 200)


class DoctorAppointmentListViewTest(TestCase):
    def setUp(self):
        self.patient = CustomUser.objects.create_user(
            username="dap", email="dap@test.com", password="testpass123",
        )
        self.doctor_user = CustomUser.objects.create_user(
            username="dadr", email="dadr@test.com", password="testpass123",
            user_type="DOCTOR",
        )
        self.doctor = Doctor.objects.create(
            user=self.doctor_user, license_number="MED-DA", consultation_fee=100,
        )
        self.appt = Appointment.objects.create(
            patient=self.patient, doctor=self.doctor,
            appointment_date="2026-10-01", appointment_time="09:00",
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("appointments:doctor_appointment_list"))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('appointments:doctor_appointment_list')}",
        )

    def test_list_shows_doctor_appointments(self):
        self.client.login(email="dadr@test.com", password="testpass123")
        response = self.client.get(reverse("appointments:doctor_appointment_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.appt.reason)

    def test_is_doctor_view_context(self):
        self.client.login(email="dadr@test.com", password="testpass123")
        response = self.client.get(reverse("appointments:doctor_appointment_list"))
        self.assertTrue(response.context["is_doctor_view"])

    def test_patient_appointments_not_shown(self):
        patient2 = CustomUser.objects.create_user(
            username="dapOther", email="dapother@test.com", password="testpass123",
        )
        doctor2_user = CustomUser.objects.create_user(
            username="dadrOther", email="dadrother@test.com", password="testpass123",
            user_type="DOCTOR",
        )
        doctor2 = Doctor.objects.create(
            user=doctor2_user, license_number="MED-DA2", consultation_fee=100,
        )
        Appointment.objects.create(
            patient=patient2, doctor=doctor2,
            appointment_date="2026-10-02", appointment_time="10:00",
        )
        self.client.login(email="dadr@test.com", password="testpass123")
        response = self.client.get(reverse("appointments:doctor_appointment_list"))
        self.assertEqual(len(response.context["appointments"]), 1)


class AppointmentDetailViewTest(TestCase):
    def setUp(self):
        self.patient = CustomUser.objects.create_user(
            username="detpatient", email="detp@test.com", password="testpass123",
        )
        self.doctor_user = CustomUser.objects.create_user(
            username="detdr", email="detdr@test.com", password="testpass123",
            user_type="DOCTOR",
        )
        self.doctor = Doctor.objects.create(
            user=self.doctor_user, license_number="MED-DET", consultation_fee=100,
        )
        self.appt = Appointment.objects.create(
            patient=self.patient, doctor=self.doctor,
            appointment_date="2026-11-01", appointment_time="09:00",
            reason="Detail view test",
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse("appointments:appointment_detail", args=[self.appt.pk])
        )
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('appointments:appointment_detail', args=[self.appt.pk])}",
        )

    def test_shows_appointment_detail_for_patient(self):
        self.client.login(email="detp@test.com", password="testpass123")
        response = self.client.get(
            reverse("appointments:appointment_detail", args=[self.appt.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Detail view test")
        self.assertTemplateUsed(response, "appointments/appointment_detail.html")

    def test_shows_appointment_detail_for_doctor(self):
        self.client.login(email="detdr@test.com", password="testpass123")
        response = self.client.get(
            reverse("appointments:appointment_detail", args=[self.appt.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Detail view test")

    def test_404_for_unauthorized_user(self):
        other = CustomUser.objects.create_user(
            username="otheruser", email="other@test.com", password="testpass123",
        )
        self.client.login(email="other@test.com", password="testpass123")
        response = self.client.get(
            reverse("appointments:appointment_detail", args=[self.appt.pk])
        )
        self.assertEqual(response.status_code, 404)
