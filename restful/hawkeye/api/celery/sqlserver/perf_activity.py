# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/celery/sqlserver/perf_activity.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 7864 bytes
from monitor.models import Performance, MSSQL_ASH
from common.util import get_10s_time, to_date
from api.v1.monitor.services.runsqlService import run_sql
from common.storages import redis
import json, re
from alarm.enum.alarm_warn_enum import WARN_ENUM
from api.v1.alarm.services.warnService import customized_warn_scanner
from common.util import build_exception_from_java
MAX_INTERVAL = 15
INTERVAL = 10

def sqlserver_performance(database):
    query = "\nselect COUNTER_NAME,CNTR_VALUE from sys.dm_os_performance_counters where\n(object_name like '%sql statistics%' and counter_name = 'batch requests/sec') or\n(object_name like '%sql statistics%' and counter_name = 'sql compilations/sec') or\n(object_name like '%sql statistics%' and counter_name = 'sql re-compilations/sec') or\n(object_name like '%buffer manager%' and counter_name = 'lazy writes/sec') or\n(object_name like '%buffer manager%' and counter_name = 'page life expectancy') or\n(object_name like '%memory manager%' and counter_name = 'connection memory (kb)') or\n(object_name like '%memory manager%' and counter_name = 'memory grants pending') or\n(object_name like '%memory manager%' and counter_name = 'sql cache memory (kb)') or\n(object_name like '%memory manager%' and counter_name = 'target server memory (kb)') or\n(object_name like '%memory manager%' and counter_name = 'total server memory (kb)') or\n(object_name like '%access methods%' and counter_name = 'full scans/sec') or\n(object_name like '%access methods%' and counter_name = 'forwarded records/sec') or\n(object_name like '%access methods%' and counter_name = 'mixed page allocations/sec') or\n(object_name like '%access methods%' and counter_name = 'page splits/sec') or\n(object_name like '%access methods%' and counter_name = 'table lock escalations/sec') or\n(object_name like '%general statistics%' and counter_name = 'logins/sec') or\n(object_name like '%general statistics%' and counter_name = 'logouts/sec') or\n(object_name like '%general statistics%' and counter_name = 'user connections') or\n(object_name like '%general statistics%' and counter_name = 'processes blocked') or\n(object_name like '%latches%' and counter_name = 'latch waits/sec') or\n(object_name like '%latches%' and counter_name = 'average latch wait time (ms)') or\n(object_name like '%access methods%' and counter_name = 'workfiles created/sec') or\n(object_name like '%access methods%' and counter_name = 'worktables created/sec') or\n(object_name like '%general statistics%' and counter_name = 'active temp tables') or\n(object_name like '%general statistics%' and counter_name = 'temp tables creation rate') or\n(object_name like '%general statistics%' and counter_name = 'temp tables for destruction') or\n(object_name like '%databases%' and counter_name ='active transactions' and instance_name = '_Total') or\n(object_name like '%databases%' and counter_name ='Transactions/sec' and instance_name = '_Total') or\n(object_name like '%databases%' and counter_name ='log flushes/sec' and instance_name = '_Total') or\n(object_name like '%databases%' and counter_name ='cache hit ratio' and instance_name = '_Total') or\n(object_name like '%SQLServer:Locks%' and counter_name like '%Lock%' and instance_name = '_Total')"
    match_patern = re.compile('/sec', re.IGNORECASE)
    date_current = get_10s_time()
    flag, json_data_current = run_sql(database, query)
    if not flag:
        print(str(build_exception_from_java(json_data_current)))
        return
    key = str(database.id) + ':performance'
    date_key = str(database.id) + ':performance_date'
    json_data_str_prev = redis.get(key)
    date_prev = redis.get(date_key)
    keys = ['COUNTER_NAME', 'CNTR_VALUE']
    redis.set(key, json.dumps(json_data_current))
    redis.set(date_key, str(date_current))
    if json_data_str_prev and date_prev and (date_current - to_date(date_prev)).total_seconds() < MAX_INTERVAL:
        json_data_prev = json.loads(json_data_str_prev)
        for idx, obj in enumerate(json_data_current):
            name = obj.get(keys[0])
            value = obj.get(keys[1])
            p = Performance()
            p.name = name
            p.database = database
            p.created_at = date_current
            if re.search(match_patern, name):
                p.value = round((float(value) - float(json_data_prev[idx].get(keys[1]))) / INTERVAL, 1)
            else:
                p.value = float(value)
            p.save()


def get_sqlserver_activity(databases):
    query = "\n            SELECT /* sample_query */\n            req.SESSION_ID,\n            convert(varchar(25), req.START_TIME, 120) START_TIME,\n            req.STATUS,\n            req.COMMAND,\n            (select name from master..sysdatabases where dbid = req.database_id) DB_NAME,\n            ses.LOGIN_NAME,\n            ses.HOST_NAME,\n            ses.PROGRAM_NAME,\n            req.BLOCKING_SESSION_ID,\n            req.WAIT_TYPE,\n            req.WAIT_TIME,\n            req.WAIT_RESOURCE,\n            req.TOTAL_ELAPSED_TIME,\n            req.ROW_COUNT,\n            sqltext.TEXT SQLTEXT,\n            substring(sys.fn_sqlvarbasetostr(req.sql_handle),3,1000) SQL_HANDLE,\n            con.CLIENT_NET_ADDRESS,\n            case when req.wait_resource like '%SPID%' then SUBSTRING(wait_resource, 1, CHARINDEX(' ', wait_resource)-1) else '' end LINKED_IP,\n            cast(case when req.wait_resource like '%SPID%' then SUBSTRING(wait_resource, CHARINDEX('=', wait_resource)+1, CHARINDEX(')', wait_resource)-CHARINDEX('=', wait_resource)-1) else '0' end as int) LINKED_SPID,\n            DATEDIFF(SECOND, req.START_TIME, getdate()) TIME\n            FROM sys.dm_exec_requests req\n            inner join sys.dm_exec_sessions ses on req.session_id = ses.session_id\n            inner join sys.dm_exec_connections con on ses.session_id = con.session_id\n            CROSS APPLY sys.dm_exec_sql_text(sql_handle) AS sqltext\n            where sqltext.TEXT not like '%sample_query%'"
    ash_date = get_10s_time()
    result_set = {}
    db_set = {}
    for db in databases:
        flag, json_data = run_sql(db, query)
        if not flag:
            print(str(build_exception_from_java(json_data)))
            continue
            result_set[str(db.id)] = json_data
            db_set[str(db.id)] = db

    for db_id, ash_data in result_set.items():
        for x in ash_data:
            ash = MSSQL_ASH()
            ash.session_id = x.get('SESSION_ID')
            ash.start_time = x.get('START_TIME')
            ash.status = x.get('STATUS').upper()
            ash.command = x.get('COMMAND')
            ash.db_name = x.get('DB_NAME')
            ash.username = x.get('LOGIN_NAME')
            ash.machine = x.get('HOST_NAME')
            ash.program = x.get('PROGRAM_NAME')
            ash.b_blocker = x.get('BLOCKING_SESSION_ID')
            ash.wait_type = x.get('WAIT_TYPE')
            ash.wait_time = x.get('WAIT_TIME')
            ash.wait_resource = x.get('WAIT_RESOURCE')
            ash.total_elapsed_time = x.get('TOTAL_ELAPSED_TIME')
            ash.row_count = x.get('ROW_COUNT')
            ash.sql_text = x.get('SQLTEXT')
            ash.sql_id = x.get('SQL_HANDLE')
            ash.client_net_address = x.get('CLIENT_NET_ADDRESS')
            ash.linked_ip = x.get('LINKED_IP')
            ash.linked_spid = x.get('LINKED_SPID')
            ash.sql_elapsed_time = x.get('TIME')
            ash.created_at = ash_date
            ash.database = db_set.get(db_id)
            ash.save()

        database = db_set.get(db_id)
        warn = WARN_ENUM.get(database.db_type).Active_Session_Warn
        p = Performance(inst_id=database.db_name, name=warn.name, value=len(ash_data), created_at=ash_date)
        customized_warn_scanner(warn, p, database, False)
# okay decompiling ./restful/hawkeye/api/celery/sqlserver/perf_activity.pyc
