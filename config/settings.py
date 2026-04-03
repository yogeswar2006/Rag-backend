

from pathlib import Path
from datetime import timedelta
import os
from dotenv import load_dotenv
load_dotenv()
import dj_database_url
import cloudinary

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG")

ALLOWED_HOSTS = ["rag-backend-pcij.onrender.com"]

AUTH_USER_MODEL = "accounts.User"

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    "cloudinary",
    "cloudinary_storage",
    
    # 'dj_celery_panel',
    'dj_redis_panel',
    'dj_control_room',
    
    'corsheaders',
    'rest_framework',
    
    'accounts',
    'ai',
    'integrations',
    'companies',
    'documents',
    'invitations',

    # for all-auth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'rest_framework.authtoken',
]

SITE_ID = 1

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',   # to be add for cors-headers
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',  # to be add for OAuth config
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

# for production using neon psql serverless db
DATABASES={
    "default": dj_database_url.parse(os.environ["DATABASE_URL"],
                                     conn_max_age=600,
                                      ssl_require=True),
}

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLODINARY_SECRECT_KEY"),
)

DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# for development---
# DATABASES={
#     'default':{
#          'ENGINE': 'django.db.backends.sqlite3',
#          'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

REST_FRAMEWORK ={
    "DEFAULT_AUTHENTICATION_CLASSES":(
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES":[
        "rest_framework.permissions.IsAuthenticated",
    ]
}

SIMPLE_JWT={
    "ACCESS_TOKEN_LIFETIME":timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME':timedelta(days=2),
}
CORS_ALLOWED_ORIGINS = [
    'https://rag-backend-pcij.onrender.com',
    "http://localhost:5173",  # your React app
]

CSRF_TRUSTED_ORIGINS = [
    'https://rag-backend-pcij.onrender.com',
    "http://localhost:5173",
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True



CORS_ALLOW_CREDENTIALS = True 

AUTHENTICATION_BACKENDS=(
    "django.contrib.auth.backends.ModelBackend",   # neeed to add for normal authetication
    "allauth.account.auth_backends.AuthenticationBackend",   # need to add for allauth(google or github and all )
)


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'
MEDIA_ROOT = "media/"


LOGIN_REDIRECT_URL = '/callback/'

SOCIALACCOUNT_PROVIDERS={
    
    'google':{
        'SCOPE':['email','profile'],
        'AUTH_PARAMS':{'access_type':'offline',  # offline for refresh token
                       'prompt':'consent'},   # very important for again refresh token
        'OAUTH_PKCE_ENABLED':True,
        'FETCH_USERINFO':True,
        
    }
}






ACCOUNT_LOGIN_METHODS = {"email"}

ACCOUNT_SIGNUP_FIELDS = [
    "email*",
    "password1*",
    "password2*"
]
ACCOUNT_USER_MODEL_USERNAME_FIELD = None

SOCIALACCOUNT_STORE_TOKENS=True
SOCIALACCOUNT_LOGIN_ON_GET = True  # to skip the confirmation page wich has only html