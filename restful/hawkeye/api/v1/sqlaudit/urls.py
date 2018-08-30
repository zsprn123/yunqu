# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/sqlaudit/urls.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 1097 bytes
from django.conf.urls import url, include
from rest_framework import routers
from api.v1.sqlaudit import views
from api.v1.sqlaudit.model_views import Audit_StrategyViewSet, Audit_RuleViewSet, Audit_JobViewSet, Optimization_JobViewSet, Audit_SQL_ResultViewSet, Audit_SchemaViewSet, SQL_Perf_Diff_ViewSet
from django.urls import path
router = routers.DefaultRouter()
router.register('audit-strategy', Audit_StrategyViewSet)
router.register('audit-rule', Audit_RuleViewSet)
router.register('audit-job', Audit_JobViewSet)
router.register('optimization-job', Optimization_JobViewSet)
router.register('audit-sql-result', Audit_SQL_ResultViewSet)
router.register('audit-schema', Audit_SchemaViewSet)
router.register('sql-perf', SQL_Perf_Diff_ViewSet)
urlpatterns = [
 path('', include(router.urls)),
 path('analysis/', views.analysis_from_post),
 path('get_schema_list/', views.get_schema_list),
 path('sql-format/', views.sql_format),
 path('index/', views.index),
 path('audit-compare-index/', views.audit_compare_index),
 path('audit_compare/', views.audit_compare)]
# okay decompiling ./restful/hawkeye/api/v1/sqlaudit/urls.pyc
