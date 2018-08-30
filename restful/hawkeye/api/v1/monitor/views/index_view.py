# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/monitor/views/index_view.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 10170 bytes
import datetime
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from alarm.models import Warn_Result
from api.v1.monitor.services.performance.performanceService import PERFORMANCE_FUNCTION
from api.v1.monitor.services.spaceService import space_info
from common.util import execute_return_json
from heathcheck.models import Heathcheck_Report
from monitor.models import Database

class DatabaseData:

    def __init__(self, db_type, data):
        self.db_type = db_type
        self.data = data


def num2pct(num):
    if not num:
        return 0
    else:
        if type(num) == str:
            num = float(num)
        return round(num, 3) * 100


@api_view(['GET'])
def index(request):
    database_count = Database.objects.all().count()
    oracle_count = (Database.objects.filter(db_type='oracle')).count()
    mysql_count = (Database.objects.filter(db_type='mysql')).count()
    db2_count = (Database.objects.filter(db_type='db2')).count()
    sqlserver_count = (Database.objects.filter(db_type='sqlserver')).count()
    warn_query_sum = Warn_Result.objects.count()
    warn_db2_count = (Warn_Result.objects.filter(database__db_type='db2')).count()
    warn_oracle_count = (Warn_Result.objects.filter(database__db_type='oracle')).count()
    warn_mysql_count = (Warn_Result.objects.filter(database__db_type='mysql')).count()
    warn_sqlserver_count = (Warn_Result.objects.filter(database__db_type='sqlserver')).count()
    warn_db2_pct = num2pct(warn_db2_count / warn_query_sum) if warn_query_sum != 0 else 0
    warn_oracle_pct = num2pct(warn_oracle_count / warn_query_sum) if warn_query_sum != 0 else 0
    warn_mysql_pct = num2pct(warn_mysql_count / warn_query_sum) if warn_query_sum != 0 else 0
    warn_sqlserver_pct = num2pct(warn_sqlserver_count / warn_query_sum) if warn_query_sum != 0 else 0
    all_health_report_score_list = list((((Heathcheck_Report.objects.exclude(report_detail__summary__score=None)).filter(status=1)).extra(select={'score': "report_detail#>'{summary,score}'"})).values_list('score', flat=True))
    healthcheck_report_danger_count = len([_score for _score in all_health_report_score_list if _score < 0.6])
    healthcheck_report_general_count = len([_score for _score in all_health_report_score_list if _score < 0.8])
    healthcheck_report_good_count = len([_score for _score in all_health_report_score_list if _score >= 0.8])
    query_result = execute_return_json('SELECT database_id FROM heathcheck_heathcheck_report GROUP BY database_id;')
    database_id_in_health_report = []
    healthcheck_score_list = []
    for _result in query_result:
        database_id_in_health_report.append(_result.get('database_id') or _result.get('DATABASE_ID'))

    for report_database_id in database_id_in_health_report[:5]:
        try:
            database = Database.objects.get(pk=report_database_id)
            score_list = (((Heathcheck_Report.objects.filter(database_id=report_database_id)).filter(status=1)).extra(select={'score': "report_detail#>'{summary,score}'"})).values_list('score', 'created_at')
            score_list = [[int(score1[1].timestamp() * 1000), type(score1[1]) == datetime.datetime and num2pct(score1[0]) if score1[1] else 0] for score1 in score_list]
            if score_list:
                healthcheck_score_list.append({'database_alias':database.alias, 
                 'data':score_list})
        except Exception as e:
            print(e)

    sql_audit_count_list = []
    sql_audit_query_result = execute_return_json('SELECT database_id,(SELECT alias From monitor_database WHERE id = database_id),AVG (total_score) FROM sqlaudit_audit_job WHERE status=3 GROUP BY database_id;')
    have_audit_database_id_list = [_data.get('database_id') or _data.get('DATABASE_ID') for _data in sql_audit_query_result]
    for _result in sql_audit_query_result:
        sql_audit_count_list.append({'database_alias':_result.get('alias') or _result.get('ALIAS'), 
         'avg':_result.get('avg') or _result.get('AVG')})

    for _database1 in Database.objects.exclude(id__in=have_audit_database_id_list):
        if len(sql_audit_count_list) < 5:
            sql_audit_count_list.append({'database_alias':_database1.alias, 
             'avg':0})

    now = datetime.datetime.now()
    d1 = now - (datetime.timedelta(hours=1))
    data1 = [
     DatabaseData('oracle', oracle_count).__dict__,
     DatabaseData('mysql', mysql_count).__dict__,
     DatabaseData('db2', db2_count).__dict__]
    data2 = [
     DatabaseData('oracle', warn_oracle_pct).__dict__,
     DatabaseData('mysql', warn_mysql_pct).__dict__,
     DatabaseData('db2', warn_db2_pct).__dict__,
     DatabaseData('sqlserver', warn_sqlserver_pct).__dict__]
    database_pct = []
    if oracle_count != 0:
        database_pct.append(DatabaseData('oracle', num2pct(oracle_count / database_count) if database_count != 0 else 0).__dict__)
    if mysql_count != 0:
        database_pct.append(DatabaseData('mysql', num2pct(mysql_count / database_count) if database_count != 0 else 0).__dict__)
    if db2_count != 0:
        database_pct.append(DatabaseData('db2', num2pct(db2_count / database_count) if database_count != 0 else 0).__dict__)
    if sqlserver_count != 0:
        database_pct.append(DatabaseData('sqlserver', num2pct(sqlserver_count / database_count) if database_count != 0 else 0).__dict__)
    data10 = {'health_check':{'score':num2pct(sum(all_health_report_score_list) / len(all_health_report_score_list)) if all_health_report_score_list else 0, 
      'level':[
       healthcheck_report_danger_count,
       healthcheck_report_general_count,
       healthcheck_report_good_count]}, 
     'warn':{'all_warn_count':warn_query_sum, 
      'recent_hour_warn_count':(Warn_Result.objects.filter(created_at__gt=d1)).count()}, 
     'database':{'able':{'able_pct': num2pct((Database.objects.filter(disabled=False)).count() / database_count) if database_count != 0 else 0}, 
      'pct':database_pct, 
      'host':{'Linux':0, 
       'AIX':0, 
       'Windows':0}}}
    data = {'1':data1, 
     '2':data2, 
     '3':healthcheck_score_list, 
     '8':sql_audit_count_list[:5], 
     '10':data10}
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def index_performance(request):
    now = round(datetime.datetime.now().timestamp())
    d1 = round((datetime.datetime.now() - (datetime.timedelta(hours=1))).timestamp())
    data4 = []
    data5 = []
    data6 = []
    data7 = []
    data9 = []
    database_list = Database.objects.filter((Q(db_type='oracle')) & (Q(disabled=False)) & (Q(is_switch_off=False)))[:5]
    for database in database_list:
        performance_func = PERFORMANCE_FUNCTION.get(database.db_type)
        performance = performance_func(database)
        result = performance.get_history_data_by_range(d1, now)
        for _result in result:
            if _result.get('name', '') == 'IO ':
                if 'PHYSICAL READ IO REQUESTS PER SEC' in _result['data'].keys():
                    io_request_list = _result['data']['PHYSICAL READ IO REQUESTS PER SEC']
                    print('io_request_list:' + str(len(io_request_list)))
                    data4.append({'database_alias':database.alias, 
                     'data':io_request_list})
            if _result.get('name', '') == '':
                if 'SESSION COUNT' in _result['data'].keys():
                    session_count_list = _result['data']['SESSION COUNT']
                    print('session_count_list:' + str(len(session_count_list)))
                    data5.append({'database_alias':database.alias, 
                     'data':session_count_list})
            if _result.get('name', '') == 'CPU (%)':
                cpu_data_list = []
                cpu_data = _result['data']
                if cpu_data:
                    cpu_data_list = cpu_data.popitem()[1]
                    print('cpu_data_list:' + str(len(cpu_data_list)))
                    data6.append({'database_alias':database.alias, 
                     'data':cpu_data_list})
            if _result.get('name', '') == 'IO ':
                if 'PHYSICAL READ TOTAL BYTES PER SEC' in _result['data'].keys():
                    io_bytes_list = _result['data']['PHYSICAL READ TOTAL BYTES PER SEC']
                    print('io_bytes_list:' + str(len(io_bytes_list)))
                    data7.append({'database_alias':database.alias, 
                     'data':io_bytes_list})

        space_result = space_info(database.id)
        if not (isinstance(space_result, dict) and 'error_message' in result):
            if 'total_trend' in space_result.keys():
                if 'data' in space_result['total_trend'].keys():
                    data9.append({'database_alias':database.alias, 
                     'data':space_result['total_trend']['data']})

    return Response({'4':data4, 
     '5':data5, 
     '6':data6, 
     '7':data7, 
     '9':data9},
      status=status.HTTP_200_OK)
# okay decompiling ./restful/hawkeye/api/v1/monitor/views/index_view.pyc
