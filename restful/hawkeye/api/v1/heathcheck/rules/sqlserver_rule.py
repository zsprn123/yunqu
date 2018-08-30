# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/heathcheck/rules/sqlserver_rule.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 25884 bytes
from api.v1.monitor.services.runsqlService import run_sql
from .base_rule import Rule
import datetime, time, logging
logger = logging.getLogger(__file__)

class SQLServer_Rule(Rule):

    def __init__(self, check_sql, category, description, advise, title):
        super(SQLServer_Rule, self).__init__()
        self.check_sql = check_sql
        self.description = description
        self.category = category
        self.advise = advise
        self.database_type = 'sqlserver'
        self.supported_db_versions = []
        self.title = title
        self.total_score = 10

    def is_right_version(self, db_version):
        return True

    def _check(self, database):
        try:
            flag, result = run_sql(database, self.check_sql)
            if flag:
                if result:
                    resultSet = [list(r.values()) for r in result]
                    self.set_result_raw(resultSet)
                    self.set_result()
            if self.is_failed():
                self.set_score()
                self.resize_result_raw()
                self.set_advise()
        except Exception as e:
            logger.exception('health check queries, error: %s', e)

    def set_result_raw(self, resultSet):
        if resultSet:
            self.result_raw = resultSet[0][0]
        else:
            self.result_raw = ''

    def set_result(self):
        pass

    def is_failed(self):
        pass

    def set_advise(self):
        pass

    def set_score(self):
        self.score = 0

    def is_checked(self):
        return self.result_raw != ''


class SQLServer_Config_Rule(SQLServer_Rule):

    def __init__(self, check_sql, description, advise, title):
        super(SQLServer_Config_Rule, self).__init__(check_sql, '', description, advise, title)

    def set_result_raw(self, resultSet):
        self.result_raw = int(resultSet[0][0] if resultSet[0][0] != '' else '0')


class SQLServer_Performance_Rule(SQLServer_Rule):

    def __init__(self, check_sql, description, advise, title):
        super(SQLServer_Performance_Rule, self).__init__(check_sql, '', description, advise, title)

    def set_result_raw(self, resultSet):
        self.result_raw = int(resultSet[0][0] if resultSet[0][0] != '' else '0')

    def is_failed(self):
        return self.result_raw > 0


class SQLServer_Secure_Rule(SQLServer_Rule):

    def __init__(self, check_sql, description, advise, title):
        super(SQLServer_Secure_Rule, self).__init__(check_sql, '', description, advise, title)

    def set_result_raw(self, resultSet):
        self.result_raw = int(resultSet[0][0] if resultSet[0][0] != '' else '0')

    def is_failed(self):
        return self.result_raw > 0


class SQLServer_Management_Rule(SQLServer_Rule):

    def __init__(self, check_sql, description, advise, title):
        super(SQLServer_Management_Rule, self).__init__(check_sql, '', description, advise, title)


class SQLServer_Backup_Rule(SQLServer_Rule):

    def __init__(self, check_sql, description, advise, title):
        super(SQLServer_Backup_Rule, self).__init__(check_sql, '', description, advise, title)


class Check_Cache_Hit(SQLServer_Performance_Rule):

    def __init__(self, id, name):
        super(Check_Cache_Hit, self).__init__("select\n (cast(sum(case ltrim(rtrim(counter_name))\n\nwhen 'buffer cache hit ratio'\n\nthen cast(cntr_value as integer) else null end) as float) /\n cast(sum(case ltrim(rtrim(counter_name))\n\nwhen 'buffer cache hit ratio base' then cast(cntr_value as integer)\n\n else null end) as float)) * 100\n as buffercachehitratio\nfrom\n sys.dm_os_performance_counters\nwhere\n ltrim(rtrim([object_name])) like '%:buffer manager' and\n [counter_name] like 'buffer cache hit ratio%'", '90%', {}, '')
        self.priority = ''
        self.score = 5
        self.total_score = 5

    def is_failed(self):
        return self.result_raw < 90

    def set_result(self):
        self.result = '(' + str(round(self.result_raw, 2)) + '%)' + (',,IO, ' if self.is_failed() else ' ')

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          ',SQL,IO\n\n:\n    ,SQL server\n,\n']}
        self.exe_advise = ' '


class Check_Log_Space(SQLServer_Secure_Rule):

    def __init__(self, id, name):
        super(Check_Log_Space, self).__init__('dbcc sqlperf(logspace)', '90%', {}, '')

    def set_result_raw(self, resultSet):
        self.result_raw = [x for x in resultSet if x[2] > 90]

    def is_failed(self):
        return len(self.result_raw) > 0

    def set_result(self):
        self.result = '(' + str(len(self.result_raw)) + ')' + (',' if self.is_failed() else ' ')

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          ',:\n\n' + ('\n        \n').join(['(' + x[0] + '):(' + str(x[2]) + ')' for x in self.result_raw])]}
        self.exe_advise = ' '


class Check_Disk_Space(SQLServer_Secure_Rule):

    def __init__(self, id, name):
        super(Check_Disk_Space, self).__init__('EXEC master.dbo.xp_fixeddrives', '10G', {}, '')

    def set_result_raw(self, resultSet):
        self.result_raw = [x for x in resultSet if x[1] < 10240]

    def is_failed(self):
        return len(self.result_raw) > 0

    def set_result(self):
        self.result = '(' + str(len(self.result_raw)) + ')' + (',' if self.is_failed() else ' ')

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          ',:\n\n' + ('\n        \n').join([':(' + x[0] + '):(' + str(x[2]) + ')' for x in self.result_raw])]}
        self.exe_advise = ' '


class Check_TOP5IO_SQL(SQLServer_Performance_Rule):

    def __init__(self, id, name):
        super(Check_TOP5IO_SQL, self).__init__('\nselect top 5\n\n    (qs.total_logical_reads / qs.execution_count) as avg_logical_reads,\n    (qs.total_logical_writes / qs.execution_count) as avg_logical_writes,\n    (qs.total_physical_reads / qs.execution_count) as avg_phys_reads,\n\n    qs.execution_count,\n\n    qs.statement_start_offset,\n    qs.statement_end_offset,\n\n    qt.dbid,\n    qt.objectid,\n\n    SUBSTRING(qt.text,\n              qs.statement_start_offset/2,\n              (case when qs.statement_end_offset = -1\n                         then len(convert(nvarchar(max), qt.text)) * 2\n                    else qs.statement_end_offset\n               end - qs.statement_start_offset\n               ) / 2  + 1\n              ) as statement\nfrom sys.dm_exec_query_stats qs\ncross apply sys.dm_exec_sql_text(sql_handle) as qt\ncross apply sys.dm_exec_query_plan(plan_handle) as q\norder by\n (total_logical_reads + total_logical_writes) / Execution_count Desc ', 'IOTOP5SQL', {}, 'IOSQL')

    def set_result_raw(self, resultSet):
        self.result_raw = resultSet

    def is_failed(self):
        return len(self.result_raw) > 0

    def set_result(self):
        self.result = '(' + str(len(self.result_raw)) + ')' + ('sqlcpu,' if self.is_failed() else ' ')

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          'SQL,:\n\n' + ('\n        \n').join(['SQL:\n' + x[-1] + '\n ' + ' ' for x in self.result_raw])]}
        self.exe_advise = ' '


class Check_TOP8_Freq_SQL(SQLServer_Performance_Rule):

    def __init__(self, id, name):
        super(Check_TOP8_Freq_SQL, self).__init__('\nSELECT TOP 8\n    cp.cacheobjtype,\n\n    cp.usecounts,      --\n    cp.size_in_bytes,  --\n\n    qs.execution_count,     --,usecounts.\n    qs.plan_generation_num, --:\n\n    qs.statement_start_offset,\n    qs.statement_end_offset,\n\n    qt.dbid,\n    qt.objectid,\n    SUBSTRING(qt.text,\n              qs.statement_start_offset/2,\n              (case when qs.statement_end_offset = -1\n                         then len(convert(nvarchar(max), qt.text)) * 2\n                    else qs.statement_end_offset\n               end - qs.statement_start_offset\n               ) / 2  + 1\n              ) as statement\nFROM sys.dm_exec_query_stats qs\n\ncross apply sys.dm_exec_sql_text(qs.sql_handle) as qt\n\ninner join sys.dm_exec_cached_plans as cp\n        on qs.plan_handle=cp.plan_handle\n           and cp.plan_handle=qs.plan_handle\n\nwhere cp.usecounts>4\nORDER BY [dbid],[Usecounts] DESC  ', 'TOP8SQL', {}, 'SQL')

    def set_result_raw(self, resultSet):
        self.result_raw = resultSet

    def is_failed(self):
        return len(self.result_raw) > 0

    def set_result(self):
        self.result = '(' + str(len(self.result_raw)) + ')' + ('sql,' if self.is_failed() else ' ')

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          'SQL,:\n\n' + ('\n        \n').join(['SQL:\n' + x[-1] + '\n' + '  ' for x in self.result_raw])]}
        self.exe_advise = ' '


class Check_TOP5_SQL(SQLServer_Performance_Rule):

    def __init__(self, id, name):
        super(Check_TOP5_SQL, self).__init__("\nselect\n    highest_cpu_queries.*,\n\n    q.dbid,\n    q.objectid,\n    q.number,\n    q.encrypted,\n     q.[text]\nfrom\n(\n    select top 5 qs.*\n    from sys.dm_exec_query_stats qs\n    order by qs.total_worker_time desc\n) as highest_cpu_queries\n\ncross apply sys.dm_exec_sql_text(plan_handle) as q\n--where text like '%%'\norder by highest_cpu_queries.total_worker_time desc ", 'CPUTOP5SQL', {}, 'CPUSQL')

    def set_result_raw(self, resultSet):
        self.result_raw = resultSet

    def is_failed(self):
        return len(self.result_raw) > 0

    def set_result(self):
        self.result = '(' + str(len(self.result_raw)) + ')' + ('sqlcpu,' if self.is_failed() else ' ')

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          'SQL,:\n\n' + ('\n        \n').join(['SQL_HANDLE(' + x[0] + ')  ' + 'SQL' for x in self.result_raw])]}
        self.exe_advise = ' '


class Check_Index_Fragment(SQLServer_Performance_Rule):

    def __init__(self, id, name):
        super(Check_Index_Fragment, self).__init__('\ndeclare @dbid int\nselect @dbid = db_id()\n\nSELECT *\nFROM sys.dm_db_index_physical_stats (@dbid, NULL, NULL, NULL, NULL)\nwhere avg_fragmentation_in_percent > 25\n  order by avg_fragmentation_in_percent desc ', '25%', {}, '')

    def set_result_raw(self, resultSet):
        self.result_raw = resultSet

    def is_failed(self):
        return len(self.result_raw) > 0

    def set_result(self):
        self.result = '(' + str(len(self.result_raw)) + ')' + ('25%,,' if self.is_failed() else ' ')

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          ',:\n\n' + ('\n        \n').join([':(' + x[0] + ')ID(' + str(x[1]) + ')' for x in self.result_raw])]}
        self.exe_advise = ' '


class Check_Unuse_Index(SQLServer_Performance_Rule):

    def __init__(self, id, name):
        super(Check_Unuse_Index, self).__init__("SELECT  ind.index_id ,\n        obj.name AS TableName ,\n        ind.name AS IndexName ,\n        ind.type_desc ,\n        indUsage.user_seeks ,\n        indUsage.user_scans ,\n        indUsage.user_lookups ,\n        indUsage.user_updates ,\n        indUsage.last_system_seek ,\n        indUsage.last_user_scan ,\n        'drop index [' + ind.name + '] ON [' + obj.name + ']' AS DropIndexCommand\nFROM    sys.indexes AS ind\n        INNER JOIN sys.objects AS obj ON ind.object_id = obj.object_id\n        LEFT JOIN sys.dm_db_index_usage_stats indUsage ON ind.object_id = indUsage.object_id\n                                                          AND ind.index_id = indUsage.index_id\nWHERE   ind.type_desc <> 'HEAP'\n        AND obj.type <> 'S'\n        AND OBJECTPROPERTY(obj.object_id, 'isusertable') = 1\n        AND ( ISNULL(indUsage.user_seeks, 0) = 0\n              AND ISNULL(indUsage.user_scans, 0) = 0\n              AND ISNULL(indUsage.user_lookups, 0) = 0\n            )\nORDER BY obj.name ,\n        ind.name", '', {}, '')
        self.priority = ''
        self.score = 5
        self.total_score = 5

    def is_failed(self):
        return len(self.result_raw) > 0

    def set_result(self):
        self.result = '(' + str(len(self.result_raw)) + '),IO ' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          ',:\n\n' + ('\n        \n').join(['(' + x[1] + ')(' + str(x[2]) + ')' for x in self.result_raw])]}
        self.exe_advise = ' '

    def set_result_raw(self, resultSet):
        self.result_raw = resultSet


class Check_Backup(SQLServer_Backup_Rule):

    def __init__(self, id, name):
        super(Check_Backup, self).__init__("select top 1  mdb.[backup_start_date] '',\n        mdb.[backup_finish_date]  AS '',\n       mdb.name AS '',\n       mdbf.physical_name AS '',\n       CASE mdb.type\n              WHEN 'D' THEN ''\n              WHEN 'I'THEN ''\n              WHEN 'L' THEN ''\n              WHEN 'F' THEN ''\n              WHEN 'G' THEN 'Differential file'\n              WHEN 'P' THEN 'Partial'\n              WHEN 'Q' THEN 'Differential partial'\n              ELSE ''\n       END AS '',\n       CASE mdb.recovery_model\n              WHEN 'SIMPLE' THEN ''\n              WHEN 'FULL' THEN ''\n       ELSE 'NULL'\n       END AS '',\n       mdb.first_lsn AS 'lsn',\n       mdb.last_lsn AS 'lsn',\n       mdbf.backup_size AS '',\n       mdbp.physical_device_name AS ''\nfrom msdb.dbo.backupset AS mdb,\n       msdb.dbo.backupmediafamily AS mdbp,\n              (select\n                     backup_set_id,\n                     backup_size,\n                     physical_name\n              from msdb.dbo.backupfile\n              --where logical_name = 'master'     --,\n              ) AS mdbf\nwhere  mdb.backup_set_id = mdbf.backup_set_id\nand mdb.media_set_id = mdbp.media_set_id  order by '' desc\n", '', {}, '')

    def is_failed(self):
        if len(self.result_raw) == 0:
            return True
        else:
            return self.result_raw[0] < datetime.datetime.now() - (datetime.timedelta(days=1))

    def set_result(self):
        self.result = ('(' + self.result_raw[0].strftime('%Y-%m-%d %H:%M:%S') + ')(' + self.result_raw[1].strftime('%Y-%m-%d %H:%M:%S') + '),(' + self.result_raw[4] + '),\n        (' + self.result_raw[-1] + ')' if len(self.result_raw) != 0 else '') if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          ',\n']}
        self.exe_advise = ' '

    def set_result_raw(self, resultSet):
        self.result_raw = resultSet if len(resultSet) == 0 else resultSet[0]


class Check_Error_Log(SQLServer_Management_Rule):

    def __init__(self, id, name):
        super(Check_Error_Log, self).__init__('EXEC master.dbo.xp_readerrorlog 0, 1, null, "Error", "%s", "%s", "desc"' % (
         (datetime.datetime.now() - (datetime.timedelta(days=30))).strftime('%Y-%m-%d %H:%M:%S'),
         datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')), '', {}, '')

    def is_failed(self):
        return len([x for x in self.result_raw if 'This instance of SQL Server has been using a process ID' not in x[2]]) > 0

    def set_result(self):
        self.result = '' + str(len(self.result_raw)) + ',' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          ',:\n\n' + ('\n        \n').join(['(' + datetime.datetime.fromtimestamp(x[0] / 1000.0).strftime('%Y-%m-%d %H:%M:%S') + '):' + str(x[1]) + x[2] for x in self.result_raw])]}
        self.exe_advise = ' '

    def set_result_raw(self, resultSet):
        self.result_raw = resultSet


class Check_Process(SQLServer_Config_Rule):

    def __init__(self, id, name):
        super(Check_Process, self).__init__('SELECT @@MAX_CONNECTIONS', '', {}, '')

    def is_failed(self):
        return self.result_raw[0][0] < 1000

    def set_result(self):
        self.result = '(MAX_CONNECTIONS)(' + self.result_raw[0][0] + ',' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          ',:\n        MAX_CONNECTIONS  SQL Server  ']}
        self.exe_advise = ' '

    def set_result_raw(self, resultSet):
        self.result_raw = resultSet


class Check_Job(SQLServer_Secure_Rule):

    def __init__(self, id, name):
        super(Check_Job, self).__init__("SELECT\n   [jop].[name] AS ''\n   ,[dp].[name] AS ''\n   ,[cat].[name] AS ''\n   ,[jop].[description] AS ''\n   ,[jop].[date_created] AS ''\n   ,[jop].[date_modified] AS ''\n    ,CASE WHEN [sJOBH].[run_date] IS NULL\n                  OR [sJOBH].[run_time] IS NULL THEN NULL\n             ELSE CAST(CAST([sJOBH].[run_date] AS CHAR(8)) + ' '\n                  + STUFF(STUFF(RIGHT('000000'\n                                      + CAST([sJOBH].[run_time] AS VARCHAR(6)),\n                                      6), 3, 0, ':'), 6, 0, ':') AS DATETIME)\n        END AS ''\n   ,[sv].[name] AS ''\n   ,[step].[step_id] AS ''\n   ,[step].[step_name] AS ''\n   , CASE\n        WHEN [sch].[schedule_uid] IS NULL THEN ''\n          ELSE ''\n      END AS ''\n   ,[sch].[name] AS ''\n   , CASE [jop].[delete_level]\n        WHEN 0 THEN ''\n        WHEN 1 THEN ''\n        WHEN 2 THEN ''\n        WHEN 3 THEN ''\n      END AS ''\n       ,[md].[run_stats] AS ''\n    ,[md].[counts] AS ''\n    ,CASE [sJOBSCH].[NextRunDate]\n          WHEN 0 THEN NULL\n          ELSE CAST(CAST([sJOBSCH].[NextRunDate] AS CHAR(8)) + ' '\n               + STUFF(STUFF(RIGHT('000000'\n                                   + CAST([sJOBSCH].[NextRunTime] AS VARCHAR(6)),\n                                   6), 3, 0, ':'), 6, 0, ':') AS DATETIME)\n        END AS ''\nFROM [msdb].[dbo].[sysjobs] AS [jop]\nLEFT JOIN [msdb].[sys].[servers] AS [sv]\n         ON [jop].[originating_server_id] = [sv].[server_id]\nLEFT JOIN [msdb].[dbo].[syscategories] AS [cat]\n         ON [jop].[category_id] = [cat].[category_id]\nLEFT JOIN [msdb].[dbo].[sysjobsteps] AS [step]\n         ON [jop].[job_id] = [step].[job_id]\n            AND [jop].[start_step_id] = [step].[step_id]\nLEFT JOIN [msdb].[sys].[database_principals] AS [dp]\n         ON [jop].[owner_sid] = [dp].[sid]\nLEFT JOIN ( SELECT  [job_id] ,\n                            MIN([next_run_date]) AS [NextRunDate] ,\n                            MIN([next_run_time]) AS [NextRunTime]\n                    FROM    [msdb].[dbo].[sysjobschedules]\n                    GROUP BY [job_id]\n                  ) AS [sJOBSCH] ON [jop].[job_id] = [sJOBSCH].[job_id]\nLEFT JOIN [msdb].[dbo].[sysjobschedules] AS [jsch]\n         ON [jop].[job_id] = [jsch].[job_id]\nLEFT JOIN [msdb].[dbo].[sysschedules] AS [sch]\n         ON [jsch].[schedule_id] = [sch].[schedule_id]\nLEFT JOIN  (\n              SELECT mdsh.job_id AS [jobid] ,\n            CASE [mdsh].[run_status]\n                WHEN 0 THEN 'Failed'\n                WHEN 1 THEN 'Succeed'\n                WHEN 2 THEN 'Retry'\n                WHEN 3 THEN 'Cancel'\n            END AS 'run_stats',\n            count(mdsh.job_id) AS 'counts'\n              FROM [msdb].[dbo].[sysjobhistory] AS [mdsh] ,[msdb].[dbo].[sysjobs] AS [mdss]\n              WHERE [mdsh].[job_id] = [mdss].[job_id]\n              AND [mdsh].[run_status] = 0\n              GROUP BY [mdsh].[job_id],[mdsh].[run_status]\n              ) AS [md]\n              ON [jop].[job_id] = [md].[jobid]\nLEFT JOIN ( SELECT  [job_id] ,\n                            [run_date] ,\n                            [run_time] ,\n                            [run_status] ,\n                            [run_duration] ,\n                            ROW_NUMBER() OVER ( PARTITION BY [job_id] ORDER BY [run_date] DESC, [run_time] DESC ) AS RowNumber\n                    FROM    [msdb].[dbo].[sysjobhistory]\nWHERE   [step_id] = 0\n                  ) AS [sJOBH] ON [jop].[job_id] = [sJOBH].[job_id]\n                                  AND [sJOBH].[RowNumber] = 1\nORDER BY [jop].[name]\n", 'job', {}, 'JOB')

    def is_failed(self):
        return len(self.result_raw) > 0

    def set_result(self):
        self.result = 'JOB' + str(len(self.result_raw)) + ',,' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          'JOB,:\n\n' + ('\n        \n').join(['job(' + x[0] + '):' + x[0].strftime('%Y-%m-%d %H:%M:%S') + ')' for x in self.result_raw])]}
        self.exe_advise = ' '

    def set_result_raw(self, resultSet):
        self.result_raw = [x for x in self.result_raw if x[13] == 'Failed'] and x[6] > datetime.datetime.now() - (datetime.timedelta(days=30))
# okay decompiling ./restful/hawkeye/api/v1/heathcheck/rules/sqlserver_rule.pyc
