# http://www.travisswicegood.com/2010/01/17/django-virtualenv-pip-and-fabric/
from django.conf import settings
from django.core.management import call_command

import os, sys

# add yadu module to the syspath in order to make available for testing
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, ROOT_DIR)

def main():
    # Dynamically configure the Django settings with the minimum necessary to
    # get Django running tests
    settings.configure(
        INSTALLED_APPS=(
            'yadu',
        ),
        # Django replaces this, but it still wants it. *shrugs*
        DATABASES = {
            'default': {
                "ENGINE": 'django.db.backends.sqlite3',
            }
        },
        ROOT_URLCONF='yadu.tests.urls',
        USE_XSENDFILE=True
    )

    # Fire off the tests
    call_command('test', 'yadu')

if __name__ == '__main__':
    main()
