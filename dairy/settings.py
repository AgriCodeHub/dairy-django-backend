import os
from pathlib import Path

# Set the base directory of the project.
BASE_DIR = Path(__file__).resolve().parent.parent

# Keep this key secret in production. It's used for various security measures.
SECRET_KEY = "django-insecure-+^mi(j_hrx($6yq_@e5b)#uhfrck(&j0ndjb6((kx4ds^#*l*v"

# Enable or disable debugging. Don't use this in a production environment.
DEBUG = True

# List of allowed host/domain names for this site. Empty for now.
ALLOWED_HOSTS = []

# Define the applications used in this Django project.
INSTALLED_APPS = [
    # Django Core Apps
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party Apps
    "rest_framework",
    "rest_framework.authtoken",
    "djoser",
    "corsheaders",
    "django_filters",
    "drf_yasg",
    # Custom Apps
    "core",
    "users",
    "production",
    "reproduction",
    "health",
    "inventory",
]

# Middleware classes. They process requests and responses globally.
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Root URL configuration and WSGI application.
ROOT_URLCONF = "dairy.urls"
WSGI_APPLICATION = "dairy.wsgi.application"

# Database configuration. Currently set to use SQLite.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation settings.
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
# Add the custom validator for CowBreed model
COW_BREED_VALIDATORS = [
    "users.validators.CustomCowBreedValidator.validate_breed_name",
]

# Internationalization settings.
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images) settings.
STATIC_URL = "static/"

# Default primary key field type.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CORS (Cross-Origin Resource Sharing) settings.
CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
]

# Define a custom User model for authentication.
AUTH_USER_MODEL = "users.CustomUser"

# Djoser configuration for user serializers.
DJOSER = {
    "SERIALIZERS": {
        "user_create": "users.serializers.CustomUserCreateSerializer",
        "user": "users.serializers.CustomUserSerializer",
    },
}

# REST framework configuration with Token Authentication.
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ]
}
