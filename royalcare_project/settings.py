import os
from pathlib import Path
from datetime import timedelta
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

# Read .env file
env = environ.Env()
env_file = os.path.join(BASE_DIR, '.env')
if os.path.exists(env_file):
    environ.Env.read_env(env_file)

SECRET_KEY = env('SECRET_KEY', default='django-insecure-royalcare-secret-key-default-2026')
DEBUG = env.bool('DEBUG', default=True)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])

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
USE_SQLITE = env.bool('USE_SQLITE', default=True)

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
            'NAME': env('DB_NAME', default='royalcare_db'),
            'USER': env('DB_USER', default='root'),
            'PASSWORD': env('DB_PASSWORD', default=''),
            'HOST': env('DB_HOST', default='localhost'),
            'PORT': env('DB_PORT', default='3306'),
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
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='Royal Care Clinic & Lab <noreply@royalcareclinic.in>')

# Clinic Metadata
CLINIC_METADATA = {
    'NAME': env('CLINIC_NAME', default='Royal Care Clinic & Lab'),
    'TAGLINE': env('CLINIC_TAGLINE', default='Excellence in Healthcare & Diagnostic Precision'),
    'ADDRESS': env('CLINIC_ADDRESS', default='8, Vijayeswari Street, Razaak Garden, Ayyavoo Colony, Aminjikarai, Chennai, Tamil Nadu 600029.'),
    'PHONE': env('CLINIC_PHONE', default='+91 98400 12345'),
    'LANDLINE': env('CLINIC_LANDLINE', default='044-2365 7890'),
    'WHATSAPP': env('CLINIC_WHATSAPP', default='919840012345'),
    'EMAIL': env('CLINIC_EMAIL', default='contact@royalcareclinic.in'),
    'BRAND': env('BRAND_POWERED_BY', default='Powered by Virhino.com'),
    'BRAND_URL': env('BRAND_URL', default='https://virhino.com'),
    'HOURS_WEEKDAY': 'Mon - Sat: 07:30 AM - 09:30 PM',
    'HOURS_SUNDAY': 'Sunday: 08:00 AM - 01:00 PM',
    'MAP_EMBED_URL': 'https://maps.google.com/maps?q=8,+Vijayeswari+Street,+Razaak+Garden,+Ayyavoo+Colony,+Aminjikarai,+Chennai,+Tamil+Nadu+600029&t=&z=16&ie=UTF8&iwloc=&output=embed',
}
