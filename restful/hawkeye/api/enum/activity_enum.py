# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/enum/activity_enum.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 15711 bytes
from enum import Enum
from common.util import get_10s_timestamp
from monitor.models import Database

class MysqlActivityType(Enum):
    ASH = 'OPTIMIZATION,TMP TABLE,TABLE OPERATION,SORT,UPDATE/DELETE,LOCK,QUERY CACHE,NETWORK,MASTER THREAD,I/O THREAD,SQL THREAD,OTHERS'

    def __str__(self):
        switcher = {'ASH': ''}
        return switcher.get(self.name, '')


class OracleActivityType(Enum):
    ASH = 'ON CPU,OTHER,APPLICATION,CONFIGURATION,CLUSTER,ADMINISTRATIVE,CONCURRENCY,COMMIT,NETWORK,USER I/O,SYSTEM I/O,SCHEDULER,QUEUEING'

    def __str__(self):
        switcher = {'ASH': ''}
        return switcher.get(self.name, '')


class DB2ActivityType(Enum):
    ASH = 'BACKUP,COMMIT_ACT,COMP,CONNECTPEND,CREATE_DB,DECOUPLED,DISCONNECTPEND,INTR,IOERROR_WAIT,LOAD,LOCKWAIT,QUIESCE_TABLESPACE,RECOMP,REMOTE_RQST,RESTART,RESTORE,ROLLBACK_ACT,ROLLBACK_TO_SAVEPOINT,TEND,THABRT,THCOMT,TPREP,UNLOAD,UOWEXEC,WAITFOR_REMOTE'

    def __str__(self):
        switcher = {'ASH': ''}
        return switcher.get(self.name, '')


class SQLServerActivityType(Enum):
    ASH = 'RUNNING,RUNNABLE,SUSPENDED,SLEEPING,BACKGROUND,ROLLBACK'

    def __str__(self):
        switcher = {'ASH': ''}
        return switcher.get(self.name, '')


Activity_Type = {'oracle':OracleActivityType, 
 'mysql':MysqlActivityType, 
 'db2':DB2ActivityType, 
 'sqlserver':SQLServerActivityType}

def get_sql_id_filter_str(type, sql_id, session_id):
    sql_id_filter = ''
    if sql_id:
        sql_id_filter = f''' and sql_id = '{sql_id}'''' if sql_id != 'null' else ' and sql_id is null'
    if session_id:
        sql_id_filter = sql_id_filter + f''' and session_id = '{session_id}''''
    return sql_id_filter


def get_default_ash(type):
    ts = get_10s_timestamp()
    if type == 'oracle':
        DefaultASH = {'name':'', 
         'type':'ASH', 
         'data':{'ON CPU':[
           [
            ts, 0]], 
          'Other':[
           [
            ts, 0]], 
          'Application':[
           [
            ts, 0]], 
          'Configuration':[
           [
            ts, 0]], 
          'Cluster':[
           [
            ts, 0]], 
          'Administrative':[
           [
            ts, 0]], 
          'Concurrency':[
           [
            ts, 0]], 
          'Commit':[
           [
            ts, 0]], 
          'Network':[
           [
            ts, 0]], 
          'User I/O':[
           [
            ts, 0]], 
          'System I/O':[
           [
            ts, 0]], 
          'Scheduler':[
           [
            ts, 0]], 
          'Queueing':[
           [
            ts, 0]]}, 
         'is_open':False}
    else:
        if type == 'mysql':
            DefaultASH = {'name':'', 
             'type':'ASH', 
             'data':{'Optimization':[
               [
                ts, 0]], 
              'Tmp Table':[
               [
                ts, 0]], 
              'Table Operation':[
               [
                ts, 0]], 
              'Sort':[
               [
                ts, 0]], 
              'Update/Delete':[
               [
                ts, 0]], 
              'Lock':[
               [
                ts, 0]], 
              'Query Cache':[
               [
                ts, 0]], 
              'Network':[
               [
                ts, 0]], 
              'Master Thread':[
               [
                ts, 0]], 
              'I/O Thread':[
               [
                ts, 0]], 
              'SQL Thread':[
               [
                ts, 0]], 
              'Others':[
               [
                ts, 0]]}, 
             'is_open':False}
        else:
            if type == 'db2':
                DefaultASH = {'name':'', 
                 'type':'ASH', 
                 'data':{'BACKUP':[
                   [
                    ts, 0]], 
                  'COMMIT_ACT':[
                   [
                    ts, 0]], 
                  'COMP':[
                   [
                    ts, 0]], 
                  'CONNECTPEND':[
                   [
                    ts, 0]], 
                  'CREATE_DB':[
                   [
                    ts, 0]], 
                  'DECOUPLED':[
                   [
                    ts, 0]], 
                  'DISCONNECTPEND':[
                   [
                    ts, 0]], 
                  'INTR':[
                   [
                    ts, 0]], 
                  'IOERROR_WAIT':[
                   [
                    ts, 0]], 
                  'LOAD':[
                   [
                    ts, 0]], 
                  'LOCKWAIT':[
                   [
                    ts, 0]], 
                  'QUIESCE_TABLESPACE':[
                   [
                    ts, 0]], 
                  'RECOMP':[
                   [
                    ts, 0]], 
                  'REMOTE_RQST':[
                   [
                    ts, 0]], 
                  'RESTART':[
                   [
                    ts, 0]], 
                  'RESTORE':[
                   [
                    ts, 0]], 
                  'ROLLBACK_ACT':[
                   [
                    ts, 0]], 
                  'ROLLBACK_TO_SAVEPOINT':[
                   [
                    ts, 0]], 
                  'TEND':[
                   [
                    ts, 0]], 
                  'THABRT':[
                   [
                    ts, 0]], 
                  'THCOMT':[
                   [
                    ts, 0]], 
                  'TPREP':[
                   [
                    ts, 0]], 
                  'UNLOAD':[
                   [
                    ts, 0]], 
                  'UOWEXEC':[
                   [
                    ts, 0]], 
                  'WAITFOR_REMOTE':[
                   [
                    ts, 0]]}, 
                 'is_open':False}
        return DefaultASH


def gen_case_when_list(wait_class_list, wait_column):
    case_when_template = "ROUND(100.0 * sum(case when {} = '{}' then 1 else 0 end)/max(v.cnt), 2)"
    case_when_list = [case_when_template.format(wait_column, wait) for wait in wait_class_list]
    case_when_list_str = (',').join(case_when_list)
    return case_when_list_str


Wait_Class = {'oracle':[
  'ON CPU',
  'Other',
  'Application',
  'Configuration',
  'Cluster',
  'Administrative',
  'Concurrency',
  'Commit',
  'Network',
  'User I/O',
  'System I/O',
  'Scheduler',
  'Queueing'], 
 'mysql':[
  'Optimization',
  'Tmp Table',
  'Table Operation',
  'Sort',
  'Update/Delete',
  'Lock',
  'Query Cache',
  'Network',
  'Master Thread',
  'I/O Thread',
  'SQL Thread',
  'Others'], 
 'sqlserver':[
  'RUNNING',
  'RUNNABLE',
  'SUSPENDED',
  'SLEEPING',
  'BACKGROUND',
  'ROLLBACK'], 
 'db2':[
  'BACKUP',
  'COMMIT_ACT',
  'COMP',
  'CONNECTPEND',
  'CREATE_DB',
  'DECOUPLED',
  'DISCONNECTPEND',
  'INTR',
  'IOERROR_WAIT',
  'LOAD',
  'LOCKWAIT',
  'QUIESCE_TABLESPACE',
  'RECOMP',
  'REMOTE_RQST',
  'RESTART',
  'RESTORE',
  'ROLLBACK_ACT',
  'ROLLBACK_TO_SAVEPOINT',
  'TEND',
  'THABRT',
  'THCOMT',
  'TPREP',
  'UNLOAD',
  'UOWEXEC',
  'WAITFOR_REMOTE']}
Wait_Class_Column = {'oracle':'wait_class', 
 'mysql':'wait_class', 
 'sqlserver':'status', 
 'db2':'appl_status'}
TABLE_HEADERS = {'oracle':[
  [
   '(%)', '', 'SQL_ID', 'SQL '],
  [
   '(%)', '', '', ''],
  [
   '(%)', '', 'SESSION_ID', '', ''],
  [
   '(%)', '', ''],
  [
   '(%)', '', ''],
  [
   '(%)', '', ''],
  [
   '(%)', '', ''],
  [
   '(%)', '', ''],
  [
   '(%)', '', ''],
  [
   '(%)', '', 'PLAN_HASH_VALUE', 'SQL_ID'],
  [
   '(%)', '', 'PLAN_ID', ''],
  [
   '(%)', '', 'SESSION_ID', '', '', '', 'ID(PHV)', '', '', '']], 
 'mysql':[
  [
   '(%)', '', 'SQL_ID', 'SQL '],
  [
   '(%)', '', '', ''],
  [
   '(%)', '', 'DB Name'],
  [
   '(%)', '', ''],
  [
   '(%)', '', ''],
  [
   '(%)', '', 'SESSION_ID', '', '']], 
 'sqlserver':[
  [
   '(%)', '', 'SQL_ID', 'SQL '],
  [
   '(%)', '', '', ''],
  [
   '(%)', '', 'DB Name'],
  [
   '(%)', '', ''],
  [
   '(%)', '', ''],
  [
   '(%)', '', ''],
  [
   '(%)', '', ''],
  [
   '(%)', '', 'SESSION_ID', '', '', '']], 
 'db2':[
  [
   '(%)', '', 'SQL_ID', 'SQL '],
  [
   '(%)', '', ''],
  [
   '(%)', '', 'DB Name'],
  [
   '(%)', '', ''],
  [
   '(%)', '', ''],
  [
   '(%)', '', 'Machine'],
  [
   '(%)', '', 'SESSION_ID', '', '', ''],
  [
   '(%)', '', 'SQL_ID', 'SQL_TEXT', 'SCHEMA']]}

def ash_dimension_data(pk, instance_id, sql_id, session_id, begin_time, end_time, dim):
    conn = Database.objects.get(pk=pk)
    case_when_str = gen_case_when_list(Wait_Class.get(conn.db_type), Wait_Class_Column.get(conn.db_type))
    if instance_id != None:
        if instance_id != 0:
            if conn.db_type == 'oracle':
                id_filter = ("database_id='{}' and inst_id={}").format(pk, instance_id)
            id_filter = ("database_id='{}'").format(pk)
        ash_name = {'oracle':'monitor_oracle_ash', 
         'mysql':'monitor_mysql_ash', 
         'sqlserver':'monitor_mssql_ash', 
         'db2':'monitor_db2_ash'}
        group_list = {'oracle':[
          "COALESCE(sql_id, 'null') sql_id,command",
          'event,wait_class',
          "sid || ','|| serial || '@' || inst_id as session_id, max(username) as username,max(PROGRAM) as program",
          'username',
          'machine',
          'program',
          'module',
          'action',
          'service_name',
          'sql_plan_hash_value,max(sql_id) as sql_id',
          'sql_plan_line_id line_id, sql_plan_operation operation',
          "sid || ','|| serial || '@' || inst_id, max(username) as username,max(PROGRAM) as PROGRAM,max(machine) as machine,max(sql_plan_hash_value) as sql_plan_hash_value, max(module) as module, max(action) as action, max(service_name) as service_name"], 
         'mysql':[
          'sql_id,command',
          'state,wait_class',
          'db_name',
          'username',
          'machine',
          'session_id,machine,username'], 
         'sqlserver':[
          'sql_id, command',
          'wait_type, status',
          'db_name',
          'username',
          'machine',
          'program',
          'wait_resource',
          'session_id,machine,username,program'], 
         'db2':[
          'sql_id,command',
          'appl_status',
          'db_name',
          'program',
          'username',
          "regexp_replace(machine, '\\.[^\\.]+.[0-9]+$', '', 'g')",
          'session_id,username,machine,program',
          'sql_id, sql_text, username']}
        group_by_list = {'oracle':[
          'sql_id,command',
          'event,wait_class',
          'inst_id,sid,serial',
          'username',
          'machine',
          'program',
          'module',
          'action',
          'service_name',
          'sql_plan_hash_value',
          'sql_plan_line_id,sql_plan_operation',
          'inst_id,sid,serial'], 
         'mysql':[
          'sql_id,command',
          'state,wait_class',
          'db_name',
          'username',
          'machine',
          'session_id,machine,username'], 
         'sqlserver':[
          'sql_id, command',
          'wait_type, status',
          'db_name',
          'username',
          'machine',
          'program',
          'wait_resource',
          'session_id,machine,username,program'], 
         'db2':[
          'sql_id,command',
          'appl_status',
          'db_name',
          'program',
          'username',
          "regexp_replace(machine, '\\.[^\\.]+.[0-9]+$', '', 'g')",
          'session_id,username,machine,program',
          'sql_id, sql_text, username']}
        group_list_str = group_list.get(conn.db_type)[dim]
        group_by_list_str = group_by_list.get(conn.db_type)[dim]
        sql_id_filter = get_sql_id_filter_str(conn.db_type, sql_id, session_id) if sql_id or session_id else ''
        data = {'ash_name':ash_name.get(conn.db_type), 
         'id_filter':id_filter, 
         'start_time':begin_time, 
         'end_time':end_time, 
         'group_list':group_list_str, 
         'group_by_list':group_by_list_str, 
         'wait_class_list':case_when_str, 
         'sql_id_filter':sql_id_filter}
        return (
         data, Wait_Class.get(conn.db_type), TABLE_HEADERS.get(conn.db_type)[dim])


ASH_CHAIN_QUERY = {'oracle': "\nwith recursive tree as (\n  select created_at, sid, serial, blocking_session, blocking_session_serial, username, program, CASE WHEN session_type = 'BACKGROUND' OR program ~ '.*\\([PJ]\\d+\\)' THEN\n              REGEXP_REPLACE(substring(program from position('(' in program)), '\\d', 'n')\n            ELSE\n                '('||REGEXP_REPLACE(REGEXP_REPLACE(program, '(.*)@(.*)(\\(.*\\))', '\x01'), '\\d', 'n')||')'\n            END || ' ' ||  event as event\n  from monitor_oracle_ash\n  where created_at BETWEEN to_timestamp({begin_time}) and to_timestamp({end_time})\n  and database_id = '{pk}' {inst_id_pred}\n  union all\n  select\n  c.created_at, c.sid, c.serial, c.blocking_session, c.blocking_session_serial, c.username, c.program, p.event||' -> '|| CASE WHEN c.session_type = 'BACKGROUND' OR c.program ~ '.*\\([PJ]\\d+\\)' THEN\n              REGEXP_REPLACE(substring(c.program from position('(' in c.program)), '\\d', 'n')\n            ELSE\n                '('||REGEXP_REPLACE(REGEXP_REPLACE(c.program, '(.*)@(.*)(\\(.*\\))', '\x01'), '\\d', 'n')||')'\n            END || ' ' ||  c.event as event\n  from monitor_oracle_ash c\n  join tree p\n  on p.blocking_session = c.sid\n  and p.blocking_session_serial = c.serial\n  and p.created_at = c.created_at\n  where c.created_at BETWEEN to_timestamp({begin_time}) and to_timestamp({end_time})\n  and c.database_id = '{pk}' {inst_id_pred}\n),\nv as (\n  select count(*) count\n  from monitor_oracle_ash\n  where created_at BETWEEN to_timestamp({begin_time}) and to_timestamp({end_time})\n  and database_id = '{pk}' {inst_id_pred}\n)\n,tree2 as (\n  select\n  c.*,\n  not exists(select p.* from tree p where p.created_at = c.created_at\n                                            and p.sid = c.blocking_session\n                                            and p.serial = c.blocking_session_serial) as is_leaf,\n  not exists(select p.* from tree p where p.created_at = c.created_at\n                                            and p.sid = c.sid\n                                            and p.serial = c.serial\n                                            and length(p.event) > length(c.event)) as no_dup_leaf\n  from tree c\n)\nselect count(*) * 10 as seconds, round(100.0*count(*)/v.count) activity_pct, username, event\nfrom tree2, v\nwhere (is_leaf = true and no_dup_leaf = true)\ngroup by username, event, v.count\norder by count(*) desc"}
Activity_Table_Name = {'mysql':'monitor_mysql_ash', 
 'db2':'monitor_db2_ash', 
 'sqlserver':'monitor_mssql_ash'}
# okay decompiling ./restful/hawkeye/api/enum/activity_enum.pyc
