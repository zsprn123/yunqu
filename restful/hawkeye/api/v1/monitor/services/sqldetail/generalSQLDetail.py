# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/monitor/services/sqldetail/generalSQLDetail.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 11670 bytes
from datetime import datetime, timedelta
from api.v1.monitor.services.runsqlService import run_sql, run_batch_sql, get_sql_plan
from common.util import build_exception_from_java, get_10s_time_str
from monitor.models import Database, SQL_Detail
from api.v1.monitor.services.sqldetail.common import get_default_sql_detail_format
from api.v1.monitor.services.sqldetail.common import get_sql_text
from api.enum.sql_audit_enum import get_db2_sql_audit

def db2_gen_sql_detail(database, sql_id, sql_text=None, schema=None, get_detail=True):
    plan_data = []
    sql_detail = get_default_sql_detail_format(database.db_type)
    time_str = get_10s_time_str()
    plan_dic = {}
    audit_data = {}
    if sql_text:
        if schema:
            flag, json_data = get_sql_plan(database, sql_text, schema)
            if not flag:
                print(sql_text)
                print(str(build_exception_from_java(json_data)))
            else:
                plan_dic[time_str] = json_data
                if json_data:
                    audit_data = get_db2_sql_audit(database, sql_id, sql_text, json_data)
                    sql_detail['audit'] = audit_data
            if get_detail:
                query = f'''SELECT
                TOTAL_CPU_TIME/1000 TOTAL_CPU_TIME,
                LOCK_WAIT_TIME/1000 LOCK_WAIT_TIME,
                (LOG_BUFFER_WAIT_TIME + LOG_DISK_WAIT_TIME)/1000  LOG_WAIT_TIME,
                (FCM_RECV_WAIT_TIME + FCM_SEND_WAIT_TIME)/1000 NET_WAIT_TIME,
                (POOL_READ_TIME + POOL_WRITE_TIME + DIRECT_READ_TIME + DIRECT_WRITE_TIME)/1000 IO_WAIT_TIME,
                STMT_EXEC_TIME/1000 STMT_EXEC_TIME,
                NUM_EXEC_WITH_METRICS,
                TOTAL_ACT_TIME/1000 TOTAL_ACT_TIME,
                TOTAL_ACT_WAIT_TIME/1000 TOTAL_ACT_WAIT_TIME,
                (POOL_DATA_L_READS + POOL_TEMP_DATA_L_READS + POOL_XDA_L_READS +   POOL_TEMP_XDA_L_READS + POOL_INDEX_L_READS + POOL_TEMP_INDEX_L_READS) POOL_L_READS,
                (POOL_DATA_P_READS + POOL_TEMP_DATA_P_READS + POOL_XDA_P_READS +  POOL_TEMP_XDA_P_READS + POOL_INDEX_P_READS + POOL_TEMP_INDEX_P_READS) POOL_P_READS,
                (POOL_DATA_WRITES + POOL_XDA_WRITES + POOL_INDEX_WRITES) POOL_WRITES,
                DIRECT_READS,
                DIRECT_WRITES,
                ROWS_READ,
                ROWS_RETURNED,
                ROWS_MODIFIED,
                LOCK_WAITS,
                LOCK_ESCALS,
                TOTAL_SORTS,
                DEADLOCKS,
                LOCK_TIMEOUTS
            FROM
                TABLE (MON_GET_PKG_CACHE_STMT(null,
                null,
                null,
                -2))
            WHERE
                EXECUTABLE_ID = x'{sql_id}''''
                flag, json_data = run_sql(database, query)
                if not flag:
                    print(str(build_exception_from_java(json_data)))
                else:
                    if json_data:
                        metric_dict = {'TOTAL_CPU_TIME':'CPU()',  'LOCK_WAIT_TIME':'()', 
                         'LOG_WAIT_TIME':'()', 
                         'NET_WAIT_TIME':'()', 
                         'IO_WAIT_TIME':'IO()', 
                         'STMT_EXEC_TIME':'()', 
                         'NUM_EXEC_WITH_METRICS':'', 
                         'TOTAL_ACT_TIME':'()', 
                         'TOTAL_ACT_WAIT_TIME':'()', 
                         'POOL_L_READS':'', 
                         'POOL_P_READS':'', 
                         'POOL_WRITES':'', 
                         'DIRECT_READS':'', 
                         'DIRECT_WRITES':'', 
                         'ROWS_READ':'', 
                         'ROWS_RETURNED':'', 
                         'ROWS_MODIFIED':'', 
                         'LOCK_WAITS':'', 
                         'LOCK_ESCALS':'', 
                         'TOTAL_SORTS':'', 
                         'DEADLOCKS':'', 
                         'LOCK_TIMEOUTS':''}
                        for idx, x in enumerate(json_data):
                            pie_chart_data = {k:v for k, v in x.items() if k in ('TOTAL_CPU_TIME',
                                                                                 'LOCK_WAIT_TIME',
                                                                                 'LOG_WAIT_TIME',
                                                                                 'IO_WAIT_TIME')}
                            total_executions = x.get('NUM_EXEC_WITH_METRICS') if x.get('NUM_EXEC_WITH_METRICS') != 0 else 1
                            total_rows = x.get('NUM_EXEC_WITH_METRICS') if x.get('NUM_EXEC_WITH_METRICS') != 0 else 1
                            execution_data = [{u'\u6307\u6807':metric_dict.get(k),  u'\u603b\u6570':v,  u'\u5e73\u5747\u6bcf\u6b21\u6267\u884c':round(v / total_executions),  u'\u5e73\u5747\u6bcf\u884c\u8bb0\u5f55':round(v / total_rows)} for k, v in x.items() if k in metric_dict if v != None]
                            key = f'''{time_str}-{idx}'''
                            sql_detail['stats'][key] = {'child_summary':[
                              {'SAMPLE_TIME': time_str}], 
                             'pie_chart_data':pie_chart_data, 
                             'execution_stats':{'header':[
                               '', '', '', ''], 
                              'data':execution_data}}

                sql_detail['sql_text'] = sql_text
                sql_detail['plans']['data'] = plan_dic
                return sql_detail


def mysql_gen_sql_detail(database, sql_id, sql_text=None, schema=None, get_detail=True):
    sql_detail = get_default_sql_detail_format(database.db_type)
    time_str = get_10s_time_str()
    plan_dic = {}
    if sql_text:
        if schema:
            flag, json_data = get_sql_plan(database, sql_text, schema)
            if not flag:
                print(str(build_exception_from_java(json_data)))
                return sql_detail
            plan_dic[time_str] = json_data
    sql_detail['sql_text'] = sql_text
    sql_detail['plans']['data'] = plan_dic
    detail = SQL_Detail()
    detail.created_at = datetime.now().replace(microsecond=0)
    detail.sql_detail = sql_detail
    detail.sql_id = sql_id
    detail.database = database
    detail.save()
    return sql_detail


def sqlserver_gen_sql_detail(database, sql_id, sql_text=None, schema=None, get_detail=True):
    sql_detail = get_default_sql_detail_format(database.db_type)
    time_str = get_10s_time_str()
    plan_dic = {}
    query = {'detail':f'''
                select
            CONVERT(VARCHAR(24), creation_time, 120) CREATION_TIME,
            CONVERT(VARCHAR(24), last_execution_time, 120) LAST_EXECUTION_TIME,
            EXECUTION_COUNT,
            convert(bigint, total_elapsed_time/1000) TOTAL_ELAPSED_TIME,
            convert(bigint, total_worker_time/1000) TOTAL_WORKER_TIME,
            TOTAL_LOGICAL_READS,
            TOTAL_PHYSICAL_READS,
            TOTAL_LOGICAL_WRITES
            --total_rows
        from
            sys.dm_exec_query_stats
        where sql_handle = cast('' as xml).value('xs:hexBinary("{sql_id}")', 'varbinary(max)')
        order by total_elapsed_time desc
        ''',  'plan':f'''
            select
                QUERY_PLAN
            from
                sys.dm_exec_query_stats
                CROSS APPLY sys.dm_exec_query_plan(plan_handle)
            where sql_handle = cast('' as xml).value('xs:hexBinary("{sql_id}")', 'varbinary(max)') '''}
    if sql_text and schema:
        flag, json_data = run_batch_sql(database, query)
        if not flag:
            print(str(build_exception_from_java(json_data)))
            return sql_detail
        plan_data = json_data.get('plan')
        detail_data = json_data.get('detail')
        plan_dic = plan_data[0].get('QUERY_PLAN') if plan_data else ''
        if detail_data:
            metric_dict = {'TOTAL_ELAPSED_TIME':'()',  'TOTAL_WORKER_TIME':'()', 
             'TOTAL_LOGICAL_READS':'', 
             'TOTAL_PHYSICAL_READS':'', 
             'TOTAL_LOGICAL_WRITES':'', 
             'TOTAL_ROWS':'', 
             'EXECUTION_COUNT':''}
            for idx, x in enumerate(detail_data):
                pie_chart_data = {k:v for k, v in x.items() if k in ('TOTAL_ELAPSED_TIME',
                                                                     'TOTAL_WORKER_TIME')}
                total_executions = x.get('EXECUTION_COUNT') if x.get('EXECUTION_COUNT') != 0 else 1
                execution_data = [{u'\u6307\u6807':metric_dict.get(k),  u'\u603b\u6570':v,  u'\u5e73\u5747\u6bcf\u6b21\u6267\u884c':round(v / total_executions)} for k, v in x.items() if k in metric_dict]
                key = f'''{time_str}-{idx}'''
                sql_detail['stats'][key] = {'child_summary':[
                  {'CREATION_TIME':x.get('CREATION_TIME'), 
                   'LAST_EXECUTION_TIME':x.get('LAST_EXECUTION_TIME')}], 
                 'pie_chart_data':pie_chart_data, 
                 'execution_stats':{'header':[
                   '', '', '', ''], 
                  'data':execution_data}}

    sql_detail['sql_text'] = sql_text
    if plan_dic:
        sql_detail['plans'] = plan_dic
    detail = SQL_Detail()
    detail.created_at = datetime.now().replace(microsecond=0)
    detail.sql_detail = sql_detail
    detail.sql_id = sql_id
    detail.database = database
    detail.save()
    return sql_detail


def get_or_gen_sql_detail(database, sql_id, sql_text=None, schema=None, get_detail=True):
    detail_data = {}
    db_type = database.db_type
    if not sql_text:
        sql_text, schema = get_sql_text(database, sql_id)
    if db_type == 'db2':
        detail_data = db2_gen_sql_detail(database, sql_id, sql_text, schema, get_detail)
    else:
        if db_type == 'mysql':
            detail_data = mysql_gen_sql_detail(database, sql_id, sql_text, schema, get_detail)
        else:
            if db_type == 'sqlserver':
                detail_data = sqlserver_gen_sql_detail(database, sql_id, sql_text, schema, get_detail)
        return detail_data


def new_sql_detail(database, sql_id, sql_text=None, schema=None, get_detail=True):
    yesterday = datetime.now() + (timedelta(days=-1))
    obj = (((SQL_Detail.objects.filter(database=database)).filter(sql_id=sql_id)).filter(created_at__gt=yesterday)).order_by('-created_at').first()
    if obj:
        return obj.sql_detail
    detail_data = {}
    db_type = database.db_type
    if db_type == 'db2':
        detail_data = db2_gen_sql_detail(database, sql_id, sql_text, schema, get_detail)
    else:
        if db_type == 'mysql':
            detail_data = mysql_gen_sql_detail(database, sql_id, sql_text, schema, get_detail)
        else:
            if db_type == 'sqlserver':
                detail_data = sqlserver_gen_sql_detail(database, sql_id, sql_text, schema, get_detail)
        return detail_data


def test_db():
    from monitor.models import DB2_ASH
    for x in DB2_ASH.objects.all():
        print(x)
        db = Database.objects.get(pk=x.database_id)
        db2_gen_sql_detail(db, x.sql_id, x.sql_text, x.authid)
# okay decompiling ./restful/hawkeye/api/v1/monitor/services/sqldetail/generalSQLDetail.pyc
