PythonAnywhere (Free Plan) Deployment Guide for DocBook
======================================================

Prerequisites
--------------
- A PythonAnywhere account (free tier)
- Git repository containing this project
- Python 3.12+ (check available versions in your PythonAnywhere account)

Steps
-----

1. Open a Bash console on PythonAnywhere and clone the repo:

       git clone https://github.com/YOUR_USERNAME/Doctor-Appointment-Booking-System.git
       cd Doctor-Appointment-Booking-System

2. Create and activate a virtual environment:

       python -m venv .venv
       source .venv/bin/activate

3. Install dependencies:

       pip install -r requirements.txt

4. Copy the environment file and edit it:

       cp .env.example .env

   Generate a real SECRET_KEY:

       python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

   Edit .env:
       - Set DEBUG=False
       - Replace SECRET_KEY with the generated key
       - Set ALLOWED_HOSTS to include your PythonAnywhere domain
       - Set CSRF_TRUSTED_ORIGINS for your PythonAnywhere domain

5. Run migrations and collect static files:

       python manage.py migrate
       python manage.py collectstatic

6. Create a superuser (optional but recommended):

       python manage.py createsuperuser

7. Configure the Web app in PythonAnywhere:
   a. Go to the Web tab and create a new web app.
   b. Choose "Manual configuration" and select Python 3.x.
   c. Under "Code":
      - Set "Source code" to the project directory (e.g., /home/username/Doctor-Appointment-Booking-System)
      - Set "Working directory" to the same path
      - Open the "WSGI configuration file" and replace its contents with the contents of
        deployment/pythonanywhere_wsgi.py (or upload that file and set the path to it)
   d. Under "Virtualenv":
      - Set to the path of the virtualenv created in step 2
   e. Under "Environment variables":
      - The wsgi.py will load .env automatically, but you can also set individual variables here
      - At minimum, set: SECRET_KEY, DEBUG=False, ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS
   f. Under "Static files" (for media uploads):
      - URL: /media/
      - Directory: /home/username/Doctor-Appointment-Booking-System/media
   g. Reload the web app.

8. Verify the deployment:
   - Visit https://yourusername.pythonanywhere.com/
   - Test signup, login, and core flows

Notes
-----
- The free plan uses SQLite which is already configured. No database setup needed.
- WhiteNoise serves static files (CSS/JS). No separate static file mapping is needed.
- Media files (user uploads) require the static file mapping in step 7f.
- Free plan web apps go to sleep after inactivity. A manual reload is needed after sleep.
- Logs are available in the Web tab under "Logs" section.
- To troubleshoot, check the error log at:
  https://www.pythonanywhere.com/user/yourusername/files/var/log/yourusername.pythonanywhere.com.error.log
