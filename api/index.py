import os
import sys
import shutil
from pathlib import Path

# Add project root directory to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'royalcare_project.settings')

# Ensure sqlite DB is in writable /tmp on Vercel
tmp_db = Path('/tmp/royalcare_clinic.sqlite3')
orig_db = BASE_DIR / 'royalcare_clinic.sqlite3'
if orig_db.exists() and not tmp_db.exists():
    try:
        shutil.copy2(orig_db, tmp_db)
    except Exception:
        pass

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()

