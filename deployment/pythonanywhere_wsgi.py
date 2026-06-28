"""
PythonAnywhere WSGI configuration for DocBook.

How to use:
1. Open the PythonAnywhere Web tab.
2. Under "Code", find the "WSGI configuration file" setting.
3. Replace its contents with the contents of this file, or
   set the WSGI file path to point to this file.
4. Adjust the PROJECT_PATH and DJANGO_SETTINGS_MODULE if needed.
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# ── Paths ────────────────────────────────────────────────────────────────────
PROJECT_PATH = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_PATH / '.env')

sys.path.append(str(PROJECT_PATH))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

# ── Application ──────────────────────────────────────────────────────────────
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
