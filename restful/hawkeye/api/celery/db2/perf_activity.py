# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/celery/db2/perf_activity.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 8544 bytes
from monitor.models import Performance, DB2_ASH
from common.util import get_10s_time, to_date, gen_sql_id, build_exception_from_java
from api.v1.monitor.services.runsqlService import run_sql
from common.storages import redis
import json
from api.v1.monitor.services.sqldetail.generalSQLDetail import new_sql_detail
from alarm.enum.alarm_warn_enum import WARN_ENUM
from api.v1.alarm.services.warnService import customized_warn_scanner
MAX_INTERVAL = 15
INTERVAL = 10

def db2_performance(database):
    query = '\n    select\n    TOTAL_CONS, APPLS_CUR_CONS, APPLS_IN_DB2, LOCKS_WAITING, NUM_ASSOC_AGENTS, ACTIVE_SORTS,\n    LOCKS_HELD, LOCK_WAITS,\n    TOTAL_SORTS, SORT_OVERFLOWS,\n    POOL_DATA_L_READS, POOL_TEMP_DATA_L_READS, POOL_INDEX_L_READS, POOL_TEMP_INDEX_L_READS, POOL_XDA_L_READS, POOL_TEMP_XDA_L_READS, POOL_DATA_P_READS, POOL_TEMP_DATA_P_READS,\n    POOL_INDEX_P_READS, POOL_TEMP_INDEX_P_READS, POOL_XDA_P_READS, POOL_TEMP_XDA_P_READS,\n    POOL_DATA_WRITES, POOL_INDEX_WRITES, POOL_XDA_WRITES,\n    DIRECT_READS, DIRECT_WRITES,\n    COMMIT_SQL_STMTS, ROLLBACK_SQL_STMTS, DYNAMIC_SQL_STMTS, STATIC_SQL_STMTS, FAILED_SQL_STMTS, SELECT_SQL_STMTS, UID_SQL_STMTS, DDL_SQL_STMTS,\n    ROWS_DELETED, ROWS_INSERTED, ROWS_UPDATED, ROWS_SELECTED, ROWS_READ,\n    LOG_READS, LOG_WRITES\n    from sysibmadm.snapdb'
    stats_list_realtime = [
     'APPLS_CUR_CONS', 'LOCKS_HELD', 'APPLS_IN_DB2', 'LOCKS_WAITING', 'NUM_ASSOC_AGENTS', 'ACTIVE_SORTS']
    stats_list_delta = ['TOTAL_CONS', 'LOCK_WAITS', 'TOTAL_SORTS', 'SORT_OVERFLOWS', 'POOL_DATA_L_READS',
     'POOL_TEMP_DATA_L_READS', 'POOL_INDEX_L_READS', 'POOL_TEMP_INDEX_L_READS', 'POOL_XDA_L_READS',
     'POOL_TEMP_XDA_L_READS', 'POOL_DATA_P_READS', 'POOL_TEMP_DATA_P_READS', 'POOL_INDEX_P_READS',
     'POOL_TEMP_INDEX_P_READS', 'POOL_XDA_P_READS', 'POOL_TEMP_XDA_P_READS', 'POOL_DATA_WRITES',
     'POOL_INDEX_WRITES', 'POOL_XDA_WRITES', 'DIRECT_READS', 'DIRECT_WRITES', 'COMMIT_SQL_STMTS',
     'ROLLBACK_SQL_STMTS', 'DYNAMIC_SQL_STMTS', 'STATIC_SQL_STMTS', 'FAILED_SQL_STMTS',
     'SELECT_SQL_STMTS', 'UID_SQL_STMTS', 'DDL_SQL_STMTS', 'ROWS_DELETED', 'ROWS_INSERTED',
     'ROWS_UPDATED', 'ROWS_SELECTED', 'ROWS_READ', 'LOG_READS', 'LOG_WRITES']
    date_current = get_10s_time()
    flag, json_data_current = run_sql(database, query)
    if not flag or not json_data_current:
        print(str(build_exception_from_java(json_data_current)))
        return
    json_data_current = json_data_current[0]
    key = str(database.id) + ':performance'
    date_key = str(database.id) + ':performance_date'
    json_data_str_prev = redis.get(key)
    date_prev = redis.get(date_key)
    redis.setex(key, MAX_INTERVAL, json.dumps(json_data_current))
    redis.setex(date_key, MAX_INTERVAL, str(date_current))
    if json_data_str_prev:
        if date_prev:
            if (date_current - to_date(date_prev)).total_seconds() < MAX_INTERVAL:
                json_data_prev = json.loads(json_data_str_prev)
                for key, value in json_data_current.items():
                    p = Performance()
                    p.name = key
                    p.created_at = date_current
                    p.database = database
                    if key in stats_list_realtime:
                        p.value = value
                    else:
                        if key in stats_list_delta:
                            p.value = (float(value) - float(json_data_prev.get(key))) / INTERVAL
                    p.save()


def db2_activity(database):
    padding_str = '_v97' if database.is_v97() else ''
    query1 = "\n    SELECT distinct rtrim(app.db_name) DB_NAME,\n                app.agent_id,\n                app.appl_id,\n                app.appl_name,\n                app.appl_status,\n                app.authid,\n                t.activity_type,\n  (select cast(p.stmt_text as varchar(2000)) from  table(mon_get_pkg_cache_stmt(NULL, t.executable_id, NULL, -2)) as p FETCH FIRST 1 ROWS ONLY) stmt_text,\n                hex(t.EXECUTABLE_ID) EXECUTABLE_ID,\n                uow.ELAPSED_TIME_SEC,\n                round(uow.TOTAL_CPU_TIME/1000000) TOTAL_CPU_TIME,\n                uow.TOTAL_ROWS_READ,\n                uow.TOTAL_ROWS_RETURNED\nFROM table(wlm_get_workload_occurrence_activities(NULL, -2)) as t,\n     sysibmadm.applications app,\n     SYSIBMADM.MON_CURRENT_UOW uow\nWHERE\n  app.agent_id = t.application_handle\n  and t.application_handle = uow.application_handle\n  and app.appl_id != (values application_id())\n  and app.appl_status not in ('CONNECTED',\n                              'UOWWAIT')"
    query1_v97_base = "\n        SELECT\n        distinct rtrim(app.db_name) DB_NAME, app.agent_id, app.appl_id, app.appl_name, app.appl_status, app.authid,\n        t.activity_type, cast(p.stmt_text as varchar(2000)) stmt_text, hex(t.EXECUTABLE_ID) EXECUTABLE_ID\n    FROM table(wlm_get_workload_occurrence_activities_v97(NULL, -2)) as t,\n         table(mon_get_pkg_cache_stmt(NULL, NULL, NULL, -2)) as p,\n         sysibmadm.applications app\n    WHERE t.executable_id = p.executable_id\n        and app.agent_id = t.application_handle\n        and app.appl_id != (values application_id())\n        and app.appl_status not in ('CONNECTED','UOWWAIT')"
    query1_v97 = "\n    SELECT distinct rtrim(app.db_name) DB_NAME,\n                app.agent_id,\n                app.appl_id,\n                app.appl_name,\n                app.appl_status,\n                app.authid,\n                t.activity_type,\n  (select cast(p.stmt_text as varchar(2000)) from  table(mon_get_pkg_cache_stmt(NULL, t.executable_id, NULL, -2)) as p FETCH FIRST 1 ROWS ONLY) stmt_text,\n                hex(t.EXECUTABLE_ID) EXECUTABLE_ID,\n                uow.ELAPSED_TIME_SEC,\n                round(uow.TOTAL_CPU_TIME/1000000) TOTAL_CPU_TIME,\n                uow.TOTAL_ROWS_READ,\n                uow.TOTAL_ROWS_RETURNED\nFROM table(wlm_get_workload_occurrence_activities_v97(NULL, -2)) as t,\n     sysibmadm.applications app,\n     SYSIBMADM.MON_CURRENT_UOW uow\nWHERE\n  app.agent_id = t.application_handle\n  and t.application_handle = uow.application_handle\n  and app.appl_id != (values application_id())\n  and app.appl_status not in ('CONNECTED',\n                              'UOWWAIT')"
    query2 = "\n    SELECT\n        app.db_name, app.agent_id, app.appl_id, app.appl_name, app.appl_status, app.authid,\n        t.activity_type, (select VALUE from table(WLM_GET_ACTIVITY_DETAILS(t.application_handle,t.uow_id,t.activity_id,-2)) where name = 'STMT_TEXT') STMT_TEXT\n    FROM table(wlm_get_workload_occurrence_activities(cast(null as bigint), -1)) as t,\n         sysibmadm.applications app\n    WHERE app.agent_id = t.application_handle\n        and app.appl_id != (values application_id())\n        and app.appl_status not in ('CONNECTED','UOWWAIT')"
    ash_date = get_10s_time()
    if not database.is_v95_base():
        if database.is_v97():
            flag, json_data = run_sql(database, query1_v97)
            if not flag:
                flag, json_data = run_sql(database, query1_v97_base)
            else:
                flag, json_data = run_sql(database, query1)
    else:
        flag, json_data = run_sql(database, query2)
    if not flag:
        print(str(build_exception_from_java(json_data)))
        return
    for x in json_data:
        ash = DB2_ASH()
        ash.db_name = x.get('AUTHID').strip()
        ash.session_id = x.get('AGENT_ID')
        ash.machine = x.get('APPL_ID')
        ash.program = x.get('APPL_NAME')
        ash.appl_status = x.get('APPL_STATUS')
        ash.username = x.get('AUTHID').strip()
        ash.command = x.get('ACTIVITY_TYPE')
        ash.sql_text = x.get('STMT_TEXT')
        if not database.is_v95_base():
            ash.sql_id = x.get('EXECUTABLE_ID')
            ash.sql_elapsed_time = x.get('ELAPSED_TIME_SEC')
            ash.total_cpu_time = x.get('TOTAL_CPU_TIME')
            ash.rows_read = x.get('TOTAL_ROWS_READ')
            ash.rows_returned = x.get('TOTAL_ROWS_RETURNED')
        else:
            ash.sql_id = gen_sql_id(x.get('STMT_TEXT')) if x.get('STMT_TEXT') else None
        ash.created_at = ash_date
        ash.database = database
        ash.save()

    warn = WARN_ENUM.get(database.db_type).Active_Session_Warn
    p = Performance(inst_id=database.db_name, name=warn.name, value=len(json_data), created_at=ash_date)
    customized_warn_scanner(warn, p, database, False)
# okay decompiling ./restful/hawkeye/api/celery/db2/perf_activity.pyc
