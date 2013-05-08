from urlparse import urlparse
from django.conf import settings
from django.views.static import serve
from django.http import HttpResponse, HttpResponseRedirect

import posixpath
import urllib
import os
import logging


logger = logging.getLogger(__name__)


USE_XSENDFILE = getattr(settings, 'USE_XSENDFILE', False)

XSENDFILE_HEADER = getattr(settings, 'XSENDFILE_HEADER', 'X-Sendfile')

def xsendfileserve(request, path, document_root=None, **kwargs):
    """
    Serve static files using X-Sendfile below a given point 
    in the directory structure.

    This is a thin wrapper around Django's built-in django.views.static,
    which optionally uses ``USE_XSENDFILE`` to tell webservers to send the
    file to the client. This can, for example, be used to enable Django's
    authentication for static files.

    To use, put a URL pattern such as::

        (r'^(?P<path>.*)$', login_required(xsendfileserve), 
                            {'document_root' : '/path/to/my/files/'})

    in your URLconf. You must provide the ``document_root`` param. You may
    also set ``show_indexes`` to ``True`` if you'd like to serve a basic index
    of the directory.  This index view will use the template hardcoded below,
    but if you'd like to override it, you can create a template called
    ``static/directory_index.html``.

    It's possible to indicate the custom header name for the web server by
    the settings' variable ``XSENDFILE_HEADER`` that has as default the Apache2's
    header name, for the Nginx server you should use ``X-Accel-Redirect`` instead.

    It's also available a logger (with name ``yadu.util``) to use in order to
    have control on this kind of requests; it's possible to configure Django
    to save this log in a file like::

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

    Original code from <http://djangosnippets.org/snippets/2226/>
    """

    if USE_XSENDFILE:
        # This code comes straight from the static file serve
        # code in Django 1.2.

        # Clean up given path to only allow serving files below document_root.
        path = posixpath.normpath(urllib.unquote(path))
        path = path.lstrip('/')
        newpath = ''
        for part in path.split('/'):
            if not part:
                # Strip empty path components.
                continue
            drive, part = os.path.splitdrive(part)
            head, part = os.path.split(part)
            if part in (os.curdir, os.pardir):
                # Strip '.' and '..' in path.
                continue
            newpath = os.path.join(newpath, part).replace('\\', '/')
        if newpath and path != newpath:
            return HttpResponseRedirect(newpath)
        fullpath = os.path.join(document_root, newpath)

        logger.info('request path %s -> %s' % (path, fullpath))

        if os.path.isdir(fullpath):
            # if we are asked for a directory pass to django
            # since mod_xsendfile doesn't allow directory listing
            return serve(request, path, document_root, **kwargs)

        # This is where the magic takes place.
        response = HttpResponse()
        response[XSENDFILE_HEADER] = fullpath
        # Unset the Content-Type as to allow for the webserver
        # to determine it.
        response['Content-Type'] = ''

        return response

    return serve(request, path, document_root, **kwargs)

def ssl_required(view_func):
    """
    Enforce the use of https:// protocol for the views/urls with which
    you choose to decorate.

    For example to make mandatory that the login view **must** be served with
    SSL enabled you have to use as follow the decorator::

        url(r'^login/$',ssl_required(login), name='login'),

    As security measure you can set to True the SESSION_COOKIE_SECURE and CSRF_COOKIE_SECURE
    so that cookies are not leaked. Another setting that you would like to configure correctly
    is the SECURE_PROXY_SSL_HEADER.
    
    Obviously you have to configure the webserver of your choice
    correctly.

    Original code from <http://djangosnippets.org/snippets/1351/>
    """
    def _checkssl(request, *args, **kwargs):
        if not request.is_secure():
            if hasattr(settings, 'SSL_DOMAIN'):
                url_str = urlparse.urljoin(
                    settings.SSL_DOMAIN,
                    request.get_full_path()
                )
            else:
                url_str = request.build_absolute_uri()
            url_str = url_str.replace('http://', 'https://')
            return HttpResponseRedirect(url_str)

        return view_func(request, *args, **kwargs)
    return _checkssl
