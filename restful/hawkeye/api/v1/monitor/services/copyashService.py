# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/monitor/services/copyashService.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 4727 bytes
from datetime import datetime
from api.v1.monitor.services.runsqlService import run_sql_with_dict, run_sql
from monitor.models import Oracle_ASH
from celery import shared_task

@shared_task()
def copyash(data):
    ash_query = ''
    if data['version'] == '10':
        ash_query = "\n            select\n                a.inst_id,\n                to_char(trunc(sample_time, 'MI') + (trunc(extract(second\n                    from sample_time)) - mod(trunc(extract(second\n                    from sample_time)), 10)) / 24 / 3600, 'yyyy-mm-dd hh24:mi:ss') sample_time,\n                SESSION_ID sid,\n                SESSION_SERIAL# serial,\n                (select username from dba_users u where u.user_id = a.user_id) username,\n                '' machine,\n                program,\n                --status,\n                case SQL_OPCODE\n                    when 1 then 'CREATE TABLE'\n                    when 2 then 'INSERT'\n                    when 3 then 'SELECT'\n                    when 6 then 'UPDATE'\n                    when 7 then 'DELETE'\n                    when 9 then 'CREATE INDEX'\n                    when 11 then 'ALTER INDEX'\n                    when 15 then 'ALTER INDEX' else 'Others' end command,\n                SQL_ID,\n                SQL_PLAN_HASH_VALUE,\n                nvl(event, 'ON CPU') event,\n                p1,\n                p2,\n                p3,\n                nvl(wait_class, 'ON CPU') wait_class,\n                module,\n                action,\n                (select name from V$ACTIVE_SERVICES s where s.NAME_HASH = a.SERVICE_HASH) SERVER_NAME,\n                '' plsql_object_name,\n                '' plsql_entry_object_name\n            from gv$active_session_history a\n            where a.sample_time > sysdate - 1/24 and nvl(a.wait_class,'ON CPU') <> 'Idle'"
    else:
        if data['version'] >= '11':
            ash_query = "\n            select\n                a.inst_id,\n                to_char(trunc(sample_time, 'MI') + (trunc(extract(second\n                    from sample_time)) - mod(trunc(extract(second\n                    from sample_time)), 10)) / 24 / 3600, 'yyyy-mm-dd hh24:mi:ss') sample_time,\n                SESSION_ID sid,\n                SESSION_SERIAL# serial,\n                (select username from dba_users u where u.user_id = a.user_id) username,\n                machine,\n                program,\n                --status,\n                case SQL_OPCODE\n                    when 1 then 'CREATE TABLE'\n                    when 2 then 'INSERT'\n                    when 3 then 'SELECT'\n                    when 6 then 'UPDATE'\n                    when 7 then 'DELETE'\n                    when 9 then 'CREATE INDEX'\n                    when 11 then 'ALTER INDEX'\n                    when 15 then 'ALTER INDEX' else 'Others' end command,\n                SQL_ID,\n                SQL_PLAN_HASH_VALUE,\n                nvl(event, 'ON CPU') event,\n                p1,\n                p2,\n                p3,\n                nvl(wait_class, 'ON CPU') wait_class,\n                module,\n                action,\n                (select name from V$ACTIVE_SERVICES s where s.NAME_HASH = a.SERVICE_HASH) SERVER_NAME ,\n                (select object_name from dba_objects s where s.object_id = a.PLSQL_OBJECT_ID) plsql_object_name,\n                (select object_name from dba_objects s where s.object_id = a.PLSQL_ENTRY_OBJECT_ID) plsql_entry_object_name\n            from gv$active_session_history a\n            where a.sample_time > sysdate - 1/24 and nvl(a.wait_class,'ON CPU') <> 'Idle'"
    flag, json_data = run_sql_with_dict(data, ash_query)
    ash_list = []
    for x in json_data:
        ash = Oracle_ASH()
        ash.inst_id = x.get('INSTANCE_NUMBER')
        ash.sid = x.get('SID')
        ash.serial = x.get('SERIAL')
        ash.username = x.get('USERNAME')
        ash.machine = x.get('MACHINE')
        ash.program = x.get('PROGRAM')
        ash.status = x.get('STATUS')
        ash.command = x.get('COMMAND')
        ash.sql_hash_value = x.get('SQL_HASH_VALUE')
        ash.sql_id = x.get('SQL_ID')
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
        ash.created_at = x.get('SAMPLE_TIME')
        ash.database_id = data.get('id')
        ash_list.append(ash)

    Oracle_ASH.objects.bulk_create(ash_list)
# okay decompiling ./restful/hawkeye/api/v1/monitor/services/copyashService.pyc
