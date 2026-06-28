# DocBook — Doctor Appointment Booking System

A production-ready Django web application that connects patients with healthcare providers. Patients browse verified doctors, book appointments, pay online, receive digital prescriptions, and leave reviews. Doctors manage availability, appointments, payments, and prescriptions through a dedicated dashboard.

Built with **Django 6.0** / **Python 3.13**, tested with **173 automated tests**, and deployable to **PythonAnywhere** with zero configuration.

---

## Features

### For Patients
- **Role-based signup** — Register as a Patient and create a medical profile (DOB, blood group, emergency contact, medical history)
- **Find Doctors** — Browse by specialization, experience, consultation fee, and verification status
- **Book Appointments** — Pick a date and time; availability is validated in real time against doctor schedules; double-booking prevented via database unique constraints
- **Make Payments** — Pay by Card, PayPal, Bank Transfer, or Cash; full payment history with status tracking
- **View Prescriptions** — Access digital prescriptions with medicine name, dosage, frequency, duration, and instructions
- **Write Reviews** — Rate doctors (1–5 stars) and leave comments on completed appointments
- **Role-specific Dashboard** — Centralized view of appointments, payments, prescriptions, and reviews

### For Doctors
- **Doctor Registration** — Dedicated form for specialization, license number, qualifications, hospital affiliation, bio, and profile picture
- **Availability Management** — Set weekly time slots (per day, start/end time); patients can only book within these windows
- **Appointment Dashboard** — View and manage incoming appointments from patients
- **Create Prescriptions** — Add diagnosis, notes, and multiple medicine items per appointment
- **Payment Overview** — See payments received from patients
- **Profile Management** — Edit professional information and verification status

### For Admins
- **Django Admin Interface** — Full CRUD for all models
- **Bulk Actions** — Confirm/cancel appointments, mark payments as completed/refunded
- **Inline Editing** — Prescription items managed inline within prescriptions
- **Search & Filter** — Every admin list includes search fields, filters, and date hierarchies

### General
- **Email-based Authentication** — Login with email instead of username
- **Responsive UI** — Mobile-first design with custom CSS, BEM naming, and vanilla JavaScript
- **Scroll-triggered Animations** — IntersectionObserver-based reveal system with staggered delays; respects `prefers-reduced-motion`
- **CSRF Protection** — Enabled globally; configurable trusted origins via environment variable
- **Error Pages** — Custom 400, 403, 404 (extend `base.html`), and standalone 500 page with animation
- **Contact Page** — Static contact form with clinic information

---

## Tech Stack

| Layer        | Technology |
|-------------|------------|
| Backend      | Python 3.13, Django 6.0.6 |
| Database     | SQLite (development), portable to PostgreSQL/MySQL |
| Frontend     | Django Template Language, Custom CSS with BEM, Vanilla JS |
| Auth         | `django.contrib.auth` with custom `AbstractUser` (email as username) |
| Static Files | WhiteNoise (production-ready serving) |
| File Storage | Django `FileSystemStorage` with `Pillow` for image uploads |
| Deployment   | PythonAnywhere, Gunicorn, WhiteNoise |
| Environment  | `python-dotenv` for `.env` configuration |

---

## Data Model

```
CustomUser (AbstractUser, email as USERNAME_FIELD)
 ├── 1:1 Patient         (medical profile: DOB, gender, blood group, address, history)
 └── 1:1 Doctor          (professional profile: specialization, license, fee, bio, photo)
      └── 1:N DoctorAvailability  (weekly time slots per doctor)

Specialization (lookup table for doctor specialties)

Doctor ──1:N── Appointment
Patient ──1:N── Appointment
        ┌──────┘
        ▼
Appointment (status: PENDING → CONFIRMED → COMPLETED/CANCELLED/REJECTED)
 ├── 1:1 Payment         (method, amount, transaction_id, status)
 └── 1:1 Prescription    (diagnosis, notes, 1:N PrescriptionItems)

Doctor  ──1:N── Review
Patient ──1:N── Review
              └── Appointment (1 review per appointment enforced by OneToOneField)
```

---

## Architecture Highlights

### Reusable Mixins (`accounts/mixins.py`)

Three custom mixins eliminate ~25+ lines of duplicated dispatch logic across views:

| Mixin | Purpose |
|-------|---------|
| `UserTypeRequiredMixin` | Redirects unauthenticated users to login; redirects wrong user-type to home |
| `ProfileExistsMixin` | Ensures the user has a related profile before accessing the view |
| `ProfileGetObjectMixin` | Sets the view's object from the user's related profile; used by UpdateView/DetailView |

### Consistent Choices

All choice fields use Django `TextChoices` / `IntegerChoices` enums:

| Model | Field | Choices Class |
|-------|-------|-------------|
| `CustomUser` | `user_type` | `UserType (PATIENT, DOCTOR, ADMIN)` |
| `Appointment` | `status` | `Status (PENDING, CONFIRMED, COMPLETED, CANCELLED, REJECTED)` |
| `Patient` | `gender` | `Gender (MALE, FEMALE, OTHER)` |
| `DoctorAvailability` | `day` | `Day (MON-SUN)` |
| `Payment` | `status`, `method` | `Status`, `Method` |
| `Review` | `rating` | `Rating (1–5 IntegerChoices)` |

### Pagination

All list views support pagination (20 items/page) with a shared `_pagination.html` include template rendering numbered page links with previous/next navigation.

---

## Project Structure

```
├── accounts/              # CustomUser model, signup form/view, mixins, context processors
├── appointments/          # Appointment model, form (availability validation), views
├── doctors/               # Doctor/Specialization/Availability models and views
├── pages/                 # Home and Contact page views
├── patients/              # Patient model (medical profile) and views
├── payments/              # Payment model, form, and views (patient + doctor lists)
├── prescriptions/         # Prescription + PrescriptionItem models, inline admin
├── reviews/               # Review model, form, and views
├── django_project/        # Settings, root URL conf, WSGI
├── deployment/            # PythonAnywhere WSGI config + deployment guide
├── static/                # CSS (`base.css`, 2162 lines) and JS (`app.js`)
├── staticfiles/           # collectstatic output (gitignored)
├── templates/             # Base template, home, contact, error pages, pagination partial
│   └── registration/      # Login and signup templates
│   └── doctors/           # Doctor list, detail, form, availability templates
│   └── appointments/      # Appointment list, detail, form templates
│   └── patients/          # Patient detail, form templates
│   └── payments/          # Payment list, detail, form templates
│   └── prescriptions/     # Prescription list, detail, form templates
│   └── reviews/           # Review list, detail, form templates
└── media/                 # User-uploaded files (profile pictures)
```

---

## Getting Started

### Prerequisites

- Python 3.13+
- pip
- virtualenv (recommended)

### Installation

```bash
# Clone the repository
git clone https://github.com/Musthak2004/Doctor-Appointment-Booking-System.git
cd Doctor-Appointment-Booking-System

# Create and activate a virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env if needed (defaults work for local development)

# Run migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Start the development server
python manage.py runserver
```

Visit **http://127.0.0.1:8000** to use the application.

---

## Configuration

The project uses environment variables via `.env` (loaded with `python-dotenv` in `settings.py` and `wsgi.py`).

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | — | Django secret key. Generate with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DEBUG` | `True` | Set to `False` in production |
| `ALLOWED_HOSTS` | `127.0.0.1,localhost` | Comma-separated hostnames |
| `CSRF_TRUSTED_ORIGINS` | — | Comma-separated origins (e.g. `https://yourdomain.pythonanywhere.com`) |
| `DJANGO_LOG_LEVEL` | `INFO` | Logging verbosity |

**Security note**: When `DEBUG=False`, the app enforces:
- `SECURE_SSL_REDIRECT = True`
- `SECURE_HSTS_SECONDS = 31536000`
- `SESSION_COOKIE_SECURE = True`
- `CSRF_COOKIE_SECURE = True`
- WhiteNoise with compressed manifest storage

---

## Testing

```bash
# Run the full test suite
python manage.py test

# Run tests for a specific app
python manage.py test appointments
python manage.py test payments

# Run with verbose output
python manage.py test -v2
```

**Test coverage**: 173 tests across all 8 apps:

| App | Tests | What's Covered |
|-----|-------|---------------|
| `accounts` | 14 | User model, creation form, signup view, update form |
| `patients` | 15 | Patient model, form, create/update/detail views |
| `doctors` | 30 | Doctor model, availability model, forms, all views |
| `appointments` | 27 | Appointment model, form (availability validation), views |
| `payments` | 23 | Payment model, form, create/detail/list views |
| `prescriptions` | 26 | Prescription/PrescriptionItem models, forms, views |
| `reviews` | 6 | Review model, form, list/detail views |
| `pages` | 8 | Home and Contact page views |

---

## Deployment (PythonAnywhere)

A complete deployment guide is included at `deployment/pythonanywhere_guide.md.txt`.

Quick-start:

```bash
# On PythonAnywhere bash console:
git clone https://github.com/Musthak2004/Doctor-Appointment-Booking-System.git
cd Doctor-Appointment-Booking-System
python -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env
# Edit .env: set SECRET_KEY, DEBUG=False, ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS
.venv/bin/python manage.py migrate
.venv/bin/python manage.py collectstatic
```

Then configure the WSGI file in the PythonAnywhere web tab using `deployment/pythonanywhere_wsgi.py` as a reference.

---

## License

MIT

---

## Acknowledgments

Built as a comprehensive Django portfolio project demonstrating:

- Custom user models and email-based authentication
- Role-based access control with reusable mixins
- Complex relational data models with unique constraints
- Form validation (availability checking, timezone-aware date comparison)
- Django admin customization with inline models and bulk actions
- Production deployment configuration (WhiteNoise, Gunicorn, PythonAnywhere)
- Full test coverage for models, forms, and views
- Modern UI with CSS animations and accessibility support
