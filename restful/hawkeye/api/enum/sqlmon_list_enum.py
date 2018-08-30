# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/enum/sqlmon_list_enum.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 1153 bytes
SQLMON_QUERY = {'realtime':"\n            select *\n            from (select  STATUS,SQL_ID,round((LAST_REFRESH_TIME-SQL_EXEC_START)*24*3600) ELAPSED_TIME,\n                           round(ELAPSED_TIME/1e6) DB_TIME,round(CPU_TIME/1e6) DB_CPU,\n                           SQL_EXEC_ID,to_char(sql_exec_start,'YYYY-MM-DD HH24:MI:SS') SQL_EXEC_START,\n                           SQL_PLAN_HASH_VALUE,INST_ID, USERNAME\n                         from gv$sql_monitor\n                   where sql_text is not null\n                   order by SQL_EXEC_START desc)", 
 'history':"\n                    select\n                    ID,\n                    STATUS,\n                    SQL_ID,\n                    ELAPSED_TIME,\n                    DB_TIME,\n                    DB_CPU,\n                    SQL_EXEC_ID,\n                    SQL_EXEC_START,\n                    SQL_PLAN_HASH_VALUE,\n                    INST_ID,\n                    USERNAME\n                    from monitor_sqlmon\n                    where created_at BETWEEN to_timestamp({begin_time}) and to_timestamp({end_time})\n                    and database_id = '{pk}'\n                "}
# okay decompiling ./restful/hawkeye/api/enum/sqlmon_list_enum.pyc
