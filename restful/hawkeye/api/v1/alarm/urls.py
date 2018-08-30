# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/alarm/urls.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 1128 bytes
from django.conf.urls import url, include
from rest_framework_bulk.routes import BulkRouter
from api.v1.alarm import views
from .views import WarnConfigViewSet, PeriodicTaskViewSet, IntervalScheduleViewSet, ReceiverViewSet, Warn_ResultViewSet, Warn_Config_TemplateViewSet, Mail_ConfigViewSet
from django.urls import path
router = BulkRouter()
router.register('warnconfig', WarnConfigViewSet)
router.register('warn-config-template', Warn_Config_TemplateViewSet)
router.register('warn-result', Warn_ResultViewSet)
router.register('warn-receiver', ReceiverViewSet)
router.register('mail-config', Mail_ConfigViewSet)
router.register('celerytask', PeriodicTaskViewSet)
router.register('interval', IntervalScheduleViewSet)
urlpatterns = (
 path('', include(router.urls)),
 path('get-mail-config/', views.get_mail_config),
 path('test-mail-connection/', views.test_mail_connection),
 path('get-celery-tasks/', views.get_celery_tasks),
 path('reset-warn-config/', views.reset_warn_config),
 path('get-space-table-name/', views.get_space_table_name),
 path('handle-prom-alert/', views.handle_prom_alert))
# okay decompiling ./restful/hawkeye/api/v1/alarm/urls.pyc
