Serving static files
--------------------

There is situation where is not possible to serve static files without
a previous management by your Django web application, think for example
to the case where you want enforce authentication before an user can
obtain the resource.

In order to accomplish this we have created the follow function using
the XSendfile module available for the principal web server out there
like `Apache <https://tn123.org/mod_xsendfile/>`_ or `Nginx <http://wiki.nginx.org/XSendfile>`_.

.. autofunction:: yadu.utils.xsendfileserve

For security reason we have to check that the web server strips client
provided headers so to avoid bypass of application permission management.
