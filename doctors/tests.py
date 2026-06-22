from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Doctor, Specialization, DoctorAvailability
from .forms import DoctorForm, AvailabilityForm

CustomUser = get_user_model()


class SpecializationModelTest(TestCase):
    def test_create_specialization(self):
        spec = Specialization.objects.create(name="Cardiology")
        self.assertEqual(str(spec), "Cardiology")

    def test_name_unique(self):
        Specialization.objects.create(name="Cardiology")
        with self.assertRaises(Exception):
            Specialization.objects.create(name="Cardiology")


class DoctorModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="drdoctor",
            email="doctor@example.com",
            password="testpass123",
        )
        self.spec = Specialization.objects.create(name="Cardiology")
        self.doctor = Doctor.objects.create(
            user=self.user,
            specialization=self.spec,
            license_number="MED-12345",
            experience_years=10,
            qualification="MD",
            hospital_name="City Hospital",
            consultation_fee=150.00,
            bio="Experienced cardiologist.",
        )

    def test_doctor_creation(self):
        self.assertEqual(self.doctor.user, self.user)
        self.assertEqual(self.doctor.specialization.name, "Cardiology")
        self.assertEqual(self.doctor.consultation_fee, 150.00)
        self.assertEqual(self.doctor.experience_years, 10)

    def test_doctor_str(self):
        self.assertEqual(str(self.doctor), "drdoctor")

    def test_default_is_verified(self):
        self.assertFalse(self.doctor.is_verified)

    def test_default_experience_years(self):
        doctor2 = Doctor.objects.create(
            user=CustomUser.objects.create_user(
                username="dr2", email="dr2@example.com", password="testpass123"
            ),
            license_number="MED-67890",
        )
        self.assertEqual(doctor2.experience_years, 0)
        self.assertEqual(doctor2.consultation_fee, 0.00)

    def test_one_to_one_relation(self):
        self.assertEqual(self.user.doctor_profile, self.doctor)

    def test_license_number_unique(self):
        with self.assertRaises(Exception):
            Doctor.objects.create(
                user=CustomUser.objects.create_user(
                    username="dr3", email="dr3@example.com", password="testpass123"
                ),
                license_number="MED-12345",
                consultation_fee=200.00,
            )


class DoctorAvailabilityModelTest(TestCase):
    def setUp(self):
        self.doctor = Doctor.objects.create(
            user=CustomUser.objects.create_user(
                username="dravail", email="avail@example.com", password="testpass123"
            ),
            license_number="MED-AVAIL",
            consultation_fee=100.00,
        )
        self.slot = DoctorAvailability.objects.create(
            doctor=self.doctor,
            day="mon",
            start_time="09:00",
            end_time="17:00",
        )

    def test_availability_creation(self):
        self.assertEqual(self.slot.doctor, self.doctor)
        self.assertEqual(self.slot.day, "mon")
        self.assertTrue(self.slot.is_available)

    def test_availability_str(self):
        self.assertEqual(str(self.slot), "dravail - mon")


class DoctorFormTest(TestCase):
    def setUp(self):
        self.spec = Specialization.objects.create(name="Dermatology")

    def test_valid_form(self):
        form = DoctorForm(data={
            "specialization": self.spec.pk,
            "license_number": "MED-FORM-001",
            "experience_years": 8,
            "qualification": "MBBS",
            "hospital_name": "Skin Clinic",
            "consultation_fee": 200.00,
            "bio": "Skin specialist.",
        })
        self.assertTrue(form.is_valid())

    def test_negative_fee_invalid(self):
        form = DoctorForm(data={
            "license_number": "MED-FORM-002",
            "consultation_fee": -50.00,
        })
        self.assertFalse(form.is_valid())

    def test_negative_experience_invalid(self):
        form = DoctorForm(data={
            "license_number": "MED-FORM-003",
            "experience_years": -1,
        })
        self.assertFalse(form.is_valid())

    def test_minimal_required_fields(self):
        form = DoctorForm(data={
            "license_number": "MED-FORM-004",
            "experience_years": 0,
            "consultation_fee": 0,
        })
        self.assertTrue(form.is_valid())


class AvailabilityFormTest(TestCase):
    def test_valid_time(self):
        form = AvailabilityForm(data={
            "day": "mon",
            "start_time": "09:00",
            "end_time": "17:00",
        })
        self.assertTrue(form.is_valid())

    def test_end_before_start_invalid(self):
        form = AvailabilityForm(data={
            "day": "mon",
            "start_time": "17:00",
            "end_time": "09:00",
        })
        self.assertFalse(form.is_valid())

    def test_same_time_invalid(self):
        form = AvailabilityForm(data={
            "day": "mon",
            "start_time": "10:00",
            "end_time": "10:00",
        })
        self.assertFalse(form.is_valid())


class DoctorListViewTest(TestCase):
    def setUp(self):
        self.spec = Specialization.objects.create(name="Neurology")
        self.doctor = Doctor.objects.create(
            user=CustomUser.objects.create_user(
                username="drlist", email="list@example.com", password="testpass123"
            ),
            specialization=self.spec,
            license_number="MED-LIST",
            consultation_fee=250.00,
            is_verified=True,
        )

    def test_list_shows_verified_doctors(self):
        response = self.client.get(reverse("doctors:doctor_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "drlist")
        self.assertTemplateUsed(response, "doctors/doctor_list.html")

    def test_list_shows_unverified_doctors(self):
        Doctor.objects.create(
            user=CustomUser.objects.create_user(
                username="drunverified",
                email="unverified@example.com",
                password="testpass123",
            ),
            license_number="MED-UNVERIFIED",
            consultation_fee=100.00,
            is_verified=False,
        )
        response = self.client.get(reverse("doctors:doctor_list"))
        self.assertContains(response, "drlist")
        self.assertContains(response, "drunverified")

    def test_empty_list(self):
        Doctor.objects.all().delete()
        response = self.client.get(reverse("doctors:doctor_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Doctors Available")


class DoctorDetailViewTest(TestCase):
    def setUp(self):
        self.doctor = Doctor.objects.create(
            user=CustomUser.objects.create_user(
                username="drdetail",
                email="detail@example.com",
                password="testpass123",
            ),
            license_number="MED-DETAIL",
            consultation_fee=300.00,
            is_verified=True,
            bio="Detail bio.",
        )

    def test_detail_shows_doctor(self):
        response = self.client.get(
            reverse("doctors:doctor_detail", args=[self.doctor.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "drdetail")
        self.assertContains(response, "Detail bio.")
        self.assertTemplateUsed(response, "doctors/doctor_detail.html")


class DoctorCreateViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="newdr",
            email="newdr@example.com",
            password="testpass123",
        )
        self.spec = Specialization.objects.create(name="Pediatrics")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("doctors:doctor_create"))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('doctors:doctor_create')}",
        )

    def test_logged_in_can_access_create(self):
        self.client.login(email="newdr@example.com", password="testpass123")
        response = self.client.get(reverse("doctors:doctor_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "doctors/doctor_form.html")

    def test_create_doctor(self):
        self.client.login(email="newdr@example.com", password="testpass123")
        response = self.client.post(reverse("doctors:doctor_create"), {
            "specialization": self.spec.pk,
            "license_number": "MED-CREATE",
            "experience_years": 5,
            "qualification": "MD",
            "consultation_fee": 180.00,
            "bio": "Pediatrician.",
        })
        self.assertRedirects(response, reverse("doctors:doctor_list"))
        self.assertTrue(
            Doctor.objects.filter(license_number="MED-CREATE").exists()
        )

    def test_redirect_to_detail_if_already_has_profile(self):
        Doctor.objects.create(
            user=self.user,
            license_number="MED-EXISTING",
            consultation_fee=100.00,
        )
        self.client.login(email="newdr@example.com", password="testpass123")
        response = self.client.get(reverse("doctors:doctor_create"))
        self.assertRedirects(
            response,
            reverse("doctors:doctor_detail", args=[self.user.doctor_profile.pk]),
        )


class DoctorUpdateViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="updatedr",
            email="update@example.com",
            password="testpass123",
        )
        self.doctor = Doctor.objects.create(
            user=self.user,
            license_number="MED-UPDATE",
            consultation_fee=100.00,
            bio="Old bio.",
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("doctors:doctor_update"))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('doctors:doctor_update')}",
        )

    def test_redirect_to_create_if_no_profile(self):
        user2 = CustomUser.objects.create_user(
            username="nodr", email="nodr@example.com", password="testpass123"
        )
        self.client.login(email="nodr@example.com", password="testpass123")
        response = self.client.get(reverse("doctors:doctor_update"))
        self.assertRedirects(response, reverse("doctors:doctor_create"))

    def test_update_doctor(self):
        self.client.login(email="update@example.com", password="testpass123")
        response = self.client.post(reverse("doctors:doctor_update"), {
            "license_number": "MED-UPDATE",
            "experience_years": 10,
            "consultation_fee": 250.00,
            "bio": "Updated bio.",
        })
        self.assertRedirects(response, reverse("doctors:doctor_list"))
        self.doctor.refresh_from_db()
        self.assertEqual(self.doctor.consultation_fee, 250.00)
        self.assertEqual(self.doctor.bio, "Updated bio.")
