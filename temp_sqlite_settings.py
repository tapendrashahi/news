import os
import sys
from pathlib import Path

# Temporarily use SQLite
os.environ['DJANGO_SETTINGS_MODULE'] = 'gis.settings'

# Backup current settings
BASE_DIR = Path(__file__).resolve().parent

# Override database to use SQLite
from django.conf import settings
if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
    )
