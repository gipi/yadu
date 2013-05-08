from django.conf.urls.defaults import patterns, url, include
from django.contrib.auth.decorators import login_required
from yadu.utils import xsendfileserve, ssl_required
from django.contrib.auth.views import login

import os


from django.contrib import admin
admin.autodiscover()

ROOT = os.path.abspath(os.path.dirname(__file__))

urlpatterns = patterns('',
    url(r'^without_login/(?P<path>.*)$', xsendfileserve,
                    {'document_root' : ROOT}, name='wo_login'),
    url(r'^with_login/(?P<path>.*)$', login_required(xsendfileserve),
                    {'document_root' : ROOT}, name='w_login'),
    url(r'^login/$',ssl_required(login), name='login'),
    (r'^admin/', include(admin.site.urls)),
)
