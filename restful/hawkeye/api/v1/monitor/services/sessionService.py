# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/monitor/services/sessionService.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 12065 bytes
from django.core.exceptions import ObjectDoesNotExist
from api.v1.monitor.services.runsqlService import run_batch_sql, run_sql
from monitor.models import Database, Session
from common.util import execute_return_json, build_exception_from_java
from api.v1.monitor.services.activityService import get_database_activity
from api.v1.monitor.services.sessiondetail.oracleSession import Detai_Query, Detai_Query_Without_IP, Old_Cursor_Query, New_Cursor_Query
from datetime import datetime

def get_default_detail_format():
    return {'detail':{u'\u8fde\u63a5\u4fe1\u606f':{'message': ''}, 
      u'\u5ba2\u6237\u7aef\u4fe1\u606f':{},  u'\u5e94\u7528\u4fe1\u606f':{},  u'\u7b49\u5f85\u4fe1\u606f':{},  u'\u963b\u585e\u4f1a\u8bdd':{},  u'\u4e8b\u52a1\u4fe1\u606f':{}}, 
     'cursor':[],  'top_activity':{},  'dim':0, 
     'instance_id':None}


def get_oracle_session_detail(database, session_id):
    detail_format = get_default_detail_format()
    import re
    prog = re.compile('([0-9]+),([0-9]+)@([0-9]+)')
    m = prog.search(session_id)
    sid, serial, inst_id = (1, 2, 3)
    if m:
        sid, serial, inst_id = m.group(1), m.group(2), m.group(3)
    detail_format['instance_id'] = inst_id
    options = {'inst_id':inst_id, 
     'sid':sid, 
     'serial':serial}
    detai_query = Detai_Query.format(**options)
    cursur_query = Old_Cursor_Query.format(**options)
    query = {'detail':detai_query, 
     'cursor':cursur_query}
    flag, json_data = run_batch_sql(database, query)
    if not flag:
        raise build_exception_from_java(json_data)
    detail_data = json_data.get('detail')
    cursor_data = json_data.get('cursor')
    if detail_data == None:
        detai_query = Detai_Query_Without_IP.format(**options)
        flag, json_data = run_sql(database, detai_query)
        if not flag:
            raise build_exception_from_java(json_data)
        detail_data = json_data
    if detail_data:
        detail_data = detail_data[0]
        detail_info = {u'\u8fde\u63a5\u4fe1\u606f':{x:detail_data[x] for x in ('SID', 'SERIAL#', 'STATUS', 'USERNAME', 'SPID', 'LOGON_TIME',
                            'SERVER') if x in detail_data}, 
         u'\u5ba2\u6237\u7aef\u4fe1\u606f':{x:detail_data[x] for x in ('OSUSER', 'PROCESS', 'MACHINE', 'IP') if x in detail_data}, 
         u'\u5e94\u7528\u4fe1\u606f':{x:detail_data[x] for x in ('SQL_ID', 'PREV_SQL_ID', 'LAST_CALL_ET', 'PROGRAM', 'MODULE',
                            'ACTION', 'SERVICE_NAME') if x in detail_data}, 
         u'\u7b49\u5f85\u4fe1\u606f':{x:detail_data[x] for x in ('EVENT', 'WAIT_CLASS', 'P1', 'P2', 'P3') if x in detail_data}, 
         u'\u963b\u585e\u4f1a\u8bdd':{x:detail_data[x] for x in ('BLOCKING_INSTANCE', 'BLOCKING_SESSION') if x in detail_data}, 
         u'\u4e8b\u52a1\u4fe1\u606f':{x:detail_data[x] for x in ('XIDUSN', 'XIDSLOT', 'XIDSQN', 'TRX_STARTED', 'USED_UBLK',
                            'USED_UREC') if x in detail_data}}
        detail_format['detail'] = detail_info
        detail_format['cursor'] = cursor_data
    return detail_format


def get_mysql_session_detail(database, session_id):
    detail_format = get_default_detail_format()
    detai_query = f'''SELECT * FROM
    information_schema.processlist
    WHERE id = {session_id}'''
    flag, json_data = run_sql(database, detai_query)
    if not flag:
        raise build_exception_from_java(json_data)
    if json_data:
        detail_format['detail'][''] = json_data[0]
    return detail_format


def get_db2_session_detail(database, session_id):
    detail_format = get_default_detail_format()
    detai_query = f'''select agent_id, db_name, appl_name, authid, appl_id,
  appl_status,client_prdid, client_pid, client_platform,client_protocol, client_nname
  FROM SYSIBMADM.APPLICATIONS
  WHERE agent_id = {session_id}'''
    flag, json_data = run_sql(database, detai_query)
    if not flag:
        raise build_exception_from_java(json_data)
    if json_data:
        detail_data = json_data[0]
        detail_info = {u'\u8fde\u63a5\u4fe1\u606f':{x:detail_data[x] for x in detail_data if 'CLIENT' in x}, 
         u'\u5ba2\u6237\u7aef\u4fe1\u606f':{x:detail_data[x] for x in detail_data if 'CLIENT' not in x}}
        detail_format['detail'] = detail_info
    return detail_format


def get_sqlserver_session_detail(database, session_id):
    detail_format = get_default_detail_format()
    detai_query = f'''SELECT
            ses.SESSION_ID,
            (select name from main..sysdatabases where dbid = req.database_id) DB_NAME,
            --client info
            ses.LOGIN_NAME,
            CONVERT(VARCHAR(24), ses.LOGIN_TIME, 120) LOGON_TIME,
            ses.HOST_NAME,
            ses.PROGRAM_NAME,
            ses.HOST_PROCESS_ID,
            ses.CLIENT_VERSION,
            ses.CLIENT_INTERFACE_NAME,
            ses.NT_DOMAIN,
            ses.NT_USER_NAME,
            --application
            ses.status STATUS,
            convert(bigint, ses.total_elapsed_time/1000000) ELAPSED_TIME,
            convert(bigint, ses.cpu_time/1000000) CPU_TIME,
            convert(bigint, ses.total_scheduled_time/1000000) SCHEDULED_TIME,
            ses.MEMORY_USAGE,
            ses.LOGICAL_READS,
            ses.READS,
            ses.WRITES,
            ses.ROW_COUNT,
            --current request
            req.STATUS REQ_STATUS,
            CONVERT(VARCHAR(24), req.start_time, 120) START_TIME,
            sqltext.TEXT SQL_TEXT,
            req.COMMAND,
            req.TRANSACTION_ID,
            req.BLOCKING_SESSION_ID B_BLOCKER,
            req.WAIT_TYPE,
            convert(bigint, req.wait_time/1000000) WAIT_TIME,
            req.WAIT_RESOURCE,
            convert(bigint, req.total_elapsed_time/1000000) ELAPSED_TIME,
            req.ROW_COUNT REQ_ROW_COUNT,
            con.CLIENT_NET_ADDRESS,
            substring(sys.fn_sqlvarbasetostr(req.sql_handle),3,1000) SQL_ID
        FROM sys.dm_exec_sessions ses
        inner join sys.dm_exec_connections con on ses.session_id = con.session_id
        left join sys.dm_exec_requests req on req.session_id = ses.session_id
        outer APPLY sys.dm_exec_sql_text(sql_handle) AS sqltext
        where ses.session_id = {session_id}'''
    flag, json_data = run_sql(database, detai_query)
    if not flag:
        raise build_exception_from_java(json_data)
    if json_data:
        detail_data = json_data[0]
        detail_info = {u'\u8fde\u63a5\u4fe1\u606f':{x:detail_data[x] for x in ('SESSION_ID', 'DB_NAME', 'STATUS', 'LOGIN_NAME', 'LOGON_TIME') if x in detail_data}, 
         u'\u5ba2\u6237\u7aef\u4fe1\u606f':{x:detail_data[x] for x in ('HOST_NAME', 'CLIENT_NET_ADDRESS', 'PROGRAM_NAME', 'HOST_PROCESS_ID',
                            'CLIENT_VERSION', 'CLIENT_INTERFACE_NAME', 'NT_DOMAIN',
                            'NT_USER_NAME') if x in detail_data}, 
         u'\u5e94\u7528\u4fe1\u606f':{x:detail_data[x] for x in ('ELAPSED_TIME', 'CPU_TIME', 'SCHEDULED_TIME', 'MEMORY_USAGE',
                            'LOGICAL_READS', 'READS', 'WRITES', 'ROW_COUNT') if x in detail_data}, 
         u'\u7b49\u5f85\u4fe1\u606f':{x:detail_data[x] for x in ('COMMAND', 'REQ_STATUS', 'START_TIME', 'SQL_TEXT', 'SQL_ID',
                            'ELAPSED_TIME') if x in detail_data}, 
         u'\u963b\u585e\u4f1a\u8bdd':{x:detail_data[x] for x in ('B_BLOCKER', 'WAIT_TIME', 'WAIT_RESOURCE', 'WAIT_TYPE') if x in detail_data}, 
         u'\u4e8b\u52a1\u4fe1\u606f':{x:detail_data[x] for x in ('TRANSACTION_ID', ) if x in detail_data}}
        detail_format['detail'] = detail_info
    return detail_format


def session_detail(pk, session_id, time_span='realtime'):
    database = Database.objects.get(pk=pk)
    db_type = database.db_type
    if time_span == 'realtime':
        try:
            if db_type == 'oracle':
                detail_format = get_oracle_session_detail(database, session_id)
            else:
                if db_type == 'mysql':
                    detail_format = get_mysql_session_detail(database, session_id)
                else:
                    if db_type == 'db2':
                        detail_format = get_db2_session_detail(database, session_id)
                    else:
                        if db_type == 'sqlserver':
                            detail_format = get_sqlserver_session_detail(database, session_id)
                    activity_data = get_database_activity(pk, 'realtime', instance_id=detail_format.get('instance_id'), session_id=session_id)
                    top_activity = activity_data.get(database.db_name) or activity_data.get(database.alias)
                    detail_format['top_activity'] = top_activity.get('data')
            return detail_format
        except ObjectDoesNotExist:
            return {'error_message': ''}
        except Exception as err:
            return {'error_message': str(err)}

    else:
        session = (((Session.objects.filter(database=database)).filter(session_id=str(session_id))).filter(created_at=datetime.fromtimestamp(time_span))).first()
        if session:
            return session.detail
        return get_default_detail_format()


def session_history(pk, session_id=None, begin_time=None, end_time=None):
    try:
        database = Database.objects.get(pk=pk)
        query = f'''
        select
    extract(epoch from created_at)*1000 CREATED_AT,
    count(*) SESSION_COUNT
from
    monitor_session
where database_id = '{pk}' and session_id = '{session_id}' and
    created_at between to_timestamp({begin_time}) and to_timestamp({end_time})
group by
    created_at
order by created_at'''
        result = execute_return_json(query)
        data = []
        for x in result:
            data.append([x.get('CREATED_AT'), x.get('SESSION_COUNT')])

        return data
    except ObjectDoesNotExist:
        return {'error_message': ''}
    except Exception as err:
        return {'error_message': str(err)}


def all_sessions(pk):
    query = {'oracle':"\n                  select\n                s.sid || ',' || s.serial# || '@' || s.inst_id session_id,\n                s.username,\n                s.status,\n                s.sql_id,\n                case when s.state = 'WAITING' then s.event else 'ON CPU' end event,\n                machine,\n                s.program,\n                to_char(s.logon_time,'YYYY-MON-DD HH24:MI') logon_time,\n                round(Value / 1024 / 1024,1) PGA_MB\n            from\n                gv$session s, V$sesstat St, V$statname Sn\n                 Where St.Sid = s.Sid\n   And St.Statistic# = Sn.Statistic#\n   And Sn.Name Like 'session pga memory'", 
     'mysql':'\n        SELECT * FROM\n    information_schema.processlist', 
     'db2':'select agent_id, db_name, appl_name, authid, appl_id,\n  appl_status, client_nname MACHINE\n  FROM SYSIBMADM.APPLICATIONS', 
     'sqlserver':'\n        SELECT\n            ses.SESSION_ID,\n            (select name from main..sysdatabases where dbid = req.database_id) DB_NAME,\n            ses.LOGIN_NAME,\n            CONVERT(VARCHAR(24), ses.LOGIN_TIME, 120) LOGON_TIME,\n            ses.HOST_NAME,\n            ses.PROGRAM_NAME,\n            --application\n            ses.status STATUS,\n            --current request\n            req.STATUS REQ_STATUS,\n            CONVERT(VARCHAR(24), req.start_time, 120) START_TIME,\n            req.ROW_COUNT REQ_ROW_COUNT,\n            con.CLIENT_NET_ADDRESS,\n            substring(sys.fn_sqlvarbasetostr(req.sql_handle),3,1000) SQL_ID\n        FROM sys.dm_exec_sessions ses\n        inner join sys.dm_exec_connections con on ses.session_id = con.session_id\n        left join sys.dm_exec_requests req on req.session_id = ses.session_id\n        outer APPLY sys.dm_exec_sql_text(sql_handle) AS sqltext'}
    database = Database.objects.get(pk=pk)
    detail_query = query.get(database.db_type)
    flag, json_data = run_sql(database, detail_query)
    if not flag:
        raise build_exception_from_java(json_data)
    return json_data
# okay decompiling ./restful/hawkeye/api/v1/monitor/services/sessionService.pyc
