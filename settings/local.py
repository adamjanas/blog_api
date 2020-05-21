from settings.base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get("DB_NAME", "postgres"),
        'USER': os.environ.get("DB_USER", "postgres"),
        'PASSWORD': os.environ.get("DB_PASSWORD", "difficultpassword"),
        'HOST': os.environ.get("DB_HOST", "database"),
        'PORT': os.environ.get("DB_HOST", 5432),

    }
}