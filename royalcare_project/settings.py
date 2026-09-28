import os
import sys
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Read .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / '.env')
except ImportError:
    pass

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-royalcare-secret-key-prod-2026')
DEBUG = os.environ.get('DEBUG', 'True').lower() in ['true', '1', 'yes']

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',

    # Royal Care Clinic & Lab Core Apps
    'accounts.apps.AccountsConfig',
    'website.apps.WebsiteConfig',
    'patients.apps.PatientsConfig',
    'doctors.apps.DoctorsConfig',
    'appointments.apps.AppointmentsConfig',
    'prescriptions.apps.PrescriptionsConfig',
    'lab.apps.LabConfig',
    'billing.apps.BillingConfig',
    'reports.apps.ReportsConfig',
    'api.apps.ApiConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'royalcare_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'website.context_processors.clinic_info',
            ],
        },
    },
]

WSGI_APPLICATION = 'royalcare_project.wsgi.application'

# Database Configuration
USE_SQLITE = os.environ.get('USE_SQLITE', 'True').lower() in ['true', '1']

if USE_SQLITE:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'royalcare_clinic.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('DB_NAME', 'royalcare_db'),
            'USER': os.environ.get('DB_USER', 'root'),
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '3306'),
            'OPTIONS': {
                'charset': 'utf8mb4',
            },
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Static & Media files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

CSRF_TRUSTED_ORIGINS = [
    'https://*.vercel.app',
    'http://localhost:8000',
    'http://127.0.0.1:8000'
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication URLs
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# Email settings
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'Royal Care Clinic & Lab <noreply@royalcareclinic.in>')

# Clinic Metadata
CLINIC_METADATA = {
    'NAME': os.environ.get('CLINIC_NAME', 'Royal Care Clinic & Lab'),
    'TAGLINE': os.environ.get('CLINIC_TAGLINE', 'Excellence in Healthcare & Diagnostic Precision'),
    'ADDRESS': os.environ.get('CLINIC_ADDRESS', '8, Vijayeswari Street, Razaak Garden, Ayyavoo Colony, Aminjikarai, Chennai, Tamil Nadu 600029.'),
    'PHONE': os.environ.get('CLINIC_PHONE', '+91 98400 12345'),
    'LANDLINE': os.environ.get('CLINIC_LANDLINE', '044-2365 7890'),
    'WHATSAPP': os.environ.get('CLINIC_WHATSAPP', '919840012345'),
    'EMAIL': os.environ.get('CLINIC_EMAIL', 'contact@royalcareclinic.in'),
    'BRAND': os.environ.get('BRAND_POWERED_BY', 'Powered by Virhino.com'),
    'BRAND_URL': os.environ.get('BRAND_URL', 'https://virhino.com'),
    'HOURS_WEEKDAY': 'Mon - Sat: 07:30 AM - 09:30 PM',
    'HOURS_SUNDAY': 'Sunday: 08:00 AM - 01:00 PM',
    'MAP_EMBED_URL': 'https://maps.google.com/maps?q=8,+Vijayeswari+Street,+Razaak+Garden,+Ayyavoo+Colony,+Aminjikarai,+Chennai,+Tamil+Nadu+600029&t=&z=16&ie=UTF8&iwloc=&output=embed',
}
