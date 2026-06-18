from django.test import TestCase
from django.urls import reverse

from .models import CustomUser
from .forms import CustomUserCreationForm


class CustomUserModelTest(TestCase):
    def test_create_patient_user(self):
        user = CustomUser.objects.create_user(
            username="patient1",
            email="patient@example.com",
            password="testpass123",
            user_type="PATIENT",
        )
        self.assertEqual(user.email, "patient@example.com")
        self.assertEqual(user.user_type, "PATIENT")
        self.assertTrue(user.check_password("testpass123"))

    def test_create_doctor_user(self):
        user = CustomUser.objects.create_user(
            username="doctor1",
            email="doctor@example.com",
            password="testpass123",
            user_type="DOCTOR",
        )
        self.assertEqual(user.user_type, "DOCTOR")

    def test_create_admin_user(self):
        user = CustomUser.objects.create_user(
            username="admin1",
            email="admin@example.com",
            password="testpass123",
            user_type="ADMIN",
        )
        self.assertEqual(user.user_type, "ADMIN")

    def test_default_user_type_is_patient(self):
        user = CustomUser.objects.create_user(
            username="defaultuser",
            email="default@example.com",
            password="testpass123",
        )
        self.assertEqual(user.user_type, "PATIENT")

    def test_email_is_unique(self):
        CustomUser.objects.create_user(
            username="user1",
            email="same@example.com",
            password="testpass123",
        )
        with self.assertRaises(Exception):
            CustomUser.objects.create_user(
                username="user2",
                email="same@example.com",
                password="testpass123",
            )

    def test_user_str_returns_email(self):
        user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        self.assertEqual(str(user), "test@example.com")

    def test_username_field_is_email(self):
        self.assertEqual(CustomUser.USERNAME_FIELD, "email")


class CustomUserCreationFormTest(TestCase):
    def test_valid_form(self):
        form = CustomUserCreationForm(data={
            "username": "newuser",
            "email": "new@example.com",
            "user_type": "PATIENT",
            "phone_number": "1234567890",
            "password1": "StrongPass1!",
            "password2": "StrongPass1!",
        })
        self.assertTrue(form.is_valid())

    def test_password_mismatch(self):
        form = CustomUserCreationForm(data={
            "username": "newuser",
            "email": "new@example.com",
            "user_type": "PATIENT",
            "password1": "StrongPass1!",
            "password2": "WrongPass1!",
        })
        self.assertFalse(form.is_valid())

    def test_duplicate_email(self):
        CustomUser.objects.create_user(
            username="existing",
            email="dup@example.com",
            password="testpass123",
        )
        form = CustomUserCreationForm(data={
            "username": "newuser",
            "email": "dup@example.com",
            "user_type": "PATIENT",
            "password1": "StrongPass1!",
            "password2": "StrongPass1!",
        })
        self.assertFalse(form.is_valid())


class SignUpViewTest(TestCase):
    def test_signup_page_status_code(self):
        response = self.client.get(reverse("accounts:signup"))
        self.assertEqual(response.status_code, 200)

    def test_signup_page_template(self):
        response = self.client.get(reverse("accounts:signup"))
        self.assertTemplateUsed(response, "registration/signup.html")

    def test_signup_creates_user(self):
        response = self.client.post(reverse("accounts:signup"), {
            "username": "signupuser",
            "email": "signup@example.com",
            "user_type": "PATIENT",
            "password1": "StrongPass1!",
            "password2": "StrongPass1!",
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))
        self.assertTrue(CustomUser.objects.filter(email="signup@example.com").exists())
