# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/misc/urls.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 290 bytes
from django.conf.urls import url, include
from rest_framework_bulk.routes import BulkRouter
from .views import ContentTypeViewSet
from django.urls import path
router = BulkRouter()
router.register('contenttypes', ContentTypeViewSet)
urlpatterns = (
 path('', include(router.urls)),)
# okay decompiling ./restful/hawkeye/api/v1/misc/urls.pyc
