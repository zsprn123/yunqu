# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/monitor/views/model_view.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 32034 bytes
import json, time
from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_bulk import BulkCreateModelMixin, BulkModelViewSet
from api.enum.database_enum import Driver
from api.v1.monitor.filtersets import DatabaseFilterSet, PerformanceFilterSet
from api.v1.monitor.serializers import DatabaseSerializer, PerformanceSerializer
from api.v1.monitor.services.activityService import get_database_activity, get_activity_dimension, get_ash_chain, get_activity_tuning_report
from api.v1.monitor.services.copyashService import copyash
from api.v1.monitor.services.performance.performanceService import PERFORMANCE_FUNCTION
from api.v1.monitor.services.sessionService import session_detail, session_history, all_sessions
from api.v1.monitor.services.lockService import get_lock_session, get_lock_trend
from api.v1.monitor.services.topsqlService import get_topsql
from api.v1.monitor.services.sqldetailService import get_sql_detail
from api.v1.monitor.services.sqltuneService import get_sqlmon_report, execute_sqltuning_task, get_sql_audit, accept_sql_profile, apply_sql_profile
from api.v1.monitor.services.createdbService import createdb
from common.aes import aes_decode
from common.filters import DjangoModelObjectPermissionsFilter, RelatedOrderingFilter
from common.util import get_java_response
from common.yunquAuthorizationUtil import current_target_available
from monitor.models import Database, Performance, type2jdbcurl
from api.v1.monitor.services.summaryService import get_summary
from api.v1.monitor.services.sqlmonService import get_sqlmon_list
from api.v1.monitor.services.reportService import get_snapshot, get_awr_report, get_ash_report, create_snapshot
from api.v1.monitor.services.spaceService import space_info, detail_info
from api.v1.monitor.services.schemaService import refresh_schema, get_schema, object_detail, schema_table_rows, overall_table_rows
from api.celery.db2.summary import get_dbsummary
from api.v1.monitor.services.sqldetail.common import get_sql_text
from api.v1.monitor.services.backupService import get_backup
from django.core.cache import cache

class DatabaseViewSet(BulkModelViewSet):
    queryset = Database.objects.all()
    serializer_class = DatabaseSerializer
    filter_class = DatabaseFilterSet
    filter_backends = (
     DjangoFilterBackend,
     DjangoModelObjectPermissionsFilter,
     RelatedOrderingFilter)

    def create(self, request, *args, **kwargs):
        if not request.user:
            return Response({'detail': 'Error decoding signature.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            request.data['owner'] = request.user.id
            createdb(request)
            license_checked = current_target_available()
            instance_count = int(request.data.get('instance_count', '1'))
            if license_checked is False:
                return Response({'error_message': '!'}, status=status.HTTP_400_BAD_REQUEST)
            if license_checked is not True:
                if license_checked - instance_count < 0:
                    return Response({'error_message': ('{},{},!').format(license_checked, instance_count)},
                      status=status.HTTP_400_BAD_REQUEST)
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                if request.data.get('db_type') == 'oracle':
                    request.data['id'] = serializer.data['id']
                    copyash.delay(request.data)
                if request.data.get('db_type') == 'db2':
                    get_dbsummary.delay(serializer.data['id'])
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.is_switch_off:
            return Response({'error_message': ' '}, status=status.HTTP_400_BAD_REQUEST)
        else:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        original_is_switch_off = instance.is_switch_off
        current_is_switch_off = serializer.context.get('request').data.get('is_switch_off')
        if original_is_switch_off == True:
            if current_is_switch_off == False:
                instance_count = instance.instance_count or 1
                license_checked = current_target_available()
        if license_checked is False:
            return Response({'error_message': '!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if license_checked is not True:
                if license_checked - instance_count < 0:
                    return Response({'error_message': ('{},{},!').format(license_checked, instance_count)},
                      status=status.HTTP_400_BAD_REQUEST)
                if current_is_switch_off == True and original_is_switch_off == False:
                    url = type2jdbcurl(instance.db_type, instance.hostname, instance.port, db_name=instance.db_name)
                    jsonobj = {'user':instance.username, 
                     'password':aes_decode(instance.password), 
                     'jdbc_url':url, 
                     'driver':Driver[instance.db_type].value}
                    get_java_response('close-conn/', jsonobj)
                self.perform_update(serializer)
                if getattr(instance, '_prefetched_objects_cache', None):
                    instance._prefetched_objects_cache = {}
            return Response(serializer.data)

    @detail_route(methods=[
     'post'],
      url_path='performance')
    def get_performance(self, request, pk=None):
        try:
            database = Database.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return {'error_message': ''}

        instance_id = request.data.get('instance_id', None)
        begin_time = request.data.get('begin_time', None)
        end_time = request.data.get('end_time', None)
        time_span = request.data.get('time_span', None)
        if time_span != 'realtime':
            pass
        if not begin_time or not end_time:
            return Response({'error_message': 'begin_time and end_time is required'}, status=status.HTTP_400_BAD_REQUEST)
        performance_func = PERFORMANCE_FUNCTION.get(database.db_type)
        performance = performance_func(database)
        result = performance.get_history_data_by_range(begin_time, end_time, instance_id=instance_id)
        if 'error_message' in result:
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(result, status=status.HTTP_200_OK)

    @detail_route(methods=[
     'get'],
      url_path='cache')
    def refresh_cache(self, request, pk=None):
        database = self.get_object()
        performance_func = PERFORMANCE_FUNCTION.get(database.db_type)
        performance = performance_func(database)
        now_time = round(time.time())
        if cache.get('performance-data' + str(database.id) + str(database.instance_id_list) + 'day', None):
            result = performance.get_history_data_by_range(now_time - 86400, now_time, instance_id=None)
            cache.set('performance-data' + str(database.id) + str(database.instance_id_list) + 'day', result, timeout=3600)
        if cache.get('performance-data' + str(database.id) + str(database.instance_id_list) + 'week', None):
            result = performance.get_history_data_by_range(now_time - 604800, now_time, instance_id=None)
            cache.set('performance-data' + str(database.id) + str(database.instance_id_list) + 'week', result, timeout=86400)
        if cache.get('performance-data' + str(database.id) + str(database.instance_id_list) + 'month', None):
            result = performance.get_history_data_by_range(now_time - 2592000, now_time, instance_id=None)
            cache.set('performance-data' + str(database.id) + str(database.instance_id_list) + 'month', result, timeout=86400)
        if cache.get('performance-data' + str(database.id) + str(database.instance_id_list) + '3month', None):
            result = performance.get_history_data_by_range(now_time - 7776000, now_time, instance_id=None)
            cache.set('performance-data' + str(database.id) + str(database.instance_id_list) + '3month', result, timeout=86400)
        return Response(status=status.HTTP_200_OK)

    @detail_route(methods=[
     'post'],
      url_path='activity')
    def get_database_activity(self, request, pk=None):
        instance_id = request.data.get('instance_id', None)
        begin_time = request.data.get('begin_time', None)
        end_time = request.data.get('end_time', None)
        time_span = request.data.get('time_span', None)
        sql_id = request.data.get('sql_id', None)
        session_id = request.data.get('session_id', None)
        if time_span != 'realtime':
            pass
        if not begin_time or not end_time:
            return Response({'error_message': 'begin_time and end_time is required'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            result = get_database_activity(pk, time_span=time_span, instance_id=instance_id, sql_id=sql_id, session_id=session_id,
              begin_time=begin_time,
              end_time=end_time)
            if 'error_message' in result:
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(result, status=status.HTTP_200_OK)

    @detail_route(methods=[
     'post'],
      url_path='lock')
    def get_database_lock(self, request, pk=None):
        time_span = request.data.get('time_span', None)
        if not time_span:
            return Response({'error_message': 'timespan is required'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            result = get_lock_session(pk, time_span=time_span)
            if 'error_message' in result:
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(result, status=status.HTTP_200_OK)

    @detail_route(methods=[
     'post'],
      url_path='lock-trend')
    def get_lock_trend(self, request, pk=None):
        begin_time = request.data.get('begin_time', None)
        end_time = request.data.get('end_time', None)
        if not begin_time or not end_time:
            return Response({'error_message': 'begin_time and end_time are required'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            result = get_lock_trend(pk, begin_time, end_time)
            if 'error_message' in result:
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(result, status=status.HTTP_200_OK)

    @detail_route(methods=[
     'post'],
      url_path='topsql')
    def get_database_topsql(self, request, pk=None):
        _type = request.data.get('type', None)
        user = request.data.get('user', None)
        sqltext = request.data.get('sql-text', None)
        result = get_topsql(pk, _type, user, sqltext)
        if 'error_message' in result:
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(result, status=status.HTTP_200_OK)

    @detail_route(methods=[
     'post'],
      url_path='sql-detail')
    def get_sql_detail(self, request, pk=None):
        sql_id = request.data.get('sql_id', None)
        instance_id = request.data.get('instance_id', None)
        begin_time = request.data.get('begin_time', None)
        end_time = request.data.get('end_time', None)
        time_span = request.data.get('time_span', None)
        cache = request.data.get('case', True)
        if not sql_id or not instance_id:
            return Response({'error_message': 'sql_id and instance_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if time_span != 'realtime':
                if not begin_time or not end_time:
                    return Response({'error_message': 'begin_time and end_time is required'}, status=status.HTTP_400_BAD_REQUEST)
                result = get_sql_detail(pk, sql_id, instance_id, time_span, begin_time, end_time, cache)
                if 'error_message' in result:
                    return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(result, status=status.HTTP_200_OK)

    @detail_route(methods=[
     'post'],
      url_path='sql-audit')
    def get_sql_audit(self, request, pk=None):
        sql_id = request.data.get('sql_id', None)
        begin_time = request.data.get('begin_time', None)
        end_time = request.data.get('end_time', None)
        time_span = request.data.get('time_span', None)
        if not sql_id:
            return Response({'error_message': 'sql_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if time_span != 'realtime':
                if not begin_time or not end_time:
                    return Response({'error_message': 'begin_time and end_time is required'}, status=status.HTTP_400_BAD_REQUEST)
                result = {}
                if sql_id != 'null':
                    result = get_sql_audit(pk, sql_id, time_span, begin_time, end_time)
                if 'error_message' in result:
                    return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(result, status=status.HTTP_200_OK)

    @detail_route(methods=[
     'post'],
      url_path='sqlmon-report')
    def get_sqlmon_report(self, request, pk=None):
        sql_id = request.data.get('sql_id', None)
        inst_id = request.data.get('instance_id', None)
        sql_exec_id = request.data.get('sql_exec_id', None)
        report_type = request.data.get('report_type', 'ACTIVE')
        time_span = request.data.get('time_span', None)
        if not sql_id or not inst_id:
            return Response({'error_message': 'sql_id and inst_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            result = get_sqlmon_report(pk, sql_id, inst_id, sql_exec_id, report_type, time_span)
            if 'error_message' in result:
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(result, status=status.HTTP_200_OK)

    @detail_route(methods=[
     'post'],
      url_path='getschema')
    def getschema(self, request, pk=None):
        database = self.get_object()
        result, jsonobj = refresh_schema(database)
        if not result:
            return Response(jsonobj, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'result': 'OK'}, status=status.HTTP_200_OK)

    @detail_route(methods=[
     'post'],
      url_path='sqltune-report')
    def get_sqltune_report(self, request, pk=None):
        sql_id = request.data.get('sql_id', None)
        timeout = request.data.get('timeout', 60)
        if not sql_id:
            return Response({'error_message': 'sql_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            result = execute_sqltuning_task(pk, sql_id, timeout)
            if 'error_message' in result:
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(result, status=status.HTTP_200_OK)

    @detail_route(methods=[
     'post'],
      url_path='accept-sql-profile')
    def accept_sql_profile(self, request, pk=None):
        action = request.data.get('action', None)
        if not action:
            return Response({'error_message': 'action is required'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            result = accept_sql_profile(pk, action)
            if 'error_message' in result:
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(result, status=status.HTTP_200_OK)

    @detail_route(methods=[
     'post'],
      url_path='apply-sql-profile')
    def apply_sql_profile(self, request, pk=None):
        sql_id = request.data.get('sql_id', None)
        plan_hash_value = request.data.get('plan_hash_value', None)
        if not sql_id or not plan_hash_value:
            return Response({'error_message': 'sql_id and plan_hash_value is required'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            result = apply_sql_profile(pk, sql_id, plan_hash_value)
            if 'error_message' in result:
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(result, status=status.HTTP_200_OK)

    @detail_route(methods=[
     'post'],
      url_path='activity-dimension')
    def get_activity_dimension(self, request, pk=None):
        instance_id = request.data.get('instance_id', None)
        begin_time = request.data.get('begin_time', None)
        end_time = request.data.get('end_time', None)
        dim = request.data.get('dim', None)
        sql_id = request.data.get('sql_id', None)
        session_id = request.data.get('session_id', None)
        if not begin_time or not end_time:
            return Response({'error_message': 'begin_time and end_time is required'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            result = get_activity_dimension(pk, instance_id=instance_id, sql_id=sql_id, session_id=session_id, begin_time=begin_time,
              end_time=end_time,
              dim=dim)
            if 'error_message' in result:
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(result, status=status.HTTP_200_OK)

    @detail_route(methods=[
     'post'],
      url_path='activity-tune')
    def get_activity_tune(self, request, pk=None):
        instance_id = request.data.get('instance_id', None)
        begin_time = request.data.get('begin_time', None)
        end_time = request.data.get('end_time', None)
        if not begin_time or not end_time:
            return Response({'error_message': 'begin_time and end_time is required'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            result = get_activity_tuning_report(pk, instance_id=instance_id, begin_time=begin_time,
              end_time=end_time)
            if 'error_message' in result:
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(result, status=status.HTTP_200_OK)

    @detail_route(methods=[
     'post'],
      url_path='session-detail')
    def get_session_detail(self, request, pk=None):
        session_id = request.data.get('session_id', None)
        time_span = request.data.get('time_span', 'realtime')
        if not session_id:
            return Response({'error_message': 'session_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            result = session_detail(pk, session_id, time_span)
            if 'error_message' in result:
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(result, status=status.HTTP_200_OK)

    @detail_route(methods=[
     'post'],
      url_path='session-history')
    def get_session_history(self, request, pk=None):
        session_id = request.data.get('session_id', None)
        begin_time = request.data.get('begin_time', None)
        end_time = request.data.get('end_time', None)
        if not begin_time or not end_time:
            return Response({'error_message': 'begin_time and end_time are required'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            result = session_history(pk, session_id, begin_time, end_time)
            if 'error_message' in result:
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(result, status=status.HTTP_200_OK)

    @detail_route(methods=[
     'post'],
      url_path='db-summary')
    def get_db_summary(self, request, pk=None):
        time_span = request.data.get('time_span', None)
        begin_time = request.data.get('begin_time', None)
        end_time = request.data.get('end_time', None)
        result = get_summary(pk, time_span, begin_time, end_time)
        if 'error_message' in result:
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(result, status=status.HTTP_200_OK)

    @detail_route(methods=[
     'post'],
      url_path='sqlmon-list')
    def get_sqlmon_list(self, request, pk=None):
        begin_time = request.data.get('begin_time', None)
        end_time = request.data.get('end_time', None)
        time_span = request.data.get('time_span', None)
        if time_span != 'realtime':
            pass
        if not begin_time or not end_time:
            return Response({'error_message': 'begin_time and end_time are required'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            result = get_sqlmon_list(pk, time_span=time_span, begin_time=begin_time, end_time=end_time)
            if isinstance(result, dict):
                if 'error_message' in result:
                    return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(result, status=status.HTTP_200_OK)

    @detail_route(methods=[
     'post'],
      url_path='snapshot')
    def get_snapshot(self, request, pk=None):
        limit = request.data.get('limit', 1000)
        result = get_snapshot(pk, limit)
        if isinstance(result, dict):
            if 'error_message' in result:
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(result, status=status.HTTP_200_OK)

    @detail_route(methods=[
     'post'],
      url_path='create-snapshot')
    def create_snapshot(self, request, pk=None):
        result = create_snapshot(pk)
        if isinstance(result, dict):
            if 'error_message' in result:
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(result, status=status.HTTP_200_OK)

    @detail_route(methods=[
     'post'],
      url_path='awr')
    def get_awr_report(self, request, pk=None):
        instance_id = request.data.get('instance_id', None)
        begin_id = request.data.get('begin_id', None)
        end_id = request.data.get('end_id', None)
        if not begin_id or not end_id:
            return Response({'error_message': 'begin_id and end_id are required'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            result = get_awr_report(pk, instance_id, begin_id, end_id)
            if 'error_message' in result:
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(result, status=status.HTTP_200_OK)

    @detail_route(methods=[
     'post'],
      url_path='ash')
    def get_ash_report(self, request, pk=None):
        instance_id = request.data.get('instance_id', None)
        begin_time = request.data.get('begin_time', None)
        end_time = request.data.get('end_time', None)
        if not begin_time or not end_time:
            return Response({'error_message': 'begin_id and end_id are required'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            result = get_ash_report(pk, instance_id, begin_time, end_time)
            if 'error_message' in result:
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(result, status=status.HTTP_200_OK)

    @detail_route(methods=[
     'post'],
      url_path='space')
    def get_space_info(self, request, pk=None):
        days = request.data.get('days', 7)
        result = space_info(pk, days)
        if isinstance(result, dict):
            if 'error_message' in result:
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(result, status=status.HTTP_200_OK)

    @detail_route(methods=[
     'post'],
      url_path='space-detail')
    def get_space_detail_info(self, request, pk=None):
        days = request.data.get('days', 7)
        name = request.data.get('name', None)
        if not name:
            return Response({'error_message': 'name is required'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            result = detail_info(pk, name, days)
            if isinstance(result, dict):
                if 'error_message' in result:
                    return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(result, status=status.HTTP_200_OK)

    @detail_route(methods=[
     'post'],
      url_path='ash-chain')
    def get_ash_chain(self, request, pk=None):
        instance_id = request.data.get('instance_id', None)
        begin_time = request.data.get('begin_time', None)
        end_time = request.data.get('end_time', None)
        if not begin_time or not end_time:
            return Response({'error_message': 'both begin_time and end_time are required'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            result = get_ash_chain(pk, instance_id, begin_time, end_time)
            if isinstance(result, dict):
                if 'error_message' in result:
                    return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(result, status=status.HTTP_200_OK)

    @detail_route(methods=[
     'post'],
      url_path='backup')
    def get_backup_info(self, request, pk=None):
        result = get_backup(pk)
        if isinstance(result, dict):
            if 'error_message' in result:
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(result, status=status.HTTP_200_OK)

    @detail_route(methods=[
     'post'],
      url_path='refresh-schema')
    def refresh_schema(self, request, pk=None):
        result = refresh_schema(pk)
        if isinstance(result, dict):
            if 'error_message' in result:
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(result, status=status.HTTP_200_OK)

    @detail_route(methods=[
     'post'],
      url_path='schema')
    def get_schema(self, request, pk=None):
        result = get_schema(pk)
        if isinstance(result, dict):
            if 'error_message' in result:
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(result, status=status.HTTP_200_OK)

    @detail_route(methods=[
     'post'],
      url_path='object-detail')
    def object_detail(self, request, pk=None):
        owner = request.data.get('schema', 7)
        object_name = request.data.get('object_name', None)
        object_type = request.data.get('object_type', None)
        subobject_name = request.data.get('subobject_name', None)
        if not owner or not object_name:
            return Response({'error_message': 'both owner and object_name are required'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            result = object_detail(pk, owner, object_name=object_name, object_type=object_type, subobject_name=subobject_name,
              cache=True)
            if isinstance(result, dict):
                if 'error_message' in result:
                    return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(result, status=status.HTTP_200_OK)

    @detail_route(methods=[
     'post'],
      url_path='sql-text')
    def sql_text(self, request, pk=None):
        import sqlparse
        sql_id = request.data.get('sql_id', None)
        if not sql_id:
            return Response({'error_message': 'sql_id are required'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            database = Database.objects.get(pk=pk)
            sql_text, schema = get_sql_text(database, sql_id)
            sql_text = (sqlparse.format(sql_text, reindent=True)) if sql_text else ''
            return Response({'sql_text': sql_text}, status=status.HTTP_200_OK)

    @detail_route(methods=[
     'post'],
      url_path='schema-rows')
    def schema_rows(self, request, pk=None):
        time_span = request.data.get('time_span', None)
        owner = request.data.get('owner', None)
        if not owner:
            return Response({'error_message': 'owner are required'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            result = schema_table_rows(pk, owner, time_span)
            if 'error_message' in result:
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(result, status=status.HTTP_200_OK)

    @detail_route(methods=[
     'post'],
      url_path='overall-rows')
    def overall(self, request, pk=None):
        time_span = request.data.get('time_span', None)
        result = overall_table_rows(pk, time_span)
        if 'error_message' in result:
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(result, status=status.HTTP_200_OK)

    @detail_route(methods=[
     'post'],
      url_path='all-sessions')
    def get_all_sessions(self, request, pk=None):
        result = all_sessions(pk)
        if 'error_message' in result:
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(result, status=status.HTTP_200_OK)

    @detail_route(methods=[
     'post'],
      url_path='test')
    def test(self, request, pk=None):
        from api.v1.monitor.services.createdbService import init_all
        init_all()
        return Response({}, status=status.HTTP_200_OK)


class PerformanceViewSet(ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
    filter_class = PerformanceFilterSet
# okay decompiling ./restful/hawkeye/api/v1/monitor/views/model_view.pyc
