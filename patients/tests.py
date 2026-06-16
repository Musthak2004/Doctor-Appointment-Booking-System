from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Patient
from .forms import PatientForm

CustomUser = get_user_model()


class PatientModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testpatient",
            email="patient@example.com",
            password="testpass123",
        )
        self.patient = Patient.objects.create(
            user=self.user,
            date_of_birth="1990-05-15",
            gender="male",
            blood_group="A+",
            address="123 Main St",
            emergency_contact="+1 555-000-0000",
            medical_history="None",
        )

    def test_patient_creation(self):
        self.assertEqual(self.patient.user, self.user)
        self.assertEqual(self.patient.blood_group, "A+")
        self.assertEqual(self.patient.gender, "male")

    def test_patient_str(self):
        self.assertEqual(str(self.patient), "testpatient")

    def test_patient_defaults(self):
        user2 = CustomUser.objects.create_user(
            username="patient2",
            email="patient2@example.com",
            password="testpass123",
        )
        patient2 = Patient.objects.create(user=user2)
        self.assertIsNone(patient2.date_of_birth)
        self.assertEqual(patient2.gender, "")
        self.assertEqual(patient2.blood_group, "")
        self.assertEqual(patient2.address, "")
        self.assertEqual(patient2.emergency_contact, "")
        self.assertEqual(patient2.medical_history, "")

    def test_one_to_one_relation(self):
        self.assertEqual(self.user.patient_profile, self.patient)


class PatientFormTest(TestCase):
    def test_valid_form(self):
        form = PatientForm(data={
            "date_of_birth": "1990-05-15",
            "gender": "female",
            "blood_group": "B+",
            "address": "456 Oak Ave",
            "emergency_contact": "+1 555-111-2222",
            "medical_history": "Asthma",
        })
        self.assertTrue(form.is_valid())

    def test_blank_form_is_valid(self):
        form = PatientForm(data={})
        self.assertTrue(form.is_valid())

    def test_invalid_gender(self):
        form = PatientForm(data={"gender": "alien"})
        self.assertFalse(form.is_valid())


class PatientCreateViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="newpatient",
            email="new@example.com",
            password="testpass123",
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("patients:patient_create"))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('patients:patient_create')}",
        )

    def test_logged_in_can_access_create(self):
        self.client.login(email="new@example.com", password="testpass123")
        response = self.client.get(reverse("patients:patient_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "patients/patient_form.html")

    def test_create_patient(self):
        self.client.login(email="new@example.com", password="testpass123")
        response = self.client.post(reverse("patients:patient_create"), {
            "date_of_birth": "1985-03-20",
            "gender": "male",
            "blood_group": "O+",
            "address": "789 Pine St",
            "emergency_contact": "+1 555-333-4444",
            "medical_history": "Diabetes",
        })
        self.assertRedirects(response, reverse("patients:patient_detail"))
        self.assertTrue(Patient.objects.filter(user=self.user).exists())

    def test_redirect_to_detail_if_already_has_profile(self):
        Patient.objects.create(user=self.user)
        self.client.login(email="new@example.com", password="testpass123")
        response = self.client.get(reverse("patients:patient_create"))
        self.assertRedirects(response, reverse("patients:patient_detail"))


class PatientDetailViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="detailpatient",
            email="detail@example.com",
            password="testpass123",
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("patients:patient_detail"))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('patients:patient_detail')}",
        )

    def test_redirect_to_create_if_no_profile(self):
        self.client.login(email="detail@example.com", password="testpass123")
        response = self.client.get(reverse("patients:patient_detail"))
        self.assertRedirects(response, reverse("patients:patient_create"))

    def test_detail_shows_profile(self):
        Patient.objects.create(
            user=self.user,
            blood_group="AB+",
            gender="female",
        )
        self.client.login(email="detail@example.com", password="testpass123")
        response = self.client.get(reverse("patients:patient_detail"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "AB+")
        self.assertContains(response, "Female")
        self.assertTemplateUsed(response, "patients/patient_detail.html")


class PatientUpdateViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="updatepatient",
            email="update@example.com",
            password="testpass123",
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("patients:patient_update"))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('patients:patient_update')}",
        )

    def test_redirect_to_create_if_no_profile(self):
        self.client.login(email="update@example.com", password="testpass123")
        response = self.client.get(reverse("patients:patient_update"))
        self.assertRedirects(response, reverse("patients:patient_create"))

    def test_update_profile(self):
        patient = Patient.objects.create(
            user=self.user,
            blood_group="A+",
        )
        self.client.login(email="update@example.com", password="testpass123")
        response = self.client.post(reverse("patients:patient_update"), {
            "blood_group": "B+",
            "gender": "male",
        })
        self.assertRedirects(response, reverse("patients:patient_detail"))
        patient.refresh_from_db()
        self.assertEqual(patient.blood_group, "B+")
