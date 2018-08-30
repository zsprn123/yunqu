# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/urls.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 645 bytes
from django.conf.urls import url, include
from .auth import urls as auth_urls
from .misc import urls as misc_urls
from .monitor import urls as monitor_urls
from .alarm import urls as alarm_urls
from .sqlaudit import urls as sqlaudit
from django.urls import path
urlpatterns = [
 path('auth/', include('api.v1.auth.urls')),
 path('misc/', include('api.v1.misc.urls')),
 path('monitor/', include('api.v1.monitor.urls')),
 path('alarm/', include('api.v1.alarm.urls')),
 path('sqlaudit/', include('api.v1.sqlaudit.urls')),
 path('heathcheck/', include('api.v1.heathcheck.urls')),
 path('hosts/', include('api.v1.hosts.urls'))]
# okay decompiling ./restful/hawkeye/api/v1/urls.pyc
