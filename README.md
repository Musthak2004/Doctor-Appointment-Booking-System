# DocBook - Doctor Appointment Booking System

A web-based platform built with **Django 6.0** that allows patients to find doctors and book appointments online.

## Features

- **User Authentication** — Custom user model with three roles: Patient, Doctor, Admin
- **Role-based signup** — Register as Patient, Doctor, or Admin
- **Patient Profiles** — Create and manage personal medical information
- **Doctor Listings** — Browse doctors with specialization, experience, fees, and verification status
- **Doctor Profiles** — Detailed profiles with availability schedules, patient reviews, and profile pictures
- **Doctor Registration** — Doctors can register with a dedicated form (specialization, license, bio, profile picture)
- **Responsive UI** — Modern, mobile-friendly design with custom CSS and vanilla JS
- **Landing Page** — Hero section, stats counter, feature highlights, and call-to-action

## Tech Stack

| Layer     | Technology                           |
|-----------|--------------------------------------|
| Backend   | Python 3.13, Django 6.0.6           |
| Database  | SQLite                               |
| Frontend  | Django Templates, Custom CSS, Vanilla JS |
| Auth      | django.contrib.auth (email-based login) |

## Project Status

**Early development.** Authentication, patient profiles, and doctor listings are built. Booking and appointment scheduling are not yet implemented.

### What's Built
- [x] Custom user model (`CustomUser`) with email login and user types
- [x] Sign-up and login flows
- [x] Django admin configuration for user management
- [x] Responsive base template with navigation and footer
- [x] Landing page with hero, stats, features, and how-it-works sections
- [x] Pages app with structured views and URL routing
- [x] Patient profiles — create, update, and view medical info
- [x] Doctor profiles — specialization, qualifications, fees, availability, reviews, profile pictures
- [x] Doctor listing page with doctor cards (profile pic, verification badge, specialty, fee) and empty state
- [x] Doctor registration and profile editing forms
- [x] Media file handling for profile picture uploads
- [x] Navigation linking across all pages (Find Doctors, My Dashboard)
- [x] Test suites for accounts (17 tests), patients (17 tests), doctors (32 tests), pages (4 tests)

### In Progress / Planned
- [ ] Appointment booking system
- [ ] User dashboard
- [ ] About, Contact, FAQ pages
- [ ] Booking confirmation and notifications

## Getting Started

```bash
git clone https://github.com/Musthak2004/Doctor-Appointment-Booking-System.git
cd Doctor-Appointment-Booking-System
python -m venv .venv
.venv\Scripts\activate    # Windows
pip install django
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to view the app.

## License

MIT
