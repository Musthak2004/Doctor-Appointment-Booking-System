# DocBook - Doctor Appointment Booking System

A web-based platform built with **Django 6.0** for patients to find doctors, book appointments, make payments, receive prescriptions, and leave reviews.

## Features

- **User Authentication** — Custom user model (`CustomUser`) with email-based login and three roles: Patient, Doctor, Admin
- **Role-based Signup** — Register as Patient, Doctor, or Admin with a dedicated signup flow
- **Patient Profiles** — Create and manage personal medical info (DOB, blood group, address, emergency contact, medical history)
- **Doctor Listings** — Browse doctors by specialization, experience, consultation fee, and verification status
- **Doctor Profiles** — Detailed profiles with bio, availability schedules, patient reviews, and profile picture uploads
- **Doctor Registration** — Dedicated form for doctors with specialization, license number, qualifications, and workplace info
- **Availability Management** — Doctors can manage weekly availability time slots (day, start/end time)
- **Appointment Booking** — Book appointments with date/time validation against doctor availability; double-booking prevented via unique constraints
- **Appointment Management** — Patients view their bookings; doctors manage appointments (confirm, cancel) with role-specific dashboards
- **Payments** — Pay for appointments (Card, PayPal, Bank Transfer, Cash) with status tracking (Pending, Completed, Failed, Refunded)
- **Prescriptions** — Doctors create digital prescriptions with diagnosis, notes, and medicine items (name, dosage, frequency, duration, instructions)
- **Reviews & Ratings** — Patients rate doctors (1–5 stars) and leave comments on completed appointments
- **Role-based Dashboards** — Separate views for patients and doctors (appointments, payments, prescriptions)
- **Responsive UI** — Modern, mobile-friendly design with custom CSS and vanilla JS
- **Error Pages** — Custom 400, 403, 404, and 500 pages
- **Django Admin** — Full admin interface for managing users, patients, doctors, appointments, payments, prescriptions, and reviews

## Tech Stack

| Layer     | Technology                           |
|-----------|--------------------------------------|
| Backend   | Python 3.13, Django 6.0.6           |
| Database  | SQLite                               |
| Frontend  | Django Templates, Custom CSS, Vanilla JS |
| Auth      | django.contrib.auth (email-based login) |

## Data Model

```
CustomUser
 ├── 1:1 PatientProfile
 └── 1:1 DoctorProfile

Specialization
 └── 1:N DoctorProfile

DoctorProfile
 ├── 1:N DoctorAvailability
 ├── 1:N Appointment
 └── 1:N Review

PatientProfile
 ├── 1:N Appointment
 └── 1:N Review

Appointment
 ├── 1:1 Payment
 └── 1:1 Prescription
```

## Project Structure

```
├── accounts/          # Custom user model, auth forms, signup view, context processors
├── appointments/      # Appointment booking, listing, and detail views
├── doctors/           # Doctor profiles, specialization, availability management
├── pages/             # Static pages (home page)
├── patients/          # Patient profile CRUD
├── payments/          # Payment processing and history
├── prescriptions/     # Prescription creation and medicine items
├── reviews/           # Patient reviews and ratings
├── django_project/    # Project settings, root URL conf, WSGI/ASGI
├── static/            # CSS and JS assets
└── templates/         # Base template, registration templates, error pages
```

## Getting Started

```bash
git clone https://github.com/Musthak2004/Doctor-Appointment-Booking-System.git
cd Doctor-Appointment-Booking-System
python -m venv .venv
.venv\Scripts\activate    # Windows | source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to view the app.

## Tests

```bash
python manage.py test
```

## License

MIT
