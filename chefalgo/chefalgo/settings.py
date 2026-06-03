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
ALLOWED_HOSTS = []

# --- UYGULAMALAR ---
INSTALLED_APPS = [
    'accounts',
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
    'default': 
    {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'chefdb',  # pgAdmin'de verdiğin isimle birebir aynı olmalı
        'USER': 'postgres',
        'PASSWORD': '6161', # Kurulumda belirlediğin şifre
        'HOST': 'localhost',
        'PORT': '5432',
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
EMAIL_HOST_USER = "chefalgo@gmail.com"
EMAIL_HOST_PASSWORD = "uygulama_sifresi"

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER  # İyi pratik, ama zorunlu değil

# Gönderici adresi
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Buraya uygulama şifresini aldığın KENDİ GMAIL ADRESİNİ yaz:
EMAIL_HOST_USER = 'kudusumeyye@gmail.com' 

# Google'dan aldığın 16 haneli şifre (Boşluksuz yazılması tercih edilir)
EMAIL_HOST_PASSWORD = 'ugbpyxckdwmlulbq' 

# Mailin kimden geldiğini gösteren "Gönderen" kısmı
DEFAULT_FROM_EMAIL = 'ChefAlgo Karar Destek Sistemi <senin.gmail.adresin@gmail.com>'

# Giriş ve Çıkış yönlendirmeleri
LOGIN_REDIRECT_URL = 'panel'  # Giriş yapınca direkt Dashboard'a gider
LOGOUT_REDIRECT_URL = 'home'   # Çıkış yapınca Landing Page'e döner
LOGIN_URL = 'accounts:login'   # Giriş yapmamışları buraya atar