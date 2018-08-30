# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/hosts/urls.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 494 bytes
from django.conf.urls import include
from rest_framework import routers
from django.urls import path
from api.v1.hosts.model_views import HostViewSet, HostDetailViewSet, host_test_connection, LogMatchKeyViewSet
router = routers.DefaultRouter()
router.register('host', HostViewSet)
router.register('host-detail', HostDetailViewSet)
router.register('log-match-key', LogMatchKeyViewSet)
urlpatterns = [
 path('', include(router.urls)),
 path('test-connection/', host_test_connection)]
# okay decompiling ./restful/hawkeye/api/v1/hosts/urls.pyc
