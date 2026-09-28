import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'royalcare_project.settings')
django.setup()

from django.test import Client
from accounts.models import User

client = Client()

print("=== 1. Testing Public Website Endpoints ===")
urls = [
    '/',
    '/about/',
    '/services/',
    '/lab-services/',
    '/doctors/',
    '/timings/',
    '/contact/',
    '/book-appointment/',
    '/book-lab-test/',
    '/accounts/login/',
]
for u in urls:
    res = client.get(u)
    print(f"GET {u} -> Status: {res.status_code}")
    assert res.status_code == 200, f"Failed on {u}"

print("\n=== 2. Testing Authenticated Staff & Analytics Endpoints ===")
admin_user = User.objects.get(username='admin')
client.force_login(admin_user)

auth_urls = [
    '/accounts/dashboard/',
    '/patients/',
    '/doctors/',
    '/appointments/',
    '/lab/',
    '/lab/catalog/',
    '/lab/orders/',
    '/prescriptions/',
    '/billing/',
    '/reports/dashboard/',
    '/reports/export/excel/',
    '/reports/export/powerbi/',
    '/reports/export/csv/FactAppointments/',
    '/api/analytics/summary/',
    '/api/patients/',
    '/api/doctors/',
    '/api/appointments/',
    '/api/lab/tests/',
]
for u in auth_urls:
    res = client.get(u)
    print(f"GET {u} -> Status: {res.status_code}")
    assert res.status_code == 200, f"Failed on {u}"

print("\nALL INTEGRATION CHECKS PASSED PERFECTLY!")
