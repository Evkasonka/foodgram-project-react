import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEYS")

DEBUG = os.getenv("DEBUG_MODE", False) == "True"

ALLOWED_HOSTS = [os.getenv("ALLOWED_HOSTS", "*"), "*"]

INSTALLED_APPS = [
    "api.apps.ApiConfig",
    "users.apps.UsersConfig",
    "recipes.apps.RecipesConfig",
    "rest_framework",
    "rest_framework.authtoken",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_filters",
    "drf_extra_fields",
    "colorfield",
    "rest_framework_simplejwt",
    "djoser",
    "reportlab",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "foodgram.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "foodgram.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "foodgram"),
        "USER": os.getenv("POSTGRES_USER", "foodgram_user"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "foodgram_user"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}


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


LANGUAGE_CODE = "ru-Ru"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "collected_static"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 6,
}

DJOSER = {
    "LOGIN_FIELD": "email",
    "SERIALIZERS": {
        "user_create": "api.serializers.CustomUserCreateSerializer",
        "user": "api.serializers.CustomUserSerializer",
        "current_user": "api.serializers.CustomUserSerializer",
    },
}


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.User"

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")
ADMIN_EMAIL = "evkasonka@yandex.ru"
LETTERS_SUBJECT = "Код подтверждения"

FILE_NAME_PDF = "shop_сart.pdf"

MIN_COOKING_TIME = 1
MIN_INGREDIENTS_AMOUNT = 1

MIN_RECIPE_COOKING_TIME = 1
