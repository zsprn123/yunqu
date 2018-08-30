# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/celery/oracle/perf_activity.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 14026 bytes
from monitor.models import Performance, Oracle_ASH
from common.util import get_10s_time, to_date
from api.v1.monitor.services.runsqlService import run_sql, run_batch_sql
from common.storages import redis
import json
from api.v1.alarm.services.warnService import customized_warn_scanner
from alarm.enum.alarm_warn_enum import WARN_ENUM
from datetime import timedelta
import re
from common.util import build_exception_from_java
MAX_INTERVAL = 15
INTERVAL = 10
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

def convert_oracle_interval_to_secodns(ora_interval):
    """convert Oracle +00 00:02:07.2 to seconds
    day (2) to second (n) interval, where n is 0 or 1"""
    time_list = re.split('[: ]', ora_interval[1:])
    return (timedelta(days=int(time_list[0]), hours=int(time_list[1]), minutes=int(time_list[2]), seconds=float(time_list[3]))).total_seconds()


def oracle_performance(database):
    query = {'stats':"\nselect inst_id, name, value\nfrom\n    (\n        select ss.inst_id\n        ,      sn.name\n        ,      ss.value\n        from   v$statname sn\n        ,      gv$sysstat  ss\n        where  sn.statistic# = ss.statistic#\n        and    sn.name in (\n        'execute count', 'logons cumulative',\n        'parse count (hard)', 'parse count (total)', 'parse count (failures)',\n        'physical read total IO requests', 'physical read total bytes',\n        'physical write total IO requests', 'physical write total bytes',\n        'redo size', --'session cursor cache hits',\n        'session logical reads', 'user calls', 'user commits', 'user rollbacks','logons current',\n        'gc cr blocks received','gc current blocks received',\n        'gc cr block receive time', 'gc current block receive time')\n        union all\n        select inst_id\n        ,      STAT_NAME\n        ,      VALUE\n        from gv$osstat\n        where STAT_NAME in ('BUSY_TIME','IDLE_TIME')\n        union all\n        select\n          (select min(INSTANCE_NUMBER) from gv$instance),\n          'SCN GAP Per Minute',\n          current_scn\n        from v$database\n    )\norder by 1,2", 
     'wait':"\n        select inst_id, event, TIME_WAITED, TOTAL_WAITS\n        from gv$system_event\n        where\n        event in (\n            'log file sync',\n            'log file parallel write',\n            'db file parallel write',\n            'db file sequential read',\n            'db file scattered read',\n            'direct path read',\n            'direct path read temp'\n            )\n            order by 1,2", 
     'dg':"\n        select\n            INST_ID,\n            NAME,\n            VALUE\n        from gv$dataguard_stats\n        where name in ('apply lag','transport lag')"}
    stats_list = {'session cursor cache hits':'session cursor cache hits', 
     'BUSY_TIME':'Host CPU Utilization (%)', 
     'physical write total IO requests':'Physical Write IO Requests Per Sec', 
     'physical write total bytes':'Physical Write Total Bytes Per Sec', 
     'physical read total IO requests':'Physical Read IO Requests Per Sec', 
     'physical read total bytes':'Physical Read Total Bytes Per Sec', 
     'SCN GAP Per Minute':'SCN GAP Per Minute', 
     'execute count':'Executions Per Sec', 
     'logons cumulative':'Logons Per Sec', 
     'logons current':'Session Count', 
     'parse count (failures)':'Parse Failure Count Per Sec', 
     'parse count (hard)':'Hard Parse Count Per Sec', 
     'parse count (total)':'Total Parse Count Per Sec', 
     'redo size':'Redo Generated Per Sec', 
     'session logical reads':'Logical Reads Per Sec', 
     'user rollbacks':'User Rollbacks Per Sec', 
     'user calls':'User Calls Per Sec', 
     'user commits':'User Commits Per Sec', 
     'gc cr blocks received':'GC CR Block Received Per Second', 
     'gc current blocks received':'GC Current Block Received Per Second', 
     'gc cr block receive time':'Global Cache Average CR Get Time', 
     'gc current block receive time':'Global Cache Average Current Get Time'}
    none_delta_stats = ('BUSY_TIME', 'IDLE_TIME', 'gc cr block receive time', 'gc current block receive time',
                        'logons current')
    date_current = get_10s_time()
    if not database.dg_stats:
        query.pop('dg')
    flag, json_data = run_batch_sql(database, query)
    if not flag:
        print(str(build_exception_from_java(json_data)))
        return
    json_data_1_current = json_data.get('stats')
    json_data_2_current = json_data.get('wait')
    json_data_dg = json_data.get('dg')
    key1 = str(database.id) + ':performance1'
    key2 = str(database.id) + ':performance2'
    date_key = str(database.id) + ':performance_date'
    json_data_str_1 = redis.get(key1)
    json_data_str_2 = redis.get(key2)
    date_prev = redis.get(date_key)
    keys1 = [
     'NAME', 'VALUE']
    keys2 = ['EVENT', 'TIME_WAITED', 'TOTAL_WAITS']
    redis.setex(key1, MAX_INTERVAL, json.dumps(json_data_1_current))
    redis.setex(key2, MAX_INTERVAL, json.dumps(json_data_2_current))
    redis.setex(date_key, MAX_INTERVAL, str(date_current))
    if json_data_str_1:
        if json_data_str_2:
            if date_prev:
                if (date_current - to_date(date_prev)).total_seconds() < MAX_INTERVAL:
                    json_data_1_prev = json.loads(json_data_str_1)
                    json_data_2_prev = json.loads(json_data_str_2)
                    for idx, obj in enumerate(json_data_1_current):
                        name = obj.get(keys1[0])
                        if name == 'IDLE_TIME':
                            continue
                        value = obj.get(keys1[1])
                        inst_id = obj.get('INST_ID')
                        p = Performance()
                        p.name = stats_list.get(name)
                        p.database = database
                        p.created_at = date_current
                        p.inst_id = inst_id
                        delta = float(value) - float(json_data_1_prev[idx].get(keys1[1]))
                        total = 1
                        if name in none_delta_stats:
                            if name in 'BUSY_TIME':
                                total = delta + float(json_data_1_current[idx + 1].get(keys1[1])) - float(json_data_1_prev[idx + 1].get(keys1[1]))
                                value = round(delta / (total if total != 0 else 1) * 100, 1)
                            else:
                                if name in ('gc cr block receive time', 'gc current block receive time'):
                                    delta = 10.0 * delta
                                    total = float(json_data_1_current[idx + 1].get(keys1[1])) - float(json_data_1_prev[idx + 1].get(keys1[1]))
                                    value = round(delta / (total if total != 0 else 1), 1)
                            p.value = value
                        else:
                            p.value = round(delta / INTERVAL, 1)
                        p.save()

                    for idx, obj in enumerate(json_data_2_current):
                        name = obj.get(keys2[0])
                        value1 = obj.get(keys2[1])
                        value2 = obj.get(keys2[2])
                        inst_id = obj.get('INST_ID')
                        delta = 10.0 * (float(value1) - float(json_data_2_prev[idx].get(keys2[1])))
                        total = float(value2) - float(json_data_2_prev[idx].get(keys2[2]))
                        value = round(delta / (total if total != 0 else 1), 1)
                        p = Performance()
                        p.name = name
                        p.database = database
                        p.created_at = date_current
                        p.inst_id = inst_id
                        p.value = value
                        p.save()

                    if json_data_dg:
                        for x in json_data_dg:
                            p = Performance()
                            p.name = x.get('NAME')
                            p.inst_id = x.get('INST_ID')
                            p.value = convert_oracle_interval_to_secodns(x.get('VALUE'))
                            p.database = database
                            p.created_at = date_current
                            p.save()


def oracle_activity(database):
    if database.version == '10':
        query = "\n            select /*+ leading(b a)*/\n                a.inst_id,\n                SESSION_ID sid,\n                SESSION_SERIAL# serial,\n                SESSION_ID || ',' || SESSION_SERIAL# || '@'|| a.inst_id SESSION_ID,\n                (select username from dba_users u where u.user_id = a.user_id) username,\n                '' machine,\n                program,\n                --status,\n                case SQL_OPCODE\n                    when 1 then 'CREATE TABLE'\n                    when 2 then 'INSERT'\n                    when 3 then 'SELECT'\n                    when 6 then 'UPDATE'\n                    when 7 then 'DELETE'\n                    when 9 then 'CREATE INDEX'\n                    when 11 then 'ALTER INDEX'\n                    when 15 then 'ALTER INDEX' else 'Others' end command,\n                SQL_ID,\n                SQL_PLAN_HASH_VALUE,\n                nvl(event, 'ON CPU') event,\n                p1,\n                p2,\n                p3,\n                nvl(wait_class, 'ON CPU') wait_class ,\n                module,\n                action,\n                (select name from V$ACTIVE_SERVICES s where s.NAME_HASH = a.SERVICE_HASH) service_name,\n                '' plsql_object_name,\n                '' plsql_entry_object_name,\n                BLOCKING_SESSION,\n                BLOCKING_SESSION_SERIAL# BLOCKING_SESSION_SERIAL,\n                null SQL_PLAN_LINE_ID,\n                '' SQL_PLAN_OPERATION,\n                SESSION_TYPE,\n                (select SQL_TEXT from v$sql b where b.sql_id = a.sql_id and rownum =1) SQL_TEXT\n            from gv$ACTIVE_SESSION_HISTORY a\n            where a.SAMPLE_TIME between systimestamp - numtodsinterval(2,'SECOND') and systimestamp - numtodsinterval(1,'SECOND')\n            and nvl(a.wait_class,'ON CPU') <> 'Idle'"
    else:
        if database.version >= '11':
            query = "\n            select /*+ leading(b a)*/\n                a.inst_id,\n                SESSION_ID sid,\n                SESSION_SERIAL# serial,\n                SESSION_ID || ',' || SESSION_SERIAL# || '@'|| a.inst_id SESSION_ID,\n                round((cast(sample_time as date)-a.sql_exec_start)*24*3600) SQL_ELAPSED_TIME,\n                (select username from dba_users u where u.user_id = a.user_id) username,\n                machine,\n                program,\n                --status,\n                case SQL_OPCODE\n                    when 1 then 'CREATE TABLE'\n                    when 2 then 'INSERT'\n                    when 3 then 'SELECT'\n                    when 6 then 'UPDATE'\n                    when 7 then 'DELETE'\n                    when 9 then 'CREATE INDEX'\n                    when 11 then 'ALTER INDEX'\n                    when 15 then 'ALTER INDEX' else 'Others' end command,\n                SQL_ID,\n                SQL_PLAN_HASH_VALUE,\n                nvl(event, 'ON CPU') event,\n                p1,\n                p2,\n                p3,\n                nvl(wait_class, 'ON CPU') wait_class,\n                module,\n                action,\n                (select name from V$ACTIVE_SERVICES s where s.NAME_HASH = a.SERVICE_HASH) SERVER_NAME ,\n                -- (select object_name from dba_objects s where s.object_id = a.PLSQL_OBJECT_ID) plsql_object_name,\n                -- (select object_name from dba_objects s where s.object_id = a.PLSQL_ENTRY_OBJECT_ID) plsql_entry_object_name,\n                '' plsql_object_name,\n                '' plsql_entry_object_name,\n                BLOCKING_SESSION,\n                BLOCKING_SESSION_SERIAL# BLOCKING_SESSION_SERIAL,\n                SQL_PLAN_LINE_ID,\n                SQL_PLAN_OPERATION || ' ' || SQL_PLAN_OPTIONS SQL_PLAN_OPERATION,\n                SESSION_TYPE,\n                (select sql_fulltext from v$sql b where b.sql_id = a.sql_id and rownum =1) SQL_TEXT\n            from gv$ACTIVE_SESSION_HISTORY a\n            where a.SAMPLE_TIME between systimestamp - numtodsinterval(2,'SECOND') and systimestamp - numtodsinterval(1,'SECOND')\n            and nvl(a.wait_class,'ON CPU') <> 'Idle'\n        "
    ash_date = get_10s_time()
    flag, json_data = run_sql(database, query)
    if not flag:
        print(str(build_exception_from_java(json_data)))
        return
    for x in json_data:
        ash = Oracle_ASH()
        ash.inst_id = x.get('INST_ID')
        ash.sid = x.get('SID')
        ash.serial = x.get('SERIAL')
        ash.username = x.get('USERNAME')
        ash.db_name = x.get('USERNAME')
        ash.machine = x.get('MACHINE')
        ash.program = x.get('PROGRAM')
        ash.status = x.get('STATUS')
        ash.command = x.get('COMMAND')
        ash.sql_hash_value = x.get('SQL_HASH_VALUE')
        ash.sql_id = x.get('SQL_ID')
        ash.sql_text = x.get('SQL_TEXT')
        ash.sql_plan_hash_value = x.get('SQL_PLAN_HASH_VALUE')
        ash.event = x.get('EVENT')
        ash.p1 = x.get('P1')
        ash.p2 = x.get('P2')
        ash.p3 = x.get('P3')
        ash.wait_class = x.get('WAIT_CLASS')
        ash.module = x.get('MODULE')
        ash.action = x.get('ACTION')
        ash.service_name = x.get('SERVICE_NAME')
        ash.plsql_object_name = x.get('PLSQL_OBJECT_NAME')
        ash.plsql_entry_object_name = x.get('PLSQL_ENTRY_OBJECT_NAME')
        ash.blocking_session = x.get('BLOCKING_SESSION')
        ash.blocking_session_serial = x.get('BLOCKING_SESSION_SERIAL')
        ash.sql_plan_line_id = x.get('SQL_PLAN_LINE_ID')
        ash.sql_plan_operation = x.get('SQL_PLAN_OPERATION')
        ash.session_type = x.get('SESSION_TYPE')
        ash.session_id = x.get('SESSION_ID')
        ash.sql_elapsed_time = x.get('SQL_ELAPSED_TIME')
        ash.created_at = ash_date
        ash.database = database
        try:
            ash.save()
        except Exception as e:
            logger.error(str(e))

    warn = WARN_ENUM.get(database.db_type).Active_Session_Warn
    p = Performance(inst_id=database.db_name, name=warn.name, value=len(json_data), created_at=ash_date)
    customized_warn_scanner(warn, p, database, False)
# okay decompiling ./restful/hawkeye/api/celery/oracle/perf_activity.pyc
