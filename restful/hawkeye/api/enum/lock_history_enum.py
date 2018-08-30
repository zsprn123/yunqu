# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/enum/lock_history_enum.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 15385 bytes
from enum import Enum
from api.enum.transaction_enum import Transaction_Query
from api.enum.database_enum import DatabaseType
from api.v1.monitor.services.runsqlService import run_sql
from common.util import build_exception_from_java
from monitor.models import Session
from datetime import datetime
from api.v1.monitor.services.sessionService import session_detail
import json

class Lock_History_Query(Enum):
    mysql = '\nSELECT distinct concat_ws(\':\', lock_table, lock_index, lock_space, lock_page, lock_rec) as B_RES,\nr.trx_id AS W_TRX_ID,\ncast(r.trx_mysql_thread_id as char) AS W_WAITER,\nTIMESTAMPDIFF(SECOND, r.trx_wait_started, CURRENT_TIMESTAMP) AS W_WAIT_TIME,\nr.trx_query AS W_SQL_TEXT,\nl.lock_table AS W_WAITING_TABLE_LOCK,\nb.trx_id AS B_TRX_ID,\ncast(b.trx_mysql_thread_id as char) AS B_BLOCKER,\nSUBSTRING(p.host, 1, INSTR(p.host, \':\') - 1) AS B_HOST,\nSUBSTRING(p.host, INSTR(p.host, \':\') +1) AS B_PORT,\nIF(p.command = "Sleep", p.time, 0) AS B_IDLE_IN_TRX,\nb.trx_query AS B_SQL_TEXT\nFROM INFORMATION_SCHEMA.INNODB_LOCK_WAITS AS w\nINNER JOIN INFORMATION_SCHEMA.INNODB_TRX AS b ON b.trx_id = w.blocking_trx_id\nINNER JOIN INFORMATION_SCHEMA.INNODB_TRX AS r ON r.trx_id = w.requesting_trx_id\nINNER JOIN INFORMATION_SCHEMA.INNODB_LOCKS AS l ON w.requested_lock_id = l.lock_id\nLEFT JOIN INFORMATION_SCHEMA.PROCESSLIST AS p ON p.id = b.trx_mysql_thread_id\nORDER BY W_WAIT_TIME DESC'
    oracle = "\nselect\n    b.type || '-' || b.id1 ||'-'|| b.id2 || case when b.type = 'TM' then (select '(' || owner || '.' || object_name || ')' from dba_objects where object_id = b.id1) else '' end as b_res,\n    s1.sid || ','|| s1.serial# || '@' || s1.inst_id as b_blocker,\n    (select count(*) from gv$lock t where t.type=b.type and t.id1 = b.id1 and t.id2 = b.id2 and request > 0) b_blocked_cnt,\n    b.request b_request,\n    b.lmode b_lmode,\n    s1.username b_username,\n    s1.sql_id b_sql_id,\n    s1.machine,\n    s1.program,\n    s1.module,\n    s1.service_name,\n--    (select SQL_TEXT from v$sql where sql_id = s1.sql_id and rownum = 1) b_sqltext,\n    s1.prev_sql_id b_prev_sql_id,\n--    (select SQL_TEXT from v$sql where sql_id = s1.prev_sql_id and rownum = 1) b_prev_sqltext,\n    b.ctime as b_ctime,\n    s2.sid || ','|| s2.serial# || '@' || s2.inst_id as w_waiter,\n    w.request w_request,\n    w.lmode w_lmode,\n    s2.username w_username,\n    s2.sql_id w_sql_id,\n--    (select SQL_TEXT from v$sql where sql_id = s2.sql_id and rownum = 1) w_sqltext,\n    s2.prev_sql_id w_prev_sql_id,\n--    (select SQL_TEXT from v$sql where sql_id = s2.prev_sql_id and rownum = 1) w_prev_sqltext,\n    w.ctime as w_ctime\nfrom\n    gv$lock b,\n    gv$lock w,\n    gv$session s1,\n    gv$session s2\nwhere\n    b.block > 0\nand w.request > 0\nand b.id1 = w.id1\nand b.id2 = w.id2\nand b.type = w.type\nand b.inst_id = s1.inst_id\nand b.sid = s1.sid\nand w.inst_id = s2.inst_id\nand w.sid = s2.sid\norder by\n    b_res,\n    w_ctime desc"
    db2 = '\nselect\n    l.lock_name B_RES,\n    lock_object_type LOCK_OBJECT_TYPE,\n    lock_wait_elapsed_time LOCK_WAIT_ELAPSED_TIME,\n    tabschema OWNER,\n    tabname TABLE_NAME,\n    lock_current_mode LOCK_CURRENT_MODE,\n    lock_mode_requested LOCK_MODE_REQUESTED,\n    cast(req_application_handle as varchar(100)) W_WAITER,\n    req_agent_tid REQ_AGENT_TID,\n    --req_member REQ_MEMBER,\n    req_application_name REQ_APPLICATION_NAME,\n    req_userid REQ_USERID,\n    req_stmt_text W_SQL_TEXT,\n    (select max(hex(p.EXECUTABLE_ID)) FROM table(mon_get_pkg_cache_stmt(NULL, NULL, NULL, -2)) as p where p.stmt_text = req_stmt_text) W_SQL_ID,\n    case when hld_application_handle is null then (select cast(lh.agent_id as varchar(100)) from SYSIBMADM.LOCKS_HELD lh where lh.lock_name = l.lock_name ) else cast(hld_application_handle as varchar(100)) end B_BLOCKER,\n    --hld_member HLD_MEMBER,\n    hld_application_name HLD_APPLICATION_NAME,\n    hld_userid HLD_USERID,\n    hld_current_stmt_text B_SQL_TEXT,\n    (select max(hex(p.EXECUTABLE_ID)) FROM table(mon_get_pkg_cache_stmt(NULL, NULL, NULL, -2)) as p where p.stmt_text = hld_current_stmt_text) B_SQL_ID\nfrom\n    sysibmadm.mon_lockwaits l'
    sqlserver = "\nWITH [Blocking]\nAS (SELECT w.[session_id]\n--           ,s.[original_login_name]\n   ,s.[login_name]\n   ,w.[wait_duration_ms]\n   ,w.[wait_type]\n   ,r.[status]\n   ,r.[wait_resource]\n   ,w.[resource_description]\n   ,s.[program_name]\n   ,w.[blocking_session_id]\n   ,s.[host_name]\n   ,r.[command]\n   ,r.[percent_complete]\n   ,r.[cpu_time]\n   ,r.[total_elapsed_time]\n   ,r.[reads]\n   ,r.[writes]\n   ,r.[logical_reads]\n   ,r.[row_count]\n   ,substring(sys.fn_sqlvarbasetostr(r.sql_handle),3,1000) sql_handle\n   ,q.text text\nFROM [sys].[dm_os_waiting_tasks] w\nINNER JOIN [sys].[dm_exec_sessions] s ON w.[session_id] = s.[session_id]\nINNER JOIN [sys].[dm_exec_requests] r ON s.[session_id] = r.[session_id]\nCROSS APPLY [sys].[dm_exec_sql_text](r.[plan_handle]) q\nWHERE w.[session_id] > 50\nAND w.[wait_type] NOT IN ('DBMIRROR_DBM_EVENT' ,'ASYNC_NETWORK_IO')\nAND w.[blocking_session_id] > 0)\nSELECT\n    CONVERT(varchar(100), b.[blocking_session_id]) AS [B_BLOCKER]\n    ,s1.[login_name] AS [B_LOGIN_NAME]\n    ,UPPER(s1.[status]) AS [B_STATUS]\n    ,q1.text as [B_SQL_TEXT]\n    ,substring(sys.fn_sqlvarbasetostr(c1.most_recent_sql_handle),3,1000) B_SQL_ID\n    ,CONVERT(varchar(100), b.[session_id]) AS [W_WAITER]\n    ,b.[login_name] AS [W_LOGIN_NAME]\n    ,UPPER(b.[status]) AS [W_STATUS]\n    ,b.[wait_duration_ms]/1000 AS [W_WAITDURATION]\n    ,b.[wait_type] AS [W_WAITTYPE]\n    ,t.[request_mode] AS [W_WAITREQUESTMODE]\n    ,b.[wait_resource] AS [B_RES]\n    ,t.[resource_type] AS [W_WAITRESOURCETYPE]\n    ,DB_NAME(t.[resource_database_id]) AS [W_WAITRESOURCEDATABASENAME]\n    ,b.[text] AS [W_SQL_TEXT]\n    ,b.[sql_handle] as [W_SQL_ID]\nFROM [Blocking] b\nINNER JOIN [sys].[dm_exec_sessions] s1\nON b.[blocking_session_id] = s1.[session_id]\nINNER JOIN [sys].[dm_exec_connections] c1\nON s1.[session_id] = c1.[session_id]\nINNER JOIN [sys].[dm_tran_locks] t\nON t.[request_session_id] = b.[session_id]\nCROSS APPLY [sys].[dm_exec_sql_text](c1.[most_recent_sql_handle]) q1\nWHERE t.[request_status] = 'WAIT'\nORDER BY b.[wait_duration_ms]"


class OLD_Lock_History_Query(Enum):
    db2 = '\n    select\n        lw.lock_name B_RES,\n        lw.LOCK_OBJECT_TYPE,\n        timestampdiff(2,char(lw.snapshot_timestamp - lw.lock_wait_start_time)) as "LOCK_WAIT_ELAPSED_TIME",\n        lw.tabschema as "OWNER",\n        lw.tabname as "TABLE_NAME",\n        lw.lock_mode,\n        lw.LOCK_MODE_REQUESTED,\n        case when ai_h.agent_id is null then (select cast(lh.agent_id as varchar(100)) from SYSIBMADM.LOCKS_HELD lh where lh.lock_name = lw.lock_name ) else cast(ai_h.agent_id as varchar(100)) end B_BLOCKER,\n        ai_h.appl_name as "HLD_APPLICATION_NAME",\n        ai_h.primary_auth_id as "HLD_USERID",\n        cast(ai_w.agent_id as varchar(100)) W_WAITER,\n        ai_w.appl_name as "REQ_APPLICATION_NAME",\n        ai_w.primary_auth_id as "REQ_USERID"\n    from\n        sysibmadm.snapappl_info ai_h,\n        sysibmadm.snapappl_info ai_w,\n        sysibmadm.snaplockwait lw\n    where lw.agent_id = ai_w.agent_id\n    and lw.agent_id_holding_lk = ai_h.agent_id'


class Lock_History_Local_Query(Enum):
    mysql = "\nselect distinct\n    b_res,\n    w_trx_id,\n    w_waiter,\n    w_wait_time,\n    w_waiting_query,\n    w_waiting_table_lock,\n    b_trx_id,\n    b_blocker,\n    b_host,\n    b_port,\n    b_idle_in_trx,\n    b_trx_query\nfrom\n    monitor_mysql_lock_history\nwhere database_id = '{}' and\n    created_at = to_timestamp({})"
    oracle = "\nselect distinct\n    B_RES,\n    B_BLOCKER,\n    B_BLOCKED_CNT,\n    B_REQUEST,\n    B_LMODE,\n    B_USERNAME,\n    B_SQL_ID,\n--    B_SQLTEXT,\n    B_PREV_SQL_ID,\n--    B_PREV_SQLTEXT,\n    B_CTIME,\n    W_WAITER,\n    W_REQUEST,\n    W_LMODE,\n    W_USERNAME,\n    W_SQL_ID,\n--    W_SQLTEXT,\n    W_PREV_SQL_ID,\n--    W_PREV_SQLTEXT,\n    W_CTIME\nfrom\n    monitor_oracle_lock_history\nwhere database_id = '{}' and\n    created_at = to_timestamp({})"
    db2 = "\nselect distinct\n    B_RES,\n    lock_object_type,\n    lock_wait_elapsed_time,\n    tabschema as OWNER,\n    tabname as TABLE_NAME,\n    data_partition_id,\n    lock_mode,\n    lock_current_mode,\n    lock_mode_requested,\n    w_waiter,\n    req_agent_tid,\n    req_member,\n    req_userid,\n    req_executable_id,\n    req_stmt_text,\n    b_blocker,\n    hld_member,\n    hld_userid,\n    hld_current_stmt_text,\n    hld_executable_id\nfrom\n    monitor_db2_lock_history\nwhere database_id = '{}' and\n    created_at = to_timestamp({})"
    sqlserver = "\nselect distinct\n    b_blocker,\n    b_login_name,\n    b_status,\n    b_text,\n    b_sql_handle,\n    w_waiter,\n    w_login_name,\n    w_status,\n    w_waitduration,\n    w_waittype,\n    w_waitrequestmode,\n    b_res,\n    w_waitresourcetype,\n    w_waitresourcedatabasename,\n    w_text,\n    w_sql_handle\nfrom\n    monitor_mssql_lock_history\nwhere database_id = '{}' and\n    created_at = to_timestamp({})"


class Lock_History_Count_Query(Enum):
    mysql = "\nselect\n    extract(epoch from created_at)*1000 created_at,\n    count(*) blocked_session_count\nfrom\n    monitor_mysql_lock_history\nwhere database_id = '{}' and\n    created_at between to_timestamp({}) and to_timestamp({})\ngroup by\n    created_at\norder by created_at"
    oracle = "\nselect\n    extract(epoch from created_at)*1000 created_at,\n    count(*) blocked_session_count\nfrom\n    monitor_oracle_lock_history\nwhere database_id = '{}' and\n    created_at between to_timestamp({}) and to_timestamp({})\ngroup by\n    created_at\norder by created_at"
    db2 = "\nselect\n    extract(epoch from created_at)*1000 created_at,\n    count(*) blocked_session_count\nfrom\n    monitor_db2_lock_history\nwhere database_id = '{}' and\n    created_at between to_timestamp({}) and to_timestamp({})\ngroup by\n    created_at\norder by created_at"
    sqlserver = "\nselect\n    extract(epoch from created_at)*1000 created_at,\n    count(*) blocked_session_count\nfrom\n    monitor_mssql_lock_history\nwhere database_id = '{}' and\n    created_at between to_timestamp({}) and to_timestamp({})\ngroup by\n    created_at\norder by created_at"


class Blocker_Header(Enum):
    oracle = [
     'B_RES', 'B_BLOCKER', 'B_BLOCKED_CNT', 'B_REQUEST', 'B_LMODE', 'B_USERNAME', 'B_SQL_ID',
     'B_PREV_SQL_ID', 'B_CTIME', 'MACHINE', 'PROGRAM', 'MODULE', 'SERVICE_NAME']
    db2 = ['B_RES', 'LOCK_OBJECT_TYPE', 'OWNER', 'TABLE_NAME', 'LOCK_CURRENT_MODE',
     'B_BLOCKER', 'HLD_USERID', 'B_SQL_TEXT', 'B_SQL_ID']
    mysql = [
     'B_RES', 'B_BLOCKER', 'B_TRX_ID', 'B_HOST', 'B_PORT',
     'B_IDLE_IN_TRX', 'B_TRX_QUERY']
    sqlserver = ['B_RES', 'B_BLOCKER', 'B_LOGIN_NAME', 'B_STATUS', 'B_SQL_TEXT', 'B_SQL_ID']


class Waiter_Header(Enum):
    oracle = [
     'W_WAITER', 'W_REQUEST', 'W_LMODE', 'W_USERNAME', 'W_SQL_ID', 'W_PREV_SQL_ID',
     'W_CTIME']
    db2 = ['LOCK_WAIT_ELAPSED_TIME', 'LOCK_MODE_REQUESTED', 'W_WAITER',
     'REQ_AGENT_TID', 'REQ_USERID', 'W_SQL_TEXT', 'W_SQL_ID']
    mysql = ['W_WAITER', 'W_WAIT_TIME', 'W_SQL_TEXT', 'W_WAITING_TABLE_LOCK']
    sqlserver = ['W_WAITER', 'W_LOGIN_NAME', 'W_STATUS', 'W_WAITDURATION', 'W_WAITTYPE', 'W_WAITREQUESTMODE',
     'W_WAITRESOURCETYPE', 'W_WAITRESOURCEDATABASENAME', 'W_SQL_TEXT', 'W_SQL_ID']


class UNLOCK_Session_Query(Enum):
    oracle = "select distinct 'ALTER SYSTEM DISCONNECT SESSION ''' || t2.sid ||','||t2.SERIAL# || ',@'||t2.INST_ID ||''' immediate;' CMD, t2.sid ||','||t2.SERIAL# || '@'||t2.INST_ID SESSION_ID from gv$session t1 , gv$session t2 where t1.final_blocking_instance  is not null and t1.final_blocking_instance = t2.inst_id and t1.final_blocking_session = t2.sid"
    db2 = "select DISTINCT 'force application (' || hld_application_handle || ')' CMD, hld_application_handle as SESSION_ID from sysibmadm.mon_lockwaits lock1\n              where not exists (select 1 from sysibmadm.mon_lockwaits lock2 where lock1.hld_application_handle = lock2.req_application_handle)"
    mysql = "SELECT distinct concat('kill ', trx.trx_mysql_thread_id, ';') as CMD, trx.trx_mysql_thread_id as SESSION_ID\nFROM information_schema.innodb_lock_waits lw\ninner join information_schema.innodb_trx trx on lw.blocking_trx_id = trx.trx_id\nwhere not exists (select 1 from information_schema.innodb_lock_waits lw2\nwhere lw.blocking_trx_id = lw2.requesting_trx_id)"
    sqlserver = "select 'kill ' +  convert(VARCHAR(100),w.[blocking_session_id]) CMD, w.[blocking_session_id] SESSION_ID\nFROM [sys].[dm_os_waiting_tasks] w\nWHERE w.[session_id] > 50\nAND w.[wait_type] NOT IN ('DBMIRROR_DBM_EVENT' ,'ASYNC_NETWORK_IO')\nAND w.[blocking_session_id] > 0\nand not exists (\n  select w.[blocking_session_id]\nFROM [sys].[dm_os_waiting_tasks] w2\nWHERE w2.[session_id] = w.[blocking_session_id]\nAND w2.[blocking_session_id] > 0\n)"


class OLD_UNLOCK_Session_Query(Enum):
    oracle = "select distinct 'ALTER SYSTEM DISCONNECT SESSION ''' || t2.sid ||','||t2.SERIAL# || ''' immediate;' CMD, t2.sid ||','||t2.SERIAL# || '@'||t2.INST_ID SESSION_ID from (select inst_id, sid from gv$lock where block > 0 and lmode > 3 and request =0 and type in ('TM','TX')) t1 , gv$session t2 where t1.inst_id = t2.inst_id and t1.sid = t2.sid order by 1"


class OLD_UNLOCK_Session_Query_RAC(Enum):
    oracle = "select distinct 'Instance ' || t2.inst_id || ': ALTER SYSTEM DISCONNECT SESSION ''' || t2.sid ||','||t2.SERIAL# || ''' immediate;' CMD, t2.sid ||','||t2.SERIAL# || '@'||t2.INST_ID SESSION_ID from (select inst_id, sid from gv$lock where block > 0 and lmode > 3 and request =0 and type in ('TM','TX')) t1 , gv$session t2 where t1.inst_id = t2.inst_id and t1.sid = t2.sid order by 1"


def get_lock_query(database):
    lock_query = Lock_History_Query[database.db_type].value
    if database.db_type == 'db2':
        if database.is_v95_base() or database.is_v97():
            lock_query = OLD_Lock_History_Query[database.db_type].value
    query = {'lock':lock_query,  'transaction':Transaction_Query[database.db_type].value}
    if database.db_type == 'mysql':
        query['tables'] = 'SHOW OPEN TABLES WHERE in_use>0'
    return query


def get_unlock_data(database):
    db_type = database.db_type
    query = ''
    if database.db_type == 'db2':
        if database.is_v95_base() or database.is_v97():
            return []
        if db_type == DatabaseType.ORACLE.value:
            if database.get_ora_version() > 10:
                query = UNLOCK_Session_Query[database.db_type].value
            elif database.instance_count > 1:
                query = OLD_UNLOCK_Session_Query_RAC[database.db_type].value
            else:
                query = OLD_UNLOCK_Session_Query[database.db_type].value
        else:
            query = UNLOCK_Session_Query[database.db_type].value
        flag, cmd_data = run_sql(database, query)
        if not flag:
            raise build_exception_from_java(cmd_data)
        else:
            return cmd_data


def get_blocking_session_detail(database):
    cmd_data = get_unlock_data(database)
    session_list = [x.get('SESSION_ID') for x in cmd_data]
    return session_list


def save_session_detail_list(database, session_list):
    created_at = datetime.now().replace(microsecond=0)
    for x in session_list:
        detail = session_detail(str(database.id), x)
        detail = json.loads(json.dumps(detail).replace('\\u0000', ''))
        session = Session(database=database, created_at=created_at, session_id=x, detail=detail)
        session.save()
# okay decompiling ./restful/hawkeye/api/enum/lock_history_enum.pyc
