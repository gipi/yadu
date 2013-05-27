from urlparse import urlparse
from django.conf import settings
from django.views.static import serve
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template
from django.utils.encoding import smart_str

import posixpath
import urllib
import os
import logging
import StringIO
import zipfile
from django.template.base import Context


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

def render_to_ods_response(ods_path, dictionary=None, context_instance=None, attachment_filename=None):
    """Return an HTTP response with an ODS document rendered using
    the passed context.

    The path of the document used to renderize must be relative to the directory
    where this is called.

    In order to modify the ODS you can unzip it

     $ unzip -l template.ods
     Archive:  template.ods
       Length      Date    Time    Name
     ---------  ---------- -----   ----
           46  2013-05-27 08:40   mimetype
         6587  2013-05-27 08:40   Thumbnails/thumbnail.png
         8329  2013-05-27 08:40   settings.xml
       289946  2013-05-27 08:40   content.xml
        93475  2013-05-27 08:40   styles.xml
         1026  2013-05-27 08:40   meta.xml
            0  2013-05-27 08:40   Configurations2/floater/
            0  2013-05-27 08:40   Configurations2/accelerator/current.xml
            0  2013-05-27 08:40   Configurations2/menubar/
            0  2013-05-27 08:40   Configurations2/popupmenu/
            0  2013-05-27 08:40   Configurations2/images/Bitmaps/
            0  2013-05-27 08:40   Configurations2/progressbar/
            0  2013-05-27 08:40   Configurations2/toolbar/
            0  2013-05-27 08:40   Configurations2/toolpanel/
            0  2013-05-27 08:40   Configurations2/statusbar/
          993  2013-05-27 08:40   META-INF/manifest.xml
    ---------                     -------
       400402                     16 files
    """
    # http://djangosnippets.org/snippets/15/
    ods_abspath = os.path.abspath(os.path.join(os.path.dirname(__file__), ods_path))
    # default mimetype
    mimetype = 'application/vnd.oasis.opendocument.text'

    # ODF is just a zipfile
    _input = zipfile.ZipFile(ods_abspath, "r" )

    # we cannot write directly to HttpResponse, so use StringIO
    text = StringIO.StringIO()

    context = Context(dictionary)
    if context_instance:
        context = context_instance.update(dictionary)

    # output document
    output = zipfile.ZipFile(text, "a")
    # go through the files in source
    for zi in _input.filelist:
        out = _input.read(zi.filename)
        # wait for the only interesting file
        if zi.filename == 'content.xml':
            # un-escape the quotes (in filters etc.)
            t = Template(out) 
            # render the document
            out = t.render(context) 
        elif zi.filename == 'mimetype':
            # mimetype is stored within the ODF
            mimetype = out 
        output.writestr(zi.filename, smart_str(out))

    # close and finish
    output.close()
    response = HttpResponse(content=text.getvalue(), mimetype=mimetype)

    response['Content-Disposition'] = 'attachment; filename=%s' % (attachment_filename if attachment_filename else 'download.ods')

    return response
