# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/monitor/services/reportService.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 3942 bytes
from api.v1.monitor.services.runsqlService import run_sql, run_batch_sql, run_plsql
from api.enum.report_enum import Snapshot_Query, DBID_Query, AWR_Query, ASH_Query, get_key_inst_str, Max_Snapshot_Query
from monitor.models import Database
from common.util import build_exception_from_java
from django.core.exceptions import ObjectDoesNotExist
from common.util import timestamp_to_char

def get_snapshot(pk, snapshot_limit=1000):
    try:
        database = Database.objects.get(pk=pk)
        json_data = []
        query = Snapshot_Query.format(snapshot_limit)
        flag, json_data = run_sql(database, query)
        if not flag:
            raise build_exception_from_java(json_data)
        return json_data
    except ObjectDoesNotExist:
        return {'error_message': ''}
    except Exception as err:
        return {'error_message': str(err)}


def create_snapshot(pk):
    query = 'begin sys.dbms_workload_repository.create_snapshot; end;'
    try:
        database = Database.objects.get(pk=pk)
        json_data = []
        flag, json_data = run_plsql(database, query)
        if not flag:
            raise build_exception_from_java(json_data)
        flag, json_data = run_sql(database, Max_Snapshot_Query)
        if not flag:
            raise build_exception_from_java(json_data)
        if json_data:
            return json_data[0]
        return {}
    except ObjectDoesNotExist:
        return {'error_message': ''}
    except Exception as err:
        return {'error_message': str(err)}


def get_awr_report(pk, instance_id, begin_id, end_id):
    try:
        database = Database.objects.get(pk=pk)
        json_data = []
        flag, json_data = run_sql(database, DBID_Query)
        if not flag:
            raise build_exception_from_java(json_data)
        db_id = json_data[0].get('DBID')
        key, inst_str = get_key_inst_str(database, instance_id)
        query_awr = AWR_Query.get(key)
        options = {'db_id':db_id, 
         'inst_str':inst_str, 
         'begin_id':begin_id, 
         'end_id':end_id}
        query_awr['report'] = query_awr.get('report').format(**options)
        flag, report_data = run_batch_sql(database, query_awr)
        if not flag:
            raise build_exception_from_java(report_data)
        report_html = ('').join([x.get('OUTPUT') for x in report_data.get('report') if x.get('OUTPUT')]) if report_data.get('report') else ''
        return {'report_html': report_html}
    except ObjectDoesNotExist:
        return {'error_message': ''}
    except Exception as err:
        return {'error_message': str(err)}


def get_ash_report(pk, instance_id, begin_time, end_time):
    try:
        database = Database.objects.get(pk=pk)
        json_data = []
        flag, json_data = run_sql(database, DBID_Query)
        if not flag:
            raise build_exception_from_java(json_data)
        db_id = json_data[0].get('DBID')
        key, inst_str = get_key_inst_str(database, instance_id)
        query_ash = ASH_Query.get(key)
        options = {'db_id':db_id, 
         'inst_str':inst_str, 
         'begin_time':timestamp_to_char(begin_time), 
         'end_time':timestamp_to_char(end_time)}
        query_ash['report'] = query_ash.get('report').format(**options)
        flag, report_data = run_batch_sql(database, query_ash)
        if not flag:
            raise build_exception_from_java(report_data)
        report_html = ('').join([x.get('OUTPUT') for x in report_data.get('report') if x.get('OUTPUT')]) if report_data.get('report') else ''
        return {'report_html': report_html}
    except ObjectDoesNotExist:
        return {'error_message': ''}
    except Exception as err:
        return {'error_message': str(err)}
# okay decompiling ./restful/hawkeye/api/v1/monitor/services/reportService.pyc
