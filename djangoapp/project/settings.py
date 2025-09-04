# app/core/settings.py

import environ
from pathlib import Path

# Configuração do django-environ
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Lendo o arquivo .env
environ.Env.read_env(BASE_DIR.parent / '.env')

# --- Variáveis de Segurança ---
SECRET_KEY = env('DJANGO_SECRET_KEY')
DEBUG = env('DJANGO_DEBUG')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

# --- Definição das Aplicações ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Nossos apps (essencial adicioná-los aqui)
    'rest_framework',
    'accounts',
    'documents.apps.DocumentsConfig',
    'dialysis',
    'billing',
    'audit',
    'organization',
    'parameters',

    # Libs de terceiros
    'storages',
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

# Assumindo que o nome do projeto é 'core'
ROOT_URLCONF = 'project.urls'
WSGI_APPLICATION = 'project.wsgi.application'

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
            ],
        },
    },
]

# --- Configuração do Banco de Dados ---
# django-environ lê a variável DATABASE_URL do .env e configura tudo
DATABASES = {
    'default': env.db(),
}

# --- Validação de Senhas ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Internacionalização ---
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# --- Arquivos Estáticos e de Mídia ---
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Variáveis lidas do .env para configurar a conexão com o MinIO
MINIO_ENDPOINT = env('MINIO_ENDPOINT')
MINIO_ACCESS_KEY = env('MINIO_ROOT_USER') # Usando as credenciais root
MINIO_SECRET_KEY = env('MINIO_ROOT_PASSWORD')
MINIO_BUCKET_PATIENT_DOCS = env('MINIO_BUCKET_PATIENT_DOCS')
MINIO_BUCKET_GUIDE_DOCS = env('MINIO_BUCKET_GUIDE_DOCS')
MINIO_USE_HTTPS = False # Em desenvolvimento, usamos HTTP

# --- Tipo de Chave Primária Padrão ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'accounts.CustomUser'
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'