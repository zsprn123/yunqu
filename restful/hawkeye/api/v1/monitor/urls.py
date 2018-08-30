# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/monitor/urls.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 897 bytes
from django.conf.urls import url, include
from rest_framework import routers
from api.v1.monitor.views import model_view, database, ash_view, index_view
from rest_framework_bulk.routes import BulkRouter
from django.urls import path
router = routers.DefaultRouter()
router.register('database', model_view.DatabaseViewSet)
router.register('ash/db2', ash_view.DB2_ASH_ViewSet)
router.register('ash/oracle', ash_view.Oracle_ASH_ViewSet)
router.register('ash/mysql', ash_view.MySQL_ASH_ViewSet)
router.register('ash/sqlserver', ash_view.MSSQL_ASH_ViewSet)
router.register('ash/postgres', ash_view.Postgres_ASH_ViewSet)
urlpatterns = [
 path('', include(router.urls)),
 path('testconn/', database.testconn),
 path('execsql/', database.execsql),
 path('translate/', database.translate),
 path('index/', index_view.index),
 path('index-performance/', index_view.index_performance)]
# okay decompiling ./restful/hawkeye/api/v1/monitor/urls.pyc
