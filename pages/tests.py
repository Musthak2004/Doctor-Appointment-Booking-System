from django.test import TestCase
from django.urls import reverse


class ContactPageViewTest(TestCase):
    def test_contact_page_status_code(self):
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)

    def test_contact_page_template(self):
        response = self.client.get(reverse("contact"))
        self.assertTemplateUsed(response, "contact.html")

    def test_contact_page_resolves(self):
        response = self.client.get("/contact/")
        self.assertEqual(response.status_code, 200)

    def test_contact_page_contains_heading(self):
        response = self.client.get(reverse("contact"))
        self.assertContains(response, "Contact Us")


class HomePageViewTest(TestCase):
    def test_home_page_status_code(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_home_page_template(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home.html")

    def test_home_page_url_resolves(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_home_page_contains_heading(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Book Your")
