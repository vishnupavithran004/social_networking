from decouple import config

DATABASE_CONFIG = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DATABASES_NAME'),
        'USER': config('DATABASES_USER'),
        'PASSWORD': config('DATABASES_PASSWORD'),
        'HOST': config('DATABASES_HOST'),
        'PORT': config('DATABASES_PORT'),
    }
}