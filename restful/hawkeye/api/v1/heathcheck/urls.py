# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/heathcheck/urls.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 572 bytes
from django.conf.urls import url, include
from rest_framework_bulk.routes import BulkRouter
from django.urls import path
from api.v1.heathcheck import views
from api.v1.heathcheck.views import Heathcheck_ReportViewSet
router = BulkRouter()
router.register('heathcheck-report', Heathcheck_ReportViewSet)
urlpatterns = (
 path('', include(router.urls)),
 path('gen-report/', views.gen_report),
 path('report-filter/', views.get_report_filter),
 path('save-filter/', views.save_filter),
 path('merge-healthcheck-report/', views.merge_healthcheck_report))
# okay decompiling ./restful/hawkeye/api/v1/heathcheck/urls.pyc
