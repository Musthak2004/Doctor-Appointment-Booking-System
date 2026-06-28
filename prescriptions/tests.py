from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from doctors.models import Doctor
from appointments.models import Appointment
from .models import Prescription, PrescriptionItem
from .forms import PrescriptionForm, PrescriptionItemForm

CustomUser = get_user_model()


class PrescriptionModelTest(TestCase):
    def setUp(self):
        patient = CustomUser.objects.create_user(
            username="rxpat", email="rxpat@test.com", password="testpass123",
        )
        doctor_user = CustomUser.objects.create_user(
            username="rxdr", email="rxdr@test.com", password="testpass123",
            user_type="DOCTOR",
        )
        doctor = Doctor.objects.create(
            user=doctor_user, license_number="MED-RX", consultation_fee=100,
        )
        self.appointment = Appointment.objects.create(
            patient=patient, doctor=doctor,
            appointment_date="2026-08-01", appointment_time="10:00",
        )
        self.prescription = Prescription.objects.create(
            appointment=self.appointment,
            diagnosis="Hypertension",
            notes="Take medication daily",
        )

    def test_prescription_creation(self):
        self.assertEqual(self.prescription.diagnosis, "Hypertension")
        self.assertEqual(self.prescription.notes, "Take medication daily")

    def test_prescription_str(self):
        self.assertIn("Rx #1", str(self.prescription))


class PrescriptionItemModelTest(TestCase):
    def setUp(self):
        patient = CustomUser.objects.create_user(
            username="ritem", email="ritem@test.com", password="testpass123",
        )
        doctor_user = CustomUser.objects.create_user(
            username="ritemdr", email="ritemdr@test.com", password="testpass123",
            user_type="DOCTOR",
        )
        doctor = Doctor.objects.create(
            user=doctor_user, license_number="MED-RX2", consultation_fee=100,
        )
        appointment = Appointment.objects.create(
            patient=patient, doctor=doctor,
            appointment_date="2026-08-10", appointment_time="10:00",
        )
        self.prescription = Prescription.objects.create(
            appointment=appointment, diagnosis="Cold",
        )
        self.item = PrescriptionItem.objects.create(
            prescription=self.prescription,
            medicine_name="Amoxicillin",
            dosage="500mg",
            frequency="3 times a day",
            duration="7 days",
            instructions="After meals",
        )

    def test_prescription_item_creation(self):
        self.assertEqual(self.item.medicine_name, "Amoxicillin")
        self.assertEqual(self.item.dosage, "500mg")
        self.assertEqual(self.item.frequency, "3 times a day")
        self.assertEqual(self.item.duration, "7 days")

    def test_prescription_item_str(self):
        self.assertEqual(str(self.item), "Amoxicillin - 500mg")

    def test_cascade_delete_prescription(self):
        pk = self.item.pk
        self.prescription.delete()
        self.assertFalse(PrescriptionItem.objects.filter(pk=pk).exists())

    def test_related_name(self):
        self.assertIn(self.item, self.prescription.items.all())


class PrescriptionFormTest(TestCase):
    def test_valid_form(self):
        form = PrescriptionForm(data={
            "diagnosis": "Diabetes",
            "notes": "Monitor blood sugar",
        })
        self.assertTrue(form.is_valid())

    def test_blank_notes_valid(self):
        form = PrescriptionForm(data={"diagnosis": "Asthma"})
        self.assertTrue(form.is_valid())

    def test_missing_diagnosis_invalid(self):
        form = PrescriptionForm(data={"notes": "Some notes"})
        self.assertFalse(form.is_valid())
        self.assertIn("diagnosis", form.errors)

    def test_form_fields(self):
        form = PrescriptionForm()
        self.assertIn("diagnosis", form.fields)
        self.assertIn("notes", form.fields)


class PrescriptionItemFormTest(TestCase):
    def test_valid_form(self):
        form = PrescriptionItemForm(data={
            "medicine_name": "Ibuprofen",
            "dosage": "200mg",
            "frequency": "Twice daily",
            "duration": "5 days",
            "instructions": "With food",
        })
        self.assertTrue(form.is_valid())

    def test_missing_required_fields_invalid(self):
        form = PrescriptionItemForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("medicine_name", form.errors)
        self.assertIn("dosage", form.errors)
        self.assertIn("frequency", form.errors)
        self.assertIn("duration", form.errors)

    def test_form_fields(self):
        form = PrescriptionItemForm()
        expected = {"medicine_name", "dosage", "frequency", "duration", "instructions"}
        self.assertEqual(set(form.fields), expected)


class PrescriptionCreateViewTest(TestCase):
    def setUp(self):
        self.patient = CustomUser.objects.create_user(
            username="rxcreate", email="rxcreate@test.com", password="testpass123",
        )
        self.doctor_user = CustomUser.objects.create_user(
            username="rxcreatedr", email="rxcreatedr@test.com",
            password="testpass123", user_type="DOCTOR",
        )
        self.doctor = Doctor.objects.create(
            user=self.doctor_user, license_number="MED-RXC", consultation_fee=100,
        )
        self.appointment = Appointment.objects.create(
            patient=self.patient, doctor=self.doctor,
            appointment_date="2026-09-01", appointment_time="10:00",
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse("prescriptions:prescription_create", args=[self.appointment.pk])
        )
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('prescriptions:prescription_create', args=[self.appointment.pk])}",
        )

    def test_create_prescription(self):
        self.client.login(email="rxcreatedr@test.com", password="testpass123")
        response = self.client.post(
            reverse("prescriptions:prescription_create", args=[self.appointment.pk]),
            {"diagnosis": "Migraine", "notes": "Rest recommended"},
        )
        self.assertTrue(Prescription.objects.filter(appointment=self.appointment).exists())
        rx = Prescription.objects.get(appointment=self.appointment)
        self.assertRedirects(
            response,
            reverse("prescriptions:prescription_detail", args=[rx.pk]),
        )

    def test_dispatch_redirects_if_prescription_exists(self):
        Prescription.objects.create(
            appointment=self.appointment, diagnosis="Existing",
        )
        self.client.login(email="rxcreatedr@test.com", password="testpass123")
        response = self.client.get(
            reverse("prescriptions:prescription_create", args=[self.appointment.pk])
        )
        existing = Prescription.objects.get(appointment=self.appointment)
        self.assertRedirects(
            response,
            reverse("prescriptions:prescription_detail", args=[existing.pk]),
        )

    def test_404_for_non_doctor(self):
        self.client.login(email="rxcreate@test.com", password="testpass123")
        response = self.client.get(
            reverse("prescriptions:prescription_create", args=[self.appointment.pk])
        )
        self.assertEqual(response.status_code, 404)


class PrescriptionDetailViewTest(TestCase):
    def setUp(self):
        self.patient = CustomUser.objects.create_user(
            username="rxdet", email="rxdet@test.com", password="testpass123",
        )
        self.doctor_user = CustomUser.objects.create_user(
            username="rxdetdr", email="rxdetdr@test.com",
            password="testpass123", user_type="DOCTOR",
        )
        doctor = Doctor.objects.create(
            user=self.doctor_user, license_number="MED-RXD", consultation_fee=100,
        )
        appointment = Appointment.objects.create(
            patient=self.patient, doctor=doctor,
            appointment_date="2026-10-01", appointment_time="10:00",
        )
        self.prescription = Prescription.objects.create(
            appointment=appointment, diagnosis="Asthma",
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse("prescriptions:prescription_detail", args=[self.prescription.pk])
        )
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('prescriptions:prescription_detail', args=[self.prescription.pk])}",
        )

    def test_shows_prescription_for_patient(self):
        self.client.login(email="rxdet@test.com", password="testpass123")
        response = self.client.get(
            reverse("prescriptions:prescription_detail", args=[self.prescription.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Asthma")
        self.assertTemplateUsed(response, "prescriptions/prescription_detail.html")

    def test_shows_prescription_for_doctor(self):
        self.client.login(email="rxdetdr@test.com", password="testpass123")
        response = self.client.get(
            reverse("prescriptions:prescription_detail", args=[self.prescription.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Asthma")

    def test_404_for_unauthorized_user(self):
        other = CustomUser.objects.create_user(
            username="rxother", email="rxother@test.com", password="testpass123",
        )
        self.client.login(email="rxother@test.com", password="testpass123")
        response = self.client.get(
            reverse("prescriptions:prescription_detail", args=[self.prescription.pk])
        )
        self.assertEqual(response.status_code, 404)


class PrescriptionListViewTest(TestCase):
    def setUp(self):
        self.patient = CustomUser.objects.create_user(
            username="rxlist", email="rxlist@test.com", password="testpass123",
        )
        doctor_user = CustomUser.objects.create_user(
            username="rxlistdr", email="rxlistdr@test.com",
            password="testpass123", user_type="DOCTOR",
        )
        doctor = Doctor.objects.create(
            user=doctor_user, license_number="MED-RXL", consultation_fee=100,
        )
        appointment = Appointment.objects.create(
            patient=self.patient, doctor=doctor,
            appointment_date="2026-11-01", appointment_time="10:00",
        )
        self.prescription = Prescription.objects.create(
            appointment=appointment, diagnosis="Allergy",
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("prescriptions:prescription_list"))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('prescriptions:prescription_list')}",
        )

    def test_list_shows_patient_prescriptions(self):
        self.client.login(email="rxlist@test.com", password="testpass123")
        response = self.client.get(reverse("prescriptions:prescription_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Allergy")
        self.assertTemplateUsed(response, "prescriptions/prescription_list.html")

    def test_list_only_shows_own(self):
        other = CustomUser.objects.create_user(
            username="rxlist2", email="rxlist2@test.com", password="testpass123",
        )
        other_doc_user = CustomUser.objects.create_user(
            username="rxlistdr2", email="rxlistdr2@test.com",
            password="testpass123", user_type="DOCTOR",
        )
        other_doc = Doctor.objects.create(
            user=other_doc_user, license_number="MED-RXL2", consultation_fee=100,
        )
        other_appt = Appointment.objects.create(
            patient=other, doctor=other_doc,
            appointment_date="2026-11-02", appointment_time="11:00",
        )
        Prescription.objects.create(appointment=other_appt, diagnosis="Other")
        self.client.login(email="rxlist@test.com", password="testpass123")
        response = self.client.get(reverse("prescriptions:prescription_list"))
        self.assertEqual(len(response.context["prescriptions"]), 1)


class DoctorPrescriptionListViewTest(TestCase):
    def setUp(self):
        self.patient = CustomUser.objects.create_user(
            username="rxdoclist", email="rxdoclist@test.com", password="testpass123",
        )
        self.doctor_user = CustomUser.objects.create_user(
            username="rxdoclistdr", email="rxdoclistdr@test.com",
            password="testpass123", user_type="DOCTOR",
        )
        self.doctor = Doctor.objects.create(
            user=self.doctor_user, license_number="MED-RXDL", consultation_fee=100,
        )
        appointment = Appointment.objects.create(
            patient=self.patient, doctor=self.doctor,
            appointment_date="2026-12-01", appointment_time="10:00",
        )
        self.prescription = Prescription.objects.create(
            appointment=appointment, diagnosis="Flu",
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("prescriptions:doctor_prescription_list"))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('prescriptions:doctor_prescription_list')}",
        )

    def test_list_shows_doctor_prescriptions(self):
        self.client.login(email="rxdoclistdr@test.com", password="testpass123")
        response = self.client.get(reverse("prescriptions:doctor_prescription_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Flu")

    def test_is_doctor_view_context(self):
        self.client.login(email="rxdoclistdr@test.com", password="testpass123")
        response = self.client.get(reverse("prescriptions:doctor_prescription_list"))
        self.assertTrue(response.context["is_doctor_view"])
