from pathlib import Path
import os

# Proje kök dizinini belirleme
BASE_DIR = Path(__file__).resolve().parent.parent

# Güvenlik ayarları
SECRET_KEY = 'django-insecure-8@fw=rhl1+7_a$@e+!5j6@ui2=28pqy+@%@j-gam8v9h@otn0d'

# Debug modu (Prodüksiyon için False yapılmalı)
DEBUG = True   

# İzin verilen hostlar
# Bu ayar, hangi hostlardan gelen isteklere izin verileceğini belirler.
ALLOWED_HOSTS = [ '127.0.0.1' , 'localhost', '192.168.1.35']

# Uygulamalar
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # GetDogCo uygulamaları
    'getdogco',

    # Ekstra kütüphaneler
    'crispy_forms',
    "crispy_bootstrap4",
    "django_cleanup",
    'ckeditor',
]

# Crispy Forms için Bootstrap 4 desteği
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4" 

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# URL Yapılandırması
ROOT_URLCONF = 'blog.urls'

# Şablon ayarları
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI uygulaması
WSGI_APPLICATION = 'getdogco.wsgi.application'

# Veritabanı ayarları
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Şifre doğrulama ayarları
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Dil ve Zaman Ayarları
LANGUAGE_CODE = 'tr'

TIME_ZONE = 'Europe/Istanbul'

USE_I18N = True

USE_TZ = True

# Statik dosya ayarları
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')    

# Ortam (Medya) dosyaları
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Varsayılan birincil anahtar tipi
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CRISPY FORMS Ayarları
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"
