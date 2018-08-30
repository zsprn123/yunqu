# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/celery/oracle/warn.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 6168 bytes
from monitor.models import Performance
from api.v1.monitor.services.runsqlService import run_sql
from datetime import datetime
from api.v1.alarm.services.warnService import customized_warn_scanner
from alarm.enum.alarm_warn_enum import WARN_ENUM
from common.util import build_exception_from_java

def diskgroup_warn(database):
    query = '\n        SELECT\n            NAME,\n            STATE,\n            round(TOTAL_MB/1024) TOTAL_GB,\n            round((TOTAL_MB-FREE_MB)/1024) USED_GB,\n            round((TOTAL_MB-FREE_MB)/TOTAL_MB*100) USED_PCT,\n            OFFLINE_DISKS\n        FROM\n            V$ASM_DISKGROUP'
    flag, json_data = run_sql(database, query)
    if not flag:
        print(str(build_exception_from_java(json_data)))
        return json_data
    created_at = datetime.now().replace(microsecond=0)
    warn = WARN_ENUM.get(database.db_type).DiskGroup_Offline_Disks_Warn
    for x in json_data:
        options = {'name': x.get('NAME')}
        p = Performance(inst_id=database.db_name, name=warn.name, value=x.get('OFFLINE_DISKS'), created_at=created_at)
        customized_warn_scanner(warn, p, database, False, options)

    warn = WARN_ENUM.get(database.db_type).DiskGroup_Status_Warn
    for x in json_data:
        options = {'name': x.get('NAME')}
        p = Performance(inst_id=database.db_name, name=warn.name, value=x.get('STATE'), created_at=created_at)
        customized_warn_scanner(warn, p, database, False, options)

    warn = WARN_ENUM.get(database.db_type).DiskGroup_Used_Percent_Warn
    for x in json_data:
        options = {'name':x.get('NAME'),  'total':x.get('TOTAL_GB'), 
         'used':x.get('USED_GB'), 
         'used_pct':x.get('USED_PCT')}
        p = Performance(inst_id=database.db_name, name=warn.name, value=x.get('STATE'), created_at=created_at)
        customized_warn_scanner(warn, p, database, False, options)


def oracle_standby_warn(database):
    query = "\nSELECT a.thread#,  b.last_seq, a.applied_seq, a. last_app_timestamp, b.last_seq-a.applied_seq ARC_DIFF, dest_name\nFROM\n        (SELECT  thread#, dest_name, MAX(sequence#) applied_seq, MAX(next_time) last_app_timestamp\n        FROM    gv$archived_log log,\n                v$ARCHIVE_DEST dest WHERE log.applied = 'YES' and dest.dest_name is not null and log.dest_id = dest.dest_id GROUP BY dest.dest_name, thread#) a,\n        (SELECT  thread#, MAX (sequence#) last_seq FROM gv$archived_log GROUP BY thread#) b\nWHERE a.thread# = b.thread#"
    flag, json_data = run_sql(database, query)
    if not flag:
        print(str(build_exception_from_java(json_data)))
        return json_data
    created_at = datetime.now().replace(microsecond=0)
    warn = WARN_ENUM.get(database.db_type).Standby_Gap_Warn
    for x in json_data:
        options = {'name':x.get('DEST_NAME'),  'applied_seq':x.get('APPLIED_SEQ'), 
         'max_seq':x.get('LAST_SEQ'), 
         'thread':x.get('THREAD#')}
        p = Performance(inst_id=database.db_name, name=warn.name, value=x.get('ARC_DIFF'), created_at=created_at)
        customized_warn_scanner(warn, p, database, False, options)


def plan_change_warn(database):
    query = '\nselect sql_id,\n      round(max(elapsed_time/decode(executions,0,1,executions))/min(elapsed_time/decode(executions,0,1,executions))) DIFF,\n      min(inst_id) INST_ID\nfrom\n  gv$sql\nwhere elapsed_time > 0\ngroup by sql_id\nhaving count(distinct plan_hash_value) > 1'
    flag, json_data = run_sql(database, query)
    if not flag:
        print(str(build_exception_from_java(json_data)))
        return json_data
    created_at = datetime.now().replace(microsecond=0)
    warn = WARN_ENUM.get(database.db_type).Plan_Change_Warn
    for x in json_data:
        options = {'sql_id': x.get('SQL_ID')}
        p = Performance(inst_id=x.get('INST_ID'), name=warn.name, value=x.get('DIFF'), created_at=created_at)
        customized_warn_scanner(warn, p, database, True, options)


def object_change_warn(database):
    query = "\nselect object_name,owner, to_char(last_ddl_time, 'yyyy-mm-dd hh24:mi:ss') last_ddl_time\nfrom dba_objects\nwhere last_ddl_time > sysdate - 1/24\nand owner not in ('SCOTT','MGMT_VIEW','MDDATA','MDSYS','SI_INFORMTN_SCHEMA','ORDPLUGINS','ORDSYS','OLAPSYS','SYSMAN','ANONYMOUS','XDB','CTXSYS','EXFSYS','WMSYS','ORACLE_OCM','DBSNMP','TSMSYS','DMSYS','DIP','OUTLN','SYSTEM','SYS') "
    flag, json_data = run_sql(database, query)
    if not flag:
        print(str(build_exception_from_java(json_data)))
        return json_data
    created_at = datetime.now().replace(microsecond=0)
    warn = WARN_ENUM.get(database.db_type).DB_Object_Change_Warn
    for x in json_data:
        options = {'schema':x.get('OWNER'),  'object_name':x.get('OBJECT_NAME'), 
         'last_ddl_time':x.get('LAST_DDL_TIME')}
        p = Performance(inst_id=database.db_name, name=warn.name, value=1, created_at=created_at)
        customized_warn_scanner(warn, p, database, True, options)


def job_failure_warn(database):
    query = "\n    select SCHEMA_USER OWNER, job || ' '|| what JOB_NAME, failures from dba_jobs where failures > 0\nunion all\nselect OWNER, JOB_NAME, count(*)\nFROM dba_scheduler_job_log\nwhere\nlog_date > sysdate - 1/24 and\nSTATUS != 'SUCCEEDED'\ngroup by OWNER, job_name"
    flag, json_data = run_sql(database, query)
    if not flag:
        print(str(build_exception_from_java(json_data)))
        return json_data
    created_at = datetime.now().replace(microsecond=0)
    warn = WARN_ENUM.get(database.db_type).Job_Warn
    for x in json_data:
        options = {'name':x.get('JOB_NAME'),  'schema':x.get('OWNER')}
        p = Performance(inst_id=database.db_name, name=warn.name, value=x.get('FAILURES'), created_at=created_at)
        customized_warn_scanner(warn, p, database, True, options)
# okay decompiling ./restful/hawkeye/api/celery/oracle/warn.pyc
