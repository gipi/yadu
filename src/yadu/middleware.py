# encoding: utf-8
from django.contrib.auth.models import User

import logging


logger = logging.getLogger(__name__)

class Debug(object):
    '''
    Add some debugging functions to a running site.

    In order to make this work add this middleware to the ``MIDDLEWARE_CLASSES`` and
    in the ``URL`` of the request add the parameter ``dev`` making a request with a user
    that is staff.

    The extra functions available are:

     * the ``request`` has the attribute ``dev`` available
     * if a ``username`` GET parameter is present, its value is used as username of the user making the request
    '''
    def process_request(self, request):
        if request.GET.has_key('dev') and request.user.is_staff:
            logger.info('ACTIVATING DEV MODE for user %s' % request.user)
            request.dev = True
            if request.GET.has_key('username'):
                request.user = User.objects.get(username=request.GET['username'])