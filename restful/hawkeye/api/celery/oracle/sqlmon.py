# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/celery/oracle/sqlmon.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 4725 bytes
from monitor.models import SQLMON, SQLMON_Plan
from api.v1.monitor.services.runsqlService import run_sql
from datetime import datetime
from common.util import build_exception_from_java

def get_sqlmon(database):
    query_sqlmon = ("\n    select a.*,dbms_sqltune.report_sql_monitor(type=>'{}', sql_id=>a.sql_id, sql_exec_id=>a.sql_exec_id, report_level=>'ALL') SQLMON\n    from (select\n               KEY, STATUS,SQL_ID,round((LAST_REFRESH_TIME-SQL_EXEC_START)*24*3600) ELAPSED_TIME,\n               round(ELAPSED_TIME/1e6) DB_TIME,round(CPU_TIME/1e6) DB_CPU,\n               SQL_EXEC_ID,to_char(sql_exec_start,'YYYY-MM-DD HH24:MI:SS') SQL_EXEC_START,\n               SQL_PLAN_HASH_VALUE,INST_ID, USERNAME,\n               SQL_TEXT\n           from Gv$sql_Monitor\n           where --(LAST_REFRESH_TIME-SQL_EXEC_START)*24*3600>60\n           sql_plan_hash_value >0 and\n           status like 'DONE%'\n           and LAST_REFRESH_TIME>=sysdate - 600/3600/24\n           and LAST_REFRESH_TIME<=sysdate\n           and sql_text is not null\n           order by elapsed_time desc\n          ) a where rownum<={} ").format(database.sqlmon_format, database.num_sqlmon_per_minute)
    query_sqlmon_plan = "select\n    INST_ID,\n    STATUS,\n    to_char(FIRST_REFRESH_TIME,'YYYY-MM-DD HH24:MI:SS') FIRST_REFRESH_TIME,\n    to_char(LAST_REFRESH_TIME,'YYYY-MM-DD HH24:MI:SS') LAST_REFRESH_TIME,\n    SID,\n    SQL_ID,\n    to_char(SQL_EXEC_START,'YYYY-MM-DD HH24:MI:SS') SQL_EXEC_START,\n    SQL_EXEC_ID,\n    SQL_PLAN_HASH_VALUE,\n    PLAN_PARENT_ID,\n    PLAN_LINE_ID,\n    PLAN_OPERATION,\n    PLAN_OPTIONS,\n    PLAN_OBJECT_OWNER,\n    PLAN_OBJECT_NAME,\n    PLAN_OBJECT_TYPE,\n    PLAN_DEPTH,\n    PLAN_POSITION,\n    PLAN_COST,\n    PLAN_CARDINALITY,\n    PLAN_TEMP_SPACE,\n    STARTS,\n    OUTPUT_ROWS,\n    PHYSICAL_READ_REQUESTS,\n    PHYSICAL_READ_BYTES,\n    PHYSICAL_WRITE_REQUESTS,\n    PHYSICAL_WRITE_BYTES\nfrom gv$sql_plan_monitor\nwhere\n    key in ({})"
    flag, sqlmon_data = run_sql(database, query_sqlmon)
    if not flag:
        print(str(build_exception_from_java(sqlmon_data)))
        return sqlmon_data
    sqlmon_time = datetime.now().replace(microsecond=0)
    for x in sqlmon_data:
        m = SQLMON()
        m.inst_id = x.get('INST_ID')
        m.sql_id = x.get('SQL_ID')
        m.status = x.get('STATUS')
        m.username = x.get('USERNAME')
        m.elapsed_time = x.get('ELAPSED_TIME')
        m.db_time = x.get('DB_TIME')
        m.db_cpu = x.get('DB_CPU')
        m.sql_exec_id = x.get('SQL_EXEC_ID')
        m.sql_exec_start = x.get('SQL_EXEC_START')
        m.sql_plan_hash_value = x.get('SQL_PLAN_HASH_VALUE')
        m.sql_text = x.get('SQL_TEXT')
        m.sqlmon = x.get('SQLMON')
        m.database = database
        m.created_at = sqlmon_time
        m.save()
# okay decompiling ./restful/hawkeye/api/celery/oracle/sqlmon.pyc
