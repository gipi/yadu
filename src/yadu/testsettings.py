DATABASES = {
    'default': {
        'NAME': '/tmp/shorturls.db',
        'ENGINE': 'django.db.backends.sqlite3',
    },
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'yadu',
    'customer',
]

ROOT_URLCONF = 'yadu.tests.urls'

USE_XSENDFILE = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level':'DEBUG',
            'class':'logging.StreamHandler',
        },
        "xsendfile_log_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "filename": "info.log",
            "maxBytes": "10485760",
            "backupCount": "20",
            "encoding": "utf8"
        },
    },
    'loggers': {
        'yadu.utils': {
            'handlers': [
                'console',
                'xsendfile_log_file_handler',
            ],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
