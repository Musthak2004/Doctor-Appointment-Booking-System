# DocBook - Doctor Appointment Booking System

A web-based platform built with **Django 6.0** that allows patients to find doctors and book appointments online.

## Features

- **User Authentication** — Custom user model with three roles: Patient, Doctor, Admin
- **Role-based signup** — Register as Patient, Doctor, or Admin
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

**Early development.** The authentication system and landing page are complete. Core booking features (doctor search, appointment scheduling, user dashboard) are not yet implemented.

### What's Built
- [x] Custom user model (`CustomUser`) with email login and user types
- [x] Sign-up and login flows
- [x] Django admin configuration for user management
- [x] Responsive base template with navigation and footer
- [x] Landing page with hero, stats, features, and how-it-works sections
- [x] Pages app with structured views and URL routing
- [x] Test suite for accounts (model, form, view tests)
- [x] Test suite for pages (home page view tests)

### In Progress / Planned
- [ ] Doctor search and filtering
- [ ] Appointment booking system
- [ ] User dashboard (patients & doctors)
- [ ] Doctor profiles and clinic management
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
