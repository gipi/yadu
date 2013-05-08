DATABASES = {
    'default': {
        'NAME': '/tmp/shorturls.db',
        'ENGINE': 'django.db.backends.sqlite3',
    },
}
INSTALLED_APPS = ['yadu',]
ROOT_URLCONF = 'yadu.tests.urls'

USE_XSENDFILE = True
