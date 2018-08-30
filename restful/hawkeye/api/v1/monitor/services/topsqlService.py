# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/monitor/services/topsqlService.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 7136 bytes
from django.core.exceptions import ObjectDoesNotExist
from api.v1.monitor.services.runsqlService import run_sql
from monitor.models import Database
from common.util import build_exception_from_java

def get_topsql(database_id, _type, user=None, sqltext=None):
    try:
        database = Database.objects.get(pk=database_id)
        data = {}
        user_filter = ''
        sqltext_filter = ''
        filter_list = []
        sql_text_map = {'oracle':'sql_fulltext', 
         'db2':'stmt_text', 
         'sqlserver':'SQL_TEXT'}
        if user or sqltext:
            if user:
                if database.db_type == 'oracle':
                    filter_list.append(f'''parsing_schema_name = '{user}'''')
            if sqltext:
                filter_list.append(f'''{(sql_text_map.get(database.db_type))} like '%{sqltext}%'''')
        where_filter = (' and ').join(filter_list)
        if where_filter:
            where_filter = ' and ' + where_filter
        if database.db_type == 'oracle':
            if not _type:
                _type = ''
            else:
                _type = 'order by ' + _type + ' desc'
            query = '\n                select * from (\n                    select\n                        inst_id,\n                        sql_id,\n                        parsing_schema_name,\n                        executions,\n                        round(ELAPSED_TIME/1e6,3) ELAPSED_TIME,\n                        trunc(elapsed_time/decode(executions, 0, 1, executions)/1e3) ELAPSED_TIME_PER_EXECUTION,\n                        round(cpu_time/1e6,3) CPU_TIME,\n                        trunc(cpu_time/decode(executions, 0, 1, executions)/1e3) CPU_TIME_PER_EXECUTION,\n                        buffer_gets,\n                        disk_reads,\n                        sql_text\n                    from\n                        gV$SQLAREA where 1 = 1 %s\n                    %s\n                    ) where rownum <= 200' % (where_filter, _type)
            flag, data = run_sql(database, query)
            if not flag:
                raise build_exception_from_java(data)
        else:
            if database.db_type == 'db2':
                if not _type:
                    _type = ''
                else:
                    _type = 'ORDER BY ' + _type + ' desc FETCH FIRST 200 ROWS ONLY'
                if not database.is_v95_base():
                    query = 'SELECT\n                    hex(executable_id) SQL_ID,\n                    stmt_text SQL_TEXT,\n                    NUM_EXEC_WITH_METRICS EXECUTIONS,\n                    STMT_EXEC_TIME/1000000 ELAPSED_TIME,\n                    STMT_EXEC_TIME/1000/NUM_EXEC_WITH_METRICS ELAPSED_TIME_PER_EXECUTION,\n                    TOTAL_CPU_TIME/1000000 CPU_TIME,\n                    LOCK_WAIT_TIME/1000000 LOCK_TIME,\n                    (POOL_READ_TIME + POOL_WRITE_TIME + DIRECT_READ_TIME + DIRECT_WRITE_TIME)/1000000 IO_TIME,\n                    (POOL_DATA_L_READS + POOL_TEMP_DATA_L_READS + POOL_XDA_L_READS +   POOL_TEMP_XDA_L_READS + POOL_INDEX_L_READS + POOL_TEMP_INDEX_L_READS) POOL_L_READS,\n                    (POOL_DATA_P_READS + POOL_TEMP_DATA_P_READS + POOL_XDA_P_READS +  POOL_TEMP_XDA_P_READS + POOL_INDEX_P_READS + POOL_TEMP_INDEX_P_READS) POOL_P_READS,\n                    ROWS_READ,\n                    ROWS_RETURNED,\n                    ROWS_MODIFIED\n                FROM\n                    TABLE (MON_GET_PKG_CACHE_STMT(null,\n                    null,\n                    null,\n                    -2)) where NUM_EXEC_WITH_METRICS > 0 %s\n                %s' % (where_filter, _type)
                else:
                    query = "\n                    SELECT\n                            '' SQL_ID,\n                            stmt_text SQL_TEXT,\n                            NUM_EXECUTIONS EXECUTIONS,\n                            TOTAL_EXEC_TIME_MS ELAPSED_TIME,\n                            TOTAL_EXEC_TIME_MS/NUM_EXECUTIONS ELAPSED_TIME_PER_EXECUTION,\n                            (TOTAL_USR_CPU_TIME_MS+TOTAL_SYS_CPU_TIME_MS)/1000 CPU_TIME,\n                            0 LOCK_TIME,\n                            0 IO_TIME,\n                            (POOL_DATA_L_READS + POOL_TEMP_DATA_L_READS + POOL_XDA_L_READS +   POOL_TEMP_XDA_L_READS + POOL_INDEX_L_READS + POOL_TEMP_INDEX_L_READS) POOL_L_READS,\n                            (POOL_DATA_P_READS + POOL_TEMP_DATA_P_READS + POOL_XDA_P_READS +  POOL_TEMP_XDA_P_READS + POOL_INDEX_P_READS + POOL_TEMP_INDEX_P_READS) POOL_P_READS,\n                            ROWS_READ,\n                            0 ROWS_RETURNED,\n                            INT_ROWS_DELETED+INT_ROWS_INSERTED+INT_ROWS_UPDATED ROWS_MODIFIED\n                        FROM\n                            SYSIBMADM.SNAPDYN_SQL where NUM_EXECUTIONS > 0 %s\n                        %s" % (where_filter, _type)
                flag, data = run_sql(database, query)
                if not flag:
                    raise build_exception_from_java(data)
                else:
                    if database.db_type == 'sqlserver':
                        if not _type:
                            _type = ''
                        else:
                            _type = 'order by ' + _type + ' desc'
                        where_filter1 = f'''and TEXT like '%{sqltext}%'''' if sqltext else ''
                        where_filter2 = f'''and name like '%{sqltext}%'''' if sqltext else ''
                        query = '\nselect top 200 v.*\nfrom (\n select\n            execution_count EXECUTIONS,\n            convert(bigint, total_elapsed_time/1000000) ELAPSED_TIME,\n            convert(bigint, total_elapsed_time/1000)/execution_count ELAPSED_TIME_PER_EXECUTION,\n            convert(bigint, total_worker_time/1000000) WORK_TIME,\n            total_logical_reads LOGICAL_READS,\n            total_physical_reads READS,\n            total_logical_writes LOGICAL_WRITES,\n            qt.TEXT as [SQL_TEXT],\n            substring(sys.fn_sqlvarbasetostr(sql_handle),3,1000) SQL_ID\n        from\n            sys.dm_exec_query_stats as qs\n        CROSS APPLY sys.dm_exec_sql_text(sql_handle) AS qt\n        where 1=1 %s\n        ) v\n%s' % (where_filter1, _type)
                        query2 = '\n          select top 200 * from (\n             select\n            execution_count EXECUTIONS,\n            convert(bigint, total_elapsed_time/1000000) ELAPSED_TIME,\n            convert(bigint, total_elapsed_time/1000)/execution_count ELAPSED_TIME_PER_EXECUTION,\n            convert(bigint, total_worker_time/1000000) WORK_TIME,\n            total_logical_reads LOGICAL_READS,\n            total_physical_reads READS,\n            total_logical_writes LOGICAL_WRITES,\n            qt.TEXT as [SQL_TEXT],\n            substring(sys.fn_sqlvarbasetostr(sql_handle),3,1000) SQL_ID\n        from\n            sys.dm_exec_query_stats as qs\n        CROSS APPLY sys.dm_exec_sql_text(sql_handle) AS qt) v where 1 = 1 %s\n%s' % (where_filter, _type)
                        flag, data = run_sql(database, query)
                        if not flag:
                            flag, data = run_sql(database, query2)
                            if not flag:
                                raise build_exception_from_java(data)
        return data
    except ObjectDoesNotExist as e:
        return {'error_message': str(e)}
    except Exception as err:
        return {'error_message': str(err)}
# okay decompiling ./restful/hawkeye/api/v1/monitor/services/topsqlService.pyc
