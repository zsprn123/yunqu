# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/celery/mysql/perf_activity.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 7689 bytes
from monitor.models import Performance, MySQL_ASH
from common.util import get_10s_time, to_date, gen_sql_id
from api.v1.monitor.services.runsqlService import run_sql
from common.storages import redis
import json, re
from api.v1.monitor.services.sqldetail.generalSQLDetail import new_sql_detail
from collections import defaultdict
from alarm.enum.alarm_warn_enum import WARN_ENUM
from api.v1.alarm.services.warnService import customized_warn_scanner
from common.util import build_exception_from_java
MAX_INTERVAL = 15
INTERVAL = 10

def mysql_performance(database):
    query = "show global status where VARIABLE_NAME in (\n        'Queries', 'Questions','Com_delete','Com_insert','Com_select','Com_update',\n        'Bytes_received','Bytes_sent',\n        'Thread_connected','Connections',\n        'Select_full_join', 'Select_full_range_join', 'Select_range', 'Select_range_check', 'Select_scan',\n        'Sort_merge_passes','Sort_scan','Sort_range','Sort_rows',\n        'Created_tmp_disk_tables','Created_tmp_files','Created_tmp_tables',\n        'Innodb_data_writes','Innodb_log_writes','Innodb_os_log_written',\n        'Innodb_rows_read','Innodb_rows_inserted','Innodb_rows_updated','Innodb_rows_deleted',\n        'Innodb_data_reads','Innodb_buffer_pool_read_requests'\n    )"
    none_delta_stats = 'Thread_connected'
    date_current = get_10s_time()
    flag, json_data_current = run_sql(database, query)
    if not flag:
        print(str(build_exception_from_java(json_data_current)))
        return
    key = str(database.id) + ':performance'
    date_key = str(database.id) + ':performance_date'
    json_data_str_prev = redis.get(key)
    date_prev = redis.get(date_key)
    k1, k2 = json_data_current[0].keys()
    if re.search('name', k1, re.IGNORECASE):
        keys = [
         k1, k2]
    else:
        keys = [
         k2, k1]
    redis.setex(key, MAX_INTERVAL, json.dumps(json_data_current))
    redis.setex(date_key, MAX_INTERVAL, str(date_current))
    if json_data_str_prev and date_prev and (date_current - to_date(date_prev)).total_seconds() < MAX_INTERVAL:
        json_data_prev = json.loads(json_data_str_prev)
        for idx, obj in enumerate(json_data_current):
            name = obj.get(keys[0])
            value = obj.get(keys[1])
            p = Performance()
            p.name = name
            p.database = database
            p.created_at = date_current
            if name in none_delta_stats:
                if not value:
                    print('value is None' + keys[1])
                p.value = float(value)
            else:
                p.value = round((float(value) - float(json_data_prev[idx].get(keys[1]))) / INTERVAL, 1)
            p.save()


def mysql_activity(database):
    query = "SELECT * FROM information_schema.processlist\n        WHERE command != 'Sleep' and id != CONNECTION_ID()\n        and state not in\n          ('Main has sent all binlog to subordinate; waiting for binlog to be up','Subordinate has read all relay log; waiting for the subordinate I/O thread t','Waiting for main to send event')\n        ORDER BY id"
    state_list = [
     ('optimizing', 'preparing', 'statistics'),
     ('copy to tmp table', 'Copying to tmp table', 'Copying to tmp table on disk', 'Creating tmp table',
 'removing tmp table'),
     ('Opening table', 'Opening tables', 'Reopen tables', 'Checking table', 'closing tables',
 'creating table', 'discard_or_import_tablespace', 'Flushing tables'),
     ('Copying to group table', 'Sorting for group', 'Sorting for order', 'Sorting index',
 'Sorting result'),
     ('update', 'updating', 'updating main table', 'updating reference tables', 'deleting from main table',
 'deleting from reference tables'),
     ('System lock', 'User lock', 'Waiting for commit lock', 'Waiting for global read lock',
 'Waiting for event metadata lock', 'Waiting for schema metadata lock', 'Waiting for stored function metadata lock',
 'Waiting for stored procedure metadata lock', 'Waiting for table level lock', 'Waiting for table metadata lock',
 'Waiting for trigger metadata lock'),
     ('checking privileges on cached query', 'checking query cache for query', 'invalidating query cache entries',
 'sending cached result to client', 'storing result in query cache', 'Waiting for query cache lock'),
     ('Reading from net', 'Writing to net', 'Sending data'),
     ('Finished reading one binlog; switching to next binlog', 'Sending binlog event to subordinate',
 'Main has sent all binlog to subordinate; waiting for binlog to be up', ' Waiting to finalize termination',
 'Waiting to finalize termination'),
     ('Waiting for main update', 'Connecting to main', 'Checking main version', 'Registering subordinate on main',
 'Requesting binlog dump', 'Waiting to reconnect after a failed binlog dump request',
 'Reconnecting after a failed binlog dump request', 'Waiting for main to send event',
 'Queueing main event to the relay log', 'Waiting to reconnect after a failed main event read',
 'Reconnecting after a failed main event read', 'Waiting for the subordinate SQL thread to free enough relay log space',
 'Waiting for subordinate mutex on exit', 'Waiting for its turn to commit'),
     ('Making temp file', 'Waiting for the next event in relay log', 'Reading event from the relay log',
 'Subordinate has read all relay log; waiting for the subordinate I/O thread t', 'Waiting for subordinate mutex on exit')]
    wait_classses = [
     'Optimization',
     'Tmp Table',
     'Table Operation',
     'Sort',
     'Update/Delete',
     'Lock',
     'Query Cache',
     'Network',
     'Main Thread',
     'I/O Thread',
     'SQL Thread',
     'Others']
    ash_date = get_10s_time()
    flag, json_data = run_sql(database, query)
    if not flag:
        print(str(build_exception_from_java(json_data)))
        return
    for x in json_data:
        ash = MySQL_ASH()
        ash.session_id = x.get('ID')
        ash.username = x.get('USER')
        ash.machine = x.get('HOST')
        ash.db_name = x.get('DB')
        ash.command = x.get('COMMAND')
        ash.sql_elapsed_time = x.get('TIME')
        ash.state = x.get('STATE')
        ash.sql_text = x.get('INFO')
        ash.sql_id = gen_sql_id(x.get('INFO')) if x.get('INFO') else None
        ash.created_at = ash_date
        ash.database = database
        others_flag = True
        for idx, val in enumerate(state_list):
            if ash.state in val:
                ash.wait_class = wait_classses[idx]
                others_flag = False
                break

        if others_flag:
            ash.wait_class = wait_classses[len(wait_classses) - 1]
        ash.save()

    warn = WARN_ENUM.get(database.db_type).Active_Session_Warn
    p = Performance(inst_id=database.db_name, name=warn.name, value=len(json_data), created_at=ash_date)
    customized_warn_scanner(warn, p, database, False)
# okay decompiling ./restful/hawkeye/api/celery/mysql/perf_activity.pyc
