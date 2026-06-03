"""
Django settings for chefalgo project.
Optimized for Modular Architecture (Templates & Static)
"""

import os
from pathlib import Path

# Projenin ana dizini
BASE_DIR = Path(__file__).resolve().parent.parent

# --- GÜVENLİK AYARLARI ---
SECRET_KEY = 'django-insecure-9j!$qyh3l^6orkosoxz^w5hxm*b#w!l5aj^q=#4aduwxp2ot&j'
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver']

# --- UYGULAMALAR ---
INSTALLED_APPS = [
    'accounts.apps.AccountsConfig',
    'dashboard', # Senin ana uygulaman
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'chefalgo.urls'

# --- TEMPLATE (ŞABLON) AYARLARI ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # DİKKAT: Ana dizindeki 'templates' klasörünü buraya bağladık
        'DIRS': [BASE_DIR / 'templates'], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'chefalgo.wsgi.application'

# --- VERİTABANI ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# --- ŞİFRE DOĞRULAMA ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- DİL VE SAAT (TÜRKİYE) ---
LANGUAGE_CODE = 'tr-tr'
TIME_ZONE = 'Europe/Istanbul'
USE_I18N = True
USE_TZ = True

# --- STATİK DOSYALAR (CSS, JS, IMAGES) ---
STATIC_URL = 'static/'

# DİKKAT: style.css'i koyduğumuz ana dizindeki static klasörünü buraya bağladık
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Canlıya geçişte (collectstatic) dosyaların toplanacağı yer
STATIC_ROOT = BASE_DIR / 'staticfiles'

# --- MEDYA DOSYALARI (YEMEK RESİMLERİ) ---
# Tariflerin resimlerini yükleyebilmek için bu ayar şarttır
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# --- DEFAULT AUTO FIELD ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- MAİL GÖNDERİM (SMTP) AYARLARI ---
# Geliştirme (Console) backend'ini kapatıp, SMTP'yi aktif ediyoruz
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Gmail hesabın
EMAIL_HOST_USER = 'chefalgo@gmail.com'

# Google'dan aldığın 16 haneli şifre (Boşluksuz yazılması tercih edilir)
EMAIL_HOST_PASSWORD = 'xcslqqxnkmkajupu'

DEFAULT_FROM_EMAIL = 'ChefAlgo <chefalgo@gmail.com>'


