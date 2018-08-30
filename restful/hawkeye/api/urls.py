# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/urls.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 214 bytes
from django.conf.urls import url, include
from .v1 import urls as v1_urls
from django.urls import path
urlpatterns = [
 path('', include(v1_urls)),
 path('v1/', include(v1_urls))]
# okay decompiling ./restful/hawkeye/api/urls.pyc
