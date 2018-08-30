# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/heathcheck/rules/oracle_rule.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 116739 bytes
import logging
from api.v1.monitor.services.runsqlService import run_sql
from .base_rule import Rule
logger = logging.getLogger('api')

class Oracle_Rule(Rule):

    def __init__(self, check_sql, category, description, advise, title):
        super(Oracle_Rule, self).__init__()
        self.check_sql = check_sql
        self.description = description
        self.category = category
        self.advise = advise
        self.database_type = 'Oracle'
        self.supported_db_versions = ['10', '11', '12']
        self.title = title
        self.total_score = 10

    def _check(self, database):
        try:
            flag, result = run_sql(database, self.check_sql)
            if flag:
                resultSet = [list(r.values()) for r in result]
                self.set_result_raw(resultSet)
                self.set_result()
            else:
                self.result = ''
            if self.is_failed():
                self.set_score()
                self.resize_result_raw()
                self.set_advise()
        except Exception as e:
            logger.exception('health check queries, error: %s', e)
            print(self.check_sql)

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


class Oracle_Config_Rule(Oracle_Rule):

    def __init__(self, check_sql, description, advise, title):
        super(Oracle_Config_Rule, self).__init__(check_sql, '', description, advise, title)
        self.priority = ''
        self.score = 5
        self.total_score = 5


class Oracle_Performance_Rule(Oracle_Rule):

    def __init__(self, check_sql, description, advise, title):
        super(Oracle_Performance_Rule, self).__init__(check_sql, '', description, advise, title)

    def set_result_raw(self, resultSet):
        self.result_raw = int(resultSet[0][0] if resultSet[0][0] != '' else '0')

    def is_failed(self):
        return self.result_raw > 0


class Oracle_Secure_Rule(Oracle_Rule):

    def __init__(self, check_sql, description, advise, title):
        super(Oracle_Secure_Rule, self).__init__(check_sql, '', description, advise, title)

    def set_result_raw(self, resultSet):
        self.result_raw = int(resultSet[0][0] if resultSet[0][0] != '' else '0')

    def is_failed(self):
        return self.result_raw > 0


class Oracle_Management_Rule(Oracle_Rule):

    def __init__(self, check_sql, description, advise, title):
        super(Oracle_Management_Rule, self).__init__(check_sql, '', description, advise, title)


class Oracle_Backup_Rule(Oracle_Rule):

    def __init__(self, check_sql, description, advise, title):
        super(Oracle_Backup_Rule, self).__init__(check_sql, '', description, advise, title)


class Check_Is_Archivelog(Oracle_Config_Rule):

    def __init__(self, id, name):
        super(Check_Is_Archivelog, self).__init__('select log_mode from v$database', '', {}, '')
        self.priority = ''
        self.score = 20
        self.total_score = 20
        self.set_id_and_db_name(id, name)

    def is_failed(self):
        return self.result_raw != 'ARCHIVELOG'

    def set_result(self):
        self.result = '(' + self.result_raw + ')' + (',,! ' if self.is_failed() else ' ')

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          ',\n:\n    ,.\n    ,,\n']}
        self.exe_advise = 'shutdown immediate;\nstartup mount;\nalter database archivelog;\nalter database open;\narchive log list;'


class Check_Redo_Size(Oracle_Config_Rule):

    def __init__(self, id, name):
        super(Check_Redo_Size, self).__init__('select min(sum(bytes/1024/1024)) from gv$log group by thread#', '', {}, 'REDO')
        self.set_id_and_db_name(id, name)

    def is_failed(self):
        return self.result_raw < 1024

    def set_result(self):
        self.result = '(' + str(self.result_raw) + 'M )' + (',,,' if self.is_failed() else ' ')

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          'REDO2G,10\n:\n    \n    ,,,']}
        self.exe_advise = {}


class Check_Processes(Oracle_Config_Rule):

    def __init__(self, id, name):
        super(Check_Processes, self).__init__("select value from v$parameter where NAME = 'processes'", 'processes', {}, '')
        self.set_id_and_db_name(id, name)

    def is_failed(self):
        return self.result_raw < 301

    def set_result_raw(self, resultSet):
        self.result_raw = int(resultSet[0][0])

    def set_result(self):
        self.result = ' processes(' + str(self.result_raw) + ')' + (',,' if self.is_failed() else ' ')

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          '\n:\n    ProcessesInstanceOSsessions,processes,,']}
        self.exe_advise = {}


class Check_Oracle_Patch(Oracle_Secure_Rule):

    def __init__(self, id, name):
        super(Check_Oracle_Patch, self).__init__("SELECT /*+ NO_MERGE */\n        TO_CHAR(ACTION_TIME,'YYYY/MM/DD HH24:MI:SS'),ACTION,COMMENTS\n  FROM dba_registry_history\n ORDER BY 1", '', {}, '')
        self.priority = ''
        self.score = 20
        self.total_score = 20
        self.supported_db_versions = [11]
        self.set_id_and_db_name(id, name)

    def is_failed(self):
        return len([x for x in self.result_raw if 'PSU 11.2.0.4.171017' in x]) == 0

    def set_result_raw(self, resultSet):
        self.result_raw = ['(' + x[0] + ') ' + x[1] + '(' + x[2] + ')' for x in resultSet]

    def set_result(self):
        self.result = '(PSU 11.2.0.4.171017)' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          '11g,,.,sysdba :\ncreate user a identified by 123456;\ncreate user b identified by 123456;\ngrant resource,connect to a;\ngrant connect to b;\nconn a/123456\ncreate table test(id number);\ninsert into test values(1);\ncommit;\nconn / as sysdba\ngrant select on a.test to b;\nconn b/123456;\ndelete from (with temp as (\nselect * from a.test)\nselect * from temp);\ncommit;\nconn / as sysdba\ndrop user a cascade;\ndrop user b cascade;\n\n\n:\n        \n' + ('\n        \n').join(self.result_raw)]}
        self.exe_advise = {}


class Check_Session(Oracle_Config_Rule):

    def __init__(self, id, name):
        super(Check_Session, self).__init__("select value from v$parameter where NAME = 'sessions'", 'sessions', {}, '')
        self.set_id_and_db_name(id, name)

    def is_failed(self):
        return self.result_raw < 301

    def set_result_raw(self, resultSet):
        self.result_raw = int(resultSet[0][0])

    def set_result(self):
        self.result = ' sessions(' + str(self.result_raw) + ')' + (',,' if self.is_failed() else ' ')

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          '\n:\n    Sessions:oracle.,']}
        self.exe_advise = {}


class Check_Block_Count(Oracle_Config_Rule):

    def __init__(self, id, name):
        super(Check_Block_Count, self).__init__("select value from v$parameter where NAME = 'db_file_multiblock_read_count'", 'db_file_multiblock_read_count', {}, '')
        self.set_id_and_db_name(id, name)

    def is_failed(self):
        return self.result_raw < 10

    def set_result_raw(self, resultSet):
        self.result_raw = int(resultSet[0][0])

    def set_result(self):
        self.result = ' db_file_multiblock_read_count(' + str(self.result_raw) + ')' + (',,' if self.is_failed() else ' ')

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          '\n:\n    Sessions:oracle.,']}
        self.exe_advise = {}


class Check_Open_Cursors(Oracle_Config_Rule):

    def __init__(self, id, name):
        super(Check_Open_Cursors, self).__init__("select value from v$parameter where NAME = 'open_cursors'", 'open_cursors', {}, '')
        self.set_id_and_db_name(id, name)

    def is_failed(self):
        return self.result_raw < 301

    def set_result_raw(self, resultSet):
        self.result_raw = int(resultSet[0][0])

    def set_result(self):
        self.result = ' open_cursors(' + str(self.result_raw) + ')' + (',, ORA-O1000 , ' if self.is_failed() else ' ')

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          ' 300\n:\n    open_cursorssession()cursor()']}
        self.exe_advise = {}


class Check_Resource_Manager(Oracle_Config_Rule):

    def __init__(self, id, name):
        super(Check_Resource_Manager, self).__init__("select value from v$parameter where NAME = 'resource_manager_plan'", '', {}, '')
        self.set_id_and_db_name(id, name)
        self.supported_db_versions = ['11', '12']

    def set_result_raw(self, resultSet):
        if resultSet:
            self.result_raw = resultSet[0][0]
        else:
            self.result_raw = ''

    def is_failed(self):
        if self.result_raw == '':
            return True
        else:
            return False

    def set_result(self):
        self.result = ' resource_manager_plan(' + str(self.result_raw) + ') ' + ',,HIGH CPU,IO ,UNDO, ' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          ',\n:\n     ,,']}
        self.exe_advise = {}


class Check_Db_files(Oracle_Config_Rule):

    def __init__(self, id, name):
        super(Check_Db_files, self).__init__("select value from v$parameter where NAME = 'db_files'", 'db_files', {}, '')
        self.set_id_and_db_name(id, name)

    def is_failed(self):
        return self.result_raw < '201'

    def set_result(self):
        self.result = ' db_files(' + str(self.result_raw) + ') ' + (',,,ORA-00059 ,' if self.is_failed() else ' ')

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          'db_files ,\n:\n     db_files,']}
        self.exe_advise = {}


class Check_Audit(Oracle_Config_Rule):

    def __init__(self, id, name):
        super(Check_Audit, self).__init__("select value from v$parameter where NAME = 'audit_trail'", '', {}, '')
        self.set_id_and_db_name(id, name)

    def is_failed(self):
        return self.result_raw == ''

    def set_result(self):
        self.result = ' audit_trail(' + str(self.result_raw) + ') ' + (',,' if self.is_failed() else ' ')

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          '\n:\n     (Audit),(:system SYS.AUD$,dba_audit_trail']}
        self.exe_advise = {}


class Check_Password_Life_Time(Oracle_Config_Rule):

    def __init__(self, id, name):
        super(Check_Password_Life_Time, self).__init__("select LIMIT FROM dba_profiles s WHERE resource_name='PASSWORD_LIFE_TIME'", 'Profile', {}, '')
        self.set_id_and_db_name(id, name)

    def is_failed(self):
        return self.result_raw != 'UNLIMITED'

    def set_result(self):
        self.result = ' PASSWORD_LIFE_TIME(' + str(self.result_raw) + ') ' + (',' if self.is_failed() else ' ')

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          '\n:\n     PASSWORD_LIFE_TIME 180']}
        self.exe_advise = {}


class Check_DWECI(Oracle_Config_Rule):

    def __init__(self, id, name):
        super(Check_DWECI, self).__init__("select upper(value)  from v$parameter where name ='_datafile_write_errors_crash_instance' ", '_datafile_write_errors_crash_instance', {}, '_datafile_write_errors_crash_instance')
        self.set_id_and_db_name(id, name)

    def is_failed(self):
        return self.result_raw != 'FALSE'

    def set_result(self):
        self.result = ' _datafile_write_errors_crash_instance(' + str(self.result_raw) + '),,IO,' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          'DBWRI/O:\n11g:\n1. ,RACSYSTEM;,OFFLINE\n2. TRUE,DBWR\n3. FALSE,SYSTEM;\n']}
        self.exe_advise = {}


class Check_AutoTask1(Oracle_Config_Rule):

    def __init__(self, id, name):
        super(Check_AutoTask1, self).__init__("select  status from dba_autotask_client  where client_name='auto optimizer stats collection' ", '', {}, '')
        self.set_id_and_db_name(id, name)

    def is_failed(self):
        return self.result_raw != 'ENABLED'

    def set_result(self):
        self.result = '(' + str(self.result_raw) + '),,' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          '\n']}
        self.exe_advise = {
         "\nBEGIN\ndbms_auto_task_admin.enable(\n client_name => 'auto optimizer stats collection',\n operation   => 'auto optimizer stats job',\n window_name => NULL);\nEND;\n/"}


class Check_AutoTask2(Oracle_Config_Rule):

    def __init__(self, id, name):
        super(Check_AutoTask2, self).__init__("select  status from dba_autotask_client  where client_name='auto space advisor' ", '', {}, '')
        self.set_id_and_db_name(id, name)

    def is_failed(self):
        return self.result_raw == 'ENABLED'

    def set_result(self):
        self.result = '(' + str(self.result_raw) + '),,' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          '\n']}
        self.exe_advise = {
         '\n'}


class Check_AutoTask3(Oracle_Config_Rule):

    def __init__(self, id, name):
        super(Check_AutoTask3, self).__init__("select  status from dba_autotask_client  where client_name='sql tuning advisor' ", 'SQL', {}, 'SQL')
        self.set_id_and_db_name(id, name)

    def is_failed(self):
        return self.result_raw == 'ENABLED'

    def set_result(self):
        self.result = 'SQL(' + str(self.result_raw) + '),,,' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          'SQL\n']}
        self.exe_advise = {
         '\n'}


class Check_Log_Param1(Oracle_Config_Rule):

    def __init__(self, id, name):
        super(Check_Log_Param1, self).__init__("select upper(value)  from v$parameter where name ='_use_adaptive_log_file_sync' ", '_use_adaptive_log_file_sync', {}, '_use_adaptive_log_file_sync')
        self.supported_db_versions = [
         '11', '12']
        self.set_id_and_db_name(id, name)

    def is_failed(self):
        return self.result_raw != 'FALSE'

    def set_result(self):
        self.result = ' _use_adaptive_log_file_sync (' + str(self.result_raw) + '),11.2.0.3TRUE,' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          '(MOS : 1462942.1 ):\nalter system set "_use_adaptive_log_file_sync"=false;\n']}
        self.exe_advise = {}


class Check_undo_autotune(Oracle_Config_Rule):

    def __init__(self, id, name):
        super(Check_undo_autotune, self).__init__("select upper(value)  from v$parameter where name ='_undo_autotune' ", '_undo_autotune', {}, '_undo_autotune')
        self.set_id_and_db_name(id, name)

    def is_failed(self):
        return self.result_raw != 'FALSE'

    def set_result(self):
        self.result = ' _undo_autotune (' + str(self.result_raw) + '),UNDOUNDO' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          '(MOS : 1574714.1 ):\nalter system set _undo_autotune = false;\n']}
        self.exe_advise = {}


class Check_DSC(Oracle_Config_Rule):

    def __init__(self, id, name):
        super(Check_DSC, self).__init__("select upper(value) from v$parameter where name ='deferred_segment_creation' ", 'deferred_segment_creation', {}, 'deferred_segment_creation')
        self.set_id_and_db_name(id, name)

    def is_failed(self):
        return self.result_raw != 'FALSE'

    def set_result(self):
        self.result = ' deferred_segment_creation (' + str(self.result_raw) + '),exp,impBUG' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          '(MOS : 1216282.1 ):\n\n']}
        self.exe_advise = {}


class Check_SL(Oracle_Config_Rule):

    def __init__(self, id, name):
        super(Check_SL, self).__init__("select upper(value) from v$parameter where name ='statistics_level' ", 'statistics_level', {}, 'statistics_level')
        self.set_id_and_db_name(id, name)

    def is_failed(self):
        return self.result_raw != 'TYPICAL'

    def set_result(self):
        self.result = ' statistics_level(' + str(self.result_raw) + '),CBO,SQL,' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          '(MOS : 957433.1 ):\n\n']}
        self.exe_advise = {}


class Check_CFRKT(Oracle_Config_Rule):

    def __init__(self, id, name):
        super(Check_CFRKT, self).__init__("select value from v$parameter where name ='control_file_record_keep_time' ", 'control_file_record_keep_time', {}, 'control_file_record_keep_time')
        self.set_id_and_db_name(id, name)

    def is_failed(self):
        return int(self.result_raw) < 15

    def set_result(self):
        self.result = ' control_file_record_keep_time(' + str(self.result_raw) + '),,,' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          '(MOS : 47322.1 ):\n\n']}
        self.exe_advise = {}


class Check_Diff_RAC_Param(Oracle_Config_Rule):

    def __init__(self, id, name):
        super(Check_Diff_RAC_Param, self).__init__("select name, 'value1:('||max(value)||') value2:('||min(value) ||')' from gv$parameter  where name not in ('thread','instance_name','instance_number','undo_tablespace','local_listener','remote_listener','lisneter_network','control_files','background_dump_dest','core_dump_dest','user_dump_dest','shared_pool_reserved_size','service_names') group by name  having count(distinct value) >1", 'RAC', {}, 'RAC')
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        self.result_raw = [':' + x[0] + ' :' + x[1] + ',' for x in resultSet]

    def is_failed(self):
        return self.result_raw.__len__() > 0

    def set_result(self):
        self.result = ' ' + str(self.result_raw.__len__()) + ',,RAC,,,' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          ',:\n        \n' + ('\n        \n').join(self.result_raw)]}
        self.exe_advise = {}


class Check_Unindexed_FK_Time(Oracle_Performance_Rule):

    def __init__(self, id, name):
        super(Check_Unindexed_FK_Time, self).__init__("WITH\nref_int_constraints AS (\nSELECT /*+ MATERIALIZE NO_MERGE */\n       col.owner,\n       col.table_name,\n       col.constraint_name,\n       con.status,\n       con.r_owner,\n       con.r_constraint_name,\n       COUNT(*) col_cnt,\n       MAX(CASE col.position WHEN 01 THEN col.column_name END) col_01,\n       MAX(CASE col.position WHEN 02 THEN col.column_name END) col_02,\n       MAX(CASE col.position WHEN 03 THEN col.column_name END) col_03,\n       MAX(CASE col.position WHEN 04 THEN col.column_name END) col_04,\n       MAX(CASE col.position WHEN 05 THEN col.column_name END) col_05,\n       MAX(CASE col.position WHEN 06 THEN col.column_name END) col_06,\n       MAX(CASE col.position WHEN 07 THEN col.column_name END) col_07,\n       MAX(CASE col.position WHEN 08 THEN col.column_name END) col_08,\n       MAX(CASE col.position WHEN 09 THEN col.column_name END) col_09,\n       MAX(CASE col.position WHEN 10 THEN col.column_name END) col_10,\n       MAX(CASE col.position WHEN 11 THEN col.column_name END) col_11,\n       MAX(CASE col.position WHEN 12 THEN col.column_name END) col_12,\n       MAX(CASE col.position WHEN 13 THEN col.column_name END) col_13,\n       MAX(CASE col.position WHEN 14 THEN col.column_name END) col_14,\n       MAX(CASE col.position WHEN 15 THEN col.column_name END) col_15,\n       MAX(CASE col.position WHEN 16 THEN col.column_name END) col_16,\n       par.owner parent_owner,\n       par.table_name parent_table_name,\n       par.constraint_name parent_constraint_name\n  FROM dba_constraints  con,\n       dba_cons_columns col,\n       dba_constraints par\n WHERE con.constraint_type = 'R'\n   AND con.owner NOT IN ('ANONYMOUS','APEX_030200','APEX_040000','APEX_040200','DVSYS','LBACSYS','OJVMSYS','APEX_SSO','APPQOSSYS','CTXSYS','DBSNMP','DIP','EXFSYS','FLOWS_FILES','MDSYS','OLAPSYS','ORACLE_OCM','ORDDATA','ORDPLUGINS','ORDSYS','OUTLN','OWBSYS')\n   AND con.owner NOT IN ('SI_INFORMTN_SCHEMA','SQLTXADMIN','SQLTXPLAIN','SYS','SYSMAN','SYSTEM','TRCANLZR','WMSYS','XDB','XS$NULL','PERFSTAT','STDBYPERF')\n   AND col.owner = con.owner\n   AND col.constraint_name = con.constraint_name\n   AND col.table_name = con.table_name\n   AND par.owner(+) = con.r_owner\n   AND par.constraint_name(+) = con.r_constraint_name\n GROUP BY\n       col.owner,\n       col.constraint_name,\n       col.table_name,\n       con.status,\n       con.r_owner,\n       con.r_constraint_name,\n       par.owner,\n       par.constraint_name,\n       par.table_name\n),\nref_int_indexes AS (\nSELECT /*+ MATERIALIZE NO_MERGE */\n       r.owner,\n       r.constraint_name,\n       c.table_owner,\n       c.table_name,\n       c.index_owner,\n       c.index_name,\n       r.col_cnt\n  FROM ref_int_constraints r,\n       dba_ind_columns c,\n       dba_indexes i\n WHERE c.table_owner = r.owner\n   AND c.table_name = r.table_name\n   AND c.column_position <= r.col_cnt\n   AND c.column_name IN (r.col_01, r.col_02, r.col_03, r.col_04, r.col_05, r.col_06, r.col_07, r.col_08,\n                         r.col_09, r.col_10, r.col_11, r.col_12, r.col_13, r.col_14, r.col_15, r.col_16)\n   AND i.owner = c.index_owner\n   AND i.index_name = c.index_name\n   AND i.table_owner = c.table_owner\n   AND i.table_name = c.table_name\n   AND i.index_type != 'BITMAP'\n GROUP BY\n       r.owner,\n       r.constraint_name,\n       c.table_owner,\n       c.table_name,\n       c.index_owner,\n       c.index_name,\n       r.col_cnt\nHAVING COUNT(*) = r.col_cnt\n)\nSELECT /*+ NO_MERGE */\n       owner,table_name,CONSTRAINT_NAME\n  FROM ref_int_constraints c\n WHERE NOT EXISTS (\nSELECT NULL\n  FROM ref_int_indexes i\n WHERE i.owner = c.owner\n   AND i.constraint_name = c.constraint_name\n)\n ", '', {}, '')
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        self.result_raw = [' ' + x[0] + '.' + x[1] + ' :' + str(x[2]) + ',' for x in resultSet]

    def is_failed(self):
        return self.result_raw.__len__() > 0

    def set_result(self):
        self.result = ',,,' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          ':\n        \n' + ('\n        \n').join(self.result_raw)]}
        self.exe_advise = {}


class Check_Shared_Pool_Shrink(Oracle_Performance_Rule):

    def __init__(self, id, name):
        super(Check_Shared_Pool_Shrink, self).__init__("SELECT\n       COMPONENT,\n       OPER_TYPE,\n       OPER_MODE,\n       PARAMETER,\n       TO_CHAR(INITIAL_SIZE/1024/1024,'999,999') as S_SIZ_MB,\n       TO_CHAR(TARGET_SIZE/1024/1024,'999,999') as T_SIZ_MB,\n       TO_CHAR(FINAL_SIZE/1024/1024,'999,999') as E_SIZ_MB,\n       STATUS,\n       TO_CHAR(START_TIME,'DD-MM-YYYY HH24:MI:SS') as STIME,\n       TO_CHAR(END_TIME,'DD-MM-YYYY HH24:MI:SS') as ETIME\n     FROM\n       V$SGA_RESIZE_OPS where PARAMETER = 'shared_pool_size' and OPER_TYPE='SHRINK'", '', {}, '')
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        self.result_raw = ['shared pool (' + x[8] + ')(' + x[9] + ') ,(' + x[4].strip() + 'MB)(' + x[6].strip() + 'M)' + ',' for x in resultSet]

    def is_failed(self):
        return self.result_raw.__len__() > 0

    def set_result(self):
        self.result = ',latch,' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          'SGA,(SGA_TARGET,MEMEORY_TARGET),SGA\n        \n' + ('\n        \n').join(self.result_raw)]}
        self.exe_advise = {}


class Check_NoPk_Table(Oracle_Performance_Rule):

    def __init__(self, id, name):
        super(Check_NoPk_Table, self).__init__(" SELECT D.OWNER, d.table_name, d.NUM_ROWS\n   FROM dba_TABLES d\n  WHERE not exists (SELECT 1\n           FROM dba_constraints dc\n          WHERE dc.constraint_type = 'P'\n            AND  dc.table_name = d.TABLE_NAME\n            AND  dc.owner = d.OWNER)\n    AND  d.OWNER NOT LIKE '%SYS%'\n    AND  owner NOT IN ('SI_INFORMTN_SCHEMA', 'SQLTXADMIN', 'SQLTXPLAIN',\n                          'SYS',\n                          'SYSMAN', 'SYSTEM', 'TRCANLZR', 'WMSYS',\n                          'XDB', 'XS$NULL', 'PERFSTAT', 'STDBYPERF',\n                          'ANONYMOUS', 'APEX_030200', 'APEX_040000', 'APEX_SSO',\n                          'APPQOSSYS', 'CTXSYS', 'DBSNMP', 'DIP',\n                          'EXFSYS', 'FLOWS_FILES', 'MDSYS', 'OLAPSYS',\n                          'ORACLE_OCM', 'ORDDATA', 'ORDPLUGINS', 'ORDSYS',\n                          'OUTLN', 'OWBSYS')\n          AND  owner  NOT IN ('SI_INFORMTN_SCHEMA', 'SQLTXADMIN', 'SQLTXPLAIN',\n                          'SYS',\n                          'SYSMAN', 'SYSTEM', 'TRCANLZR', 'WMSYS',\n                          'XDB', 'XS$NULL', 'PERFSTAT', 'STDBYPERF',\n                          'ANONYMOUS', 'APEX_030200', 'APEX_040000', 'APEX_SSO',\n                          'APPQOSSYS', 'CTXSYS', 'DBSNMP', 'DIP',\n                          'EXFSYS', 'FLOWS_FILES', 'MDSYS', 'OLAPSYS',\n                          'ORACLE_OCM', 'ORDDATA', 'ORDPLUGINS', 'ORDSYS',\n                          'OUTLN', 'OWBSYS')\n    AND  D.NUM_ROWS >= 100000\n  ORDER BY d.NUM_ROWS desc", '10W', {}, '')
        self.priority = ''
        self.score = 5
        self.total_score = 5
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        self.result_raw = ['(' + x[0] + '.' + x[1] + ') (' + str(x[2]) + '),' for x in resultSet]

    def is_failed(self):
        return self.result_raw.__len__() > 0

    def set_result(self):
        self.result = '(' + str(self.result_raw.__len__()) + ') ,' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          ',,:\n        \n' + ('\n        \n').join(self.result_raw)]}
        self.exe_advise = {}


class Check_Large_Table_NoPartition(Oracle_Performance_Rule):

    def __init__(self, id, name):
        super(Check_Large_Table_NoPartition, self).__init__(" SELECT owner,\n       table_name,\n       NUM_ROWS\n  FROM dba_tables\nwhere  owner  NOT IN ('SI_INFORMTN_SCHEMA', 'SQLTXADMIN', 'SQLTXPLAIN',\n                          'SYS',\n                          'SYSMAN', 'SYSTEM', 'TRCANLZR', 'WMSYS',\n                          'XDB', 'XS$NULL', 'PERFSTAT', 'STDBYPERF',\n                          'ANONYMOUS', 'APEX_030200', 'APEX_040000', 'APEX_SSO',\n                          'APPQOSSYS', 'CTXSYS', 'DBSNMP', 'DIP',\n                          'EXFSYS', 'FLOWS_FILES', 'MDSYS', 'OLAPSYS',\n                          'ORACLE_OCM', 'ORDDATA', 'ORDPLUGINS', 'ORDSYS',\n                          'OUTLN', 'OWBSYS')\n      and table_name not in (select distinct table_name from DBA_TAB_PARTITIONS)\n      and  NUM_ROWS > 5e7\nORDER BY NUM_ROWS desc", '5', {}, '')
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        self.result_raw = ['(' + x[0] + '.' + x[1] + ') (' + str(x[2]) + '),' for x in resultSet]

    def is_failed(self):
        return self.result_raw.__len__() > 0

    def set_result(self):
        self.result = '(' + str(self.result_raw.__len__()) + ') ,' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          ',:\n        \n' + ('\n        \n').join(self.result_raw)]}
        self.exe_advise = {}


class Check_Large_Table_No_Index(Oracle_Performance_Rule):

    def __init__(self, id, name):
        super(Check_Large_Table_No_Index, self).__init__(" SELECT owner,\n       segment_name,\n       round(bytes / 1024 / 1024 / 1024, 3)\nFROM   dba_segments\nWHERE  segment_type = 'TABLE'\nAND    segment_name NOT IN (SELECT table_name FROM dba_indexes)\nAND    bytes / 1024 / 1024 / 1024  >= 1\nand  owner NOT IN ('ANONYMOUS','APEX_030200','APEX_040000','APEX_SSO','APPQOSSYS','CTXSYS','DBSNMP','DIP','EXFSYS','FLOWS_FILES','MDSYS','OLAPSYS','ORACLE_OCM','ORDDATA','ORDPLUGINS','ORDSYS','OUTLN','OWBSYS','SI_INFORMTN_SCHEMA','SQLTXADMIN','SQLTXPLAIN','SYS','SYSMAN','SYSTEM','TRCANLZR','WMSYS','XDB','XS$NULL','PERFSTAT','STDBYPERF')\nORDER  BY bytes DESC", '1G', {}, '')
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        self.result_raw = ['(' + x[0] + '.' + x[1] + ')(' + str(x[2]) + ')G,' for x in resultSet]

    def is_failed(self):
        return self.result_raw.__len__() > 0

    def set_result(self):
        self.result = '(' + str(self.result_raw.__len__()) + ') ,' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          ',SQL,:\n        \n' + ('\n        \n').join(self.result_raw)]}
        self.exe_advise = {}


class Check_Unused_Indexes(Oracle_Performance_Rule):

    def __init__(self, id, name):
        super(Check_Unused_Indexes, self).__init__("WITH\nobjects AS (\nSELECT /*+ MATERIALIZE NO_MERGE */\n       object_id,\n       owner,\n       object_name\n  FROM dba_objects\n WHERE object_type LIKE 'INDEX%'\n   AND owner NOT IN ('ANONYMOUS','APEX_030200','APEX_040000','APEX_SSO','APPQOSSYS','CTXSYS','DBSNMP','DIP','EXFSYS','FLOWS_FILES','MDSYS','OLAPSYS','ORACLE_OCM','ORDDATA','ORDPLUGINS','ORDSYS','OUTLN','OWBSYS','SI_INFORMTN_SCHEMA','SQLTXADMIN','SQLTXPLAIN','SYS','SYSMAN','SYSTEM','TRCANLZR','WMSYS','XDB','XS$NULL','PERFSTAT','STDBYPERF')\n),\nash_mem AS (\nSELECT /*+ MATERIALIZE NO_MERGE */\n       DISTINCT current_obj#\n  FROM gv$active_session_history\n WHERE sql_plan_operation = 'INDEX'\n   AND current_obj# > 0\n),\nash_awr AS (\nSELECT /*+ MATERIALIZE NO_MERGE DYNAMIC_SAMPLING(4) */\n       DISTINCT current_obj#\n  FROM dba_hist_active_sess_history\n WHERE sql_plan_operation = 'INDEX'\n   AND snap_id BETWEEN 27284 AND 27498\n   AND dbid = 646749667\n   AND current_obj# > 0\n),\nsql_mem AS (\nSELECT /*+ MATERIALIZE NO_MERGE DYNAMIC_SAMPLING(4) */\n       DISTINCT object_owner, object_name\n  FROM gv$sql_plan\nWHERE operation = 'INDEX'\n),\nsql_awr AS (\nSELECT /*+ MATERIALIZE NO_MERGE DYNAMIC_SAMPLING(4) */\n       DISTINCT object_owner, object_name\n  FROM dba_hist_sql_plan\n WHERE operation = 'INDEX' AND dbid = 646749667\n)\nSELECT /*+ NO_MERGE */\n       i.table_owner,\n       i.table_name,\n       i.index_name\n  FROM dba_indexes i\n WHERE (index_type LIKE 'NORMAL%' OR index_type = 'BITMAP'  OR index_type LIKE 'FUNCTION%')\n   AND i.table_owner NOT IN ('ANONYMOUS','APEX_030200','APEX_040000','APEX_040200','DVSYS','LBACSYS','OJVMSYS','APEX_SSO','APPQOSSYS','CTXSYS','DBSNMP','DIP','EXFSYS','FLOWS_FILES','MDSYS','OLAPSYS','ORACLE_OCM','ORDDATA','ORDPLUGINS','ORDSYS','OUTLN','OWBSYS','SI_INFORMTN_SCHEMA','SQLTXADMIN','SQLTXPLAIN','SYS','SYSMAN','SYSTEM','TRCANLZR','WMSYS','XDB','XS$NULL','PERFSTAT','STDBYPERF','SCOTT')\n   AND (i.owner, i.index_name) NOT IN ( SELECT o.owner, o.object_name FROM ash_mem a, objects o WHERE o.object_id = a.current_obj# )\n   AND (i.owner, i.index_name) NOT IN ( SELECT o.owner, o.object_name FROM ash_awr a, objects o WHERE o.object_id = a.current_obj# )\n   AND (i.owner, i.index_name) NOT IN ( SELECT object_owner, object_name FROM sql_mem)\n   AND (i.owner, i.index_name) NOT IN ( SELECT object_owner, object_name FROM sql_awr)\n ORDER BY\n       i.table_owner,\n       i.table_name,\n       i.index_name", ' ', {}, '')
        self.priority = ''
        self.score = 5
        self.total_score = 5
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        self.result_raw = ['alter index ' + x[0] + '.' + x[2] + ' monitoring usage; ' for x in resultSet]

    def is_failed(self):
        return self.result_raw.__len__() > 0

    def set_result(self):
        self.result = ',DML,' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          ',,invisible,drop\n:\n' + ('\n\n').join(self.result_raw)]}
        self.exe_advise = {}


class Check_Indexes_Count(Oracle_Performance_Rule):

    def __init__(self, id, name):
        super(Check_Indexes_Count, self).__init__("SELECT /*+ NO_MERGE */\n       COUNT(*) indexes,\n       table_owner,\n       table_name\n  FROM dba_indexes\n WHERE table_owner NOT IN ('ANONYMOUS','APEX_030200','APEX_040000','APEX_040200','DVSYS','LBACSYS','OJVMSYS','APEX_SSO','APPQOSSYS','CTXSYS','DBSNMP','DIP','EXFSYS','FLOWS_FILES','MDSYS','OLAPSYS','ORACLE_OCM','ORDDATA','ORDPLUGINS','ORDSYS','OUTLN','OWBSYS','SI_INFORMTN_SCHEMA','SQLTXADMIN','SQLTXPLAIN','SYS','SYSMAN','SYSTEM','TRCANLZR','WMSYS','XDB','XS$NULL','PERFSTAT','STDBYPERF')\n GROUP BY\n       table_owner,\n       table_name\nHAVING COUNT(*) > 8\n ORDER BY\n       1 DESC", '8', {}, '')
        self.priority = ''
        self.score = 5
        self.total_score = 5
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        self.result_raw = [' ' + x[1] + '.' + x[2] + ' :' + str(x[0]) + ',' for x in resultSet]

    def is_failed(self):
        return self.result_raw.__len__() > 0

    def set_result(self):
        self.result = '8,DML,' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          'SQL,\n        :' + ('\n        \n').join(self.result_raw)]}
        self.exe_advise = {}


class Check_Redo_Isolation(Oracle_Performance_Rule):

    def __init__(self, id, name):
        super(Check_Redo_Isolation, self).__init__("select distinct\n    case when INSTR(file_name,'/') > 0 then\n        case when file_name like '+%' then\n            SUBSTR(file_name,0,(INSTR(file_name,'/',1,1)))\n        else\n            SUBSTR(file_name,0,(INSTR(file_name,'/',-1,1)))\n        end\n    else\n        case when file_name like '+%' then\n            SUBSTR(file_name,0,(INSTR(file_name,'',1,1)))\n        else\n            SUBSTR(file_name,0,(INSTR(file_name,'',-1,1)))\n        end\n    end\nfrom dba_data_files\nintersect\nselect distinct\n    case when INSTR(member,'/') > 0 then\n        case when member like '+%' then\n            SUBSTR(member,0,(INSTR(member,'/',1,1)))\n        else\n            SUBSTR(member,0,(INSTR(member,'/',-1,1)))\n        end\n    else\n        case when member like '+%' then\n            SUBSTR(member,0,(INSTR(member,'',1,1)))\n        else\n            SUBSTR(member,0,(INSTR(member,'',-1,1)))\n        end\n    end\nfrom v$logfile", ' Redo ', {}, 'Redo ')
        self.priority = ''
        self.score = 5
        self.total_score = 5
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        self.result_raw = ['redo :' + x[0] for x in resultSet]

    def is_failed(self):
        return self.result_raw.__len__() > 0

    def set_result(self):
        self.result = 'REDO,REDO,DML' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          'REDO\n        :\n        \n' + ('\n        \n').join(self.result_raw)]}
        self.exe_advise = {}


class Check_Sequence_Cache(Oracle_Performance_Rule):

    def __init__(self, id, name):
        super(Check_Sequence_Cache, self).__init__("SELECT\n       s.SEQUENCE_OWNER,SEQUENCE_NAME,CACHE_SIZE\nfrom dba_sequences s\nwhere\n   s.sequence_owner not in ('ANONYMOUS','APEX_030200','APEX_040000','APEX_040200','DVSYS','LBACSYS','OJVMSYS','APEX_SSO','APPQOSSYS','CTXSYS','DBSNMP','DIP','EXFSYS','FLOWS_FILES','MDSYS','OLAPSYS','ORACLE_OCM','ORDDATA','ORDPLUGINS','ORDSYS','OUTLN','OWBSYS','SI_INFORMTN_SCHEMA','SQLTXADMIN','SQLTXPLAIN','SYS','SYSMAN','SYSTEM','TRCANLZR','WMSYS','XDB','XS$NULL','PERFSTAT','STDBYPERF')\nand s.max_value > 0\nand s.CACHE_SIZE < 100", '', {}, '')
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        self.result_raw = [' ' + x[0] + '.' + x[1] + ' :' + str(x[2]) + ',' for x in resultSet]

    def is_failed(self):
        return self.result_raw.__len__() > 0

    def set_result(self):
        self.result = ',,' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          ',5000\n        \n' + ('\n        \n').join(self.result_raw)]}
        self.exe_advise = {}


class Check_Pessimistic_Lock(Oracle_Performance_Rule):

    def __init__(self, id, name):
        super(Check_Pessimistic_Lock, self).__init__("select distinct SQL_ID from v$sql where (SQL_TEXT like 'select%for update' or SQL_TEXT like 'SELECT%FOR UPDATE') and PARSING_SCHEMA_NAME not in ('ANONYMOUS','APEX_030200','APEX_040000','APEX_SSO','APPQOSSYS','CTXSYS','DBSNMP','DIP','EXFSYS','FLOWS_FILES','MDSYS','OLAPSYS','ORACLE_OCM','ORDDATA','ORDPLUGINS','ORDSYS','OUTLN','OWBSYS','SI_INFORMTN_SCHEMA','SQLTXADMIN','SQLTXPLAIN','SYS','SYSMAN','SYSTEM','TRCANLZR','WMSYS','XDB','XS$NULL','PERFSTAT','STDBYPERF')", 'SQL', {}, '')
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        self.result_raw = ['SQL_ID (' + x[0] + '),' for x in resultSet]

    def is_failed(self):
        return self.result_raw.__len__() > 0

    def set_result(self):
        self.result = 'SQLselect for update,,' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          'SQL,SQL_id:\n        \n' + ('\n        \n').join(self.result_raw)]}
        self.exe_advise = {}


class Check_Table_Waste_Space(Oracle_Performance_Rule):

    def __init__(self, id, name):
        super(Check_Table_Waste_Space, self).__init__("select * from (\nselect a.owner,\n a.table_name,\n a.num_rows,\n a.avg_row_len * a.num_rows,\n sum(b.bytes/1024/1024/1024) sg,\n (a.avg_row_len * a.num_rows) / sum(b.bytes) frag\n from dba_tables a, dba_segments b\n where a.table_name = b.segment_name\nand a.owner= b.owner\n and a.owner not in\n ('ANONYMOUS','APEX_030200','APEX_040000','APEX_SSO','APPQOSSYS','CTXSYS','DBSNMP','DIP','EXFSYS','FLOWS_FILES','MDSYS','OLAPSYS','ORACLE_OCM','ORDDATA','ORDPLUGINS','ORDSYS','OUTLN','OWBSYS','SI_INFORMTN_SCHEMA','SQLTXADMIN','SQLTXPLAIN','SYS','SYSMAN','SYSTEM','TRCANLZR','WMSYS','XDB','XS$NULL','PERFSTAT','STDBYPERF')\n group by a.owner,a.table_name,a.avg_row_len, a.num_rows\n having a.avg_row_len * a.num_rows / sum(b.bytes) < 0.7\n order by sum(b.bytes/1024/1024/1024) desc)\nwhere sg > 1 and rownum <= 100", '', {}, '')
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        self.result_raw = ['' + x[0] + '.' + x[1] + '' + str(x[4]) + 'G,' + ':' + str(round(x[5], 2)) for x in resultSet]

    def is_failed(self):
        return self.result_raw.__len__() > 0

    def set_result(self):
        self.result = ',,,' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          ':\n        \n' + ('\n        \n').join(self.result_raw)]}
        self.exe_advise = {}


class Check_Recycle_Bin_Objects(Oracle_Performance_Rule):

    def __init__(self, id, name):
        super(Check_Recycle_Bin_Objects, self).__init__("SELECT ORIGINAL_NAME,TYPE,OWNER\n  FROM dba_recyclebin\n WHERE owner NOT IN ('ANONYMOUS','APEX_030200','APEX_040000','APEX_SSO','APPQOSSYS','CTXSYS','DBSNMP','DIP','EXFSYS','FLOWS_FILES','MDSYS','OLAPSYS','ORACLE_OCM','ORDDATA','ORDPLUGINS','ORDSYS','OUTLN','OWBSYS')\n   AND owner NOT IN ('SI_INFORMTN_SCHEMA','SQLTXADMIN','SQLTXPLAIN','SYS','SYSMAN','SYSTEM','TRCANLZR','WMSYS','XDB','XS$NULL','PERFSTAT','STDBYPERF')\n ORDER BY\n       owner,\n       object_name", '', {}, '')
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        self.result_raw = [':(' + x[1] + '): ' + x[2] + '.' + x[0] + ',' for x in resultSet]

    def is_failed(self):
        return self.result_raw.__len__() > 10000

    def set_result(self):
        self.result = '' + str(self.result_raw.__len__()) + ',,' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          ',:\n        \n' + ('\n        \n').join(self.result_raw)]}
        self.exe_advise = {}


class Check_Table_Missing_Statistics(Oracle_Performance_Rule):

    def __init__(self, id, name):
        super(Check_Table_Missing_Statistics, self).__init__("SELECT /*+ NO_MERGE */\n       s.owner, s.table_name, s.stale_stats, to_char(s.last_analyzed,'YYYY/MM/DD HH24:MI:SS')\n  FROM dba_tab_statistics s,\n       dba_tables t\n WHERE s.object_type = 'TABLE'\n   AND s.owner NOT IN ('ANONYMOUS','APEX_030200','APEX_040000','APEX_SSO','APPQOSSYS','CTXSYS','DBSNMP','DIP','EXFSYS','FLOWS_FILES','MDSYS','OLAPSYS','ORACLE_OCM','ORDDATA','ORDPLUGINS','ORDSYS','OUTLN','OWBSYS','SI_INFORMTN_SCHEMA','SQLTXADMIN','SQLTXPLAIN','SYS','SYSMAN','SYSTEM','TRCANLZR','WMSYS','XDB','XS$NULL','PERFSTAT','STDBYPERF')\n   AND (s.last_analyzed IS NULL or  s.stale_stats = 'YES' or s.last_analyzed < sysdate -7)\n   AND s.table_name NOT LIKE 'BIN%'\n   AND NOT (s.table_name LIKE '%TEMP' OR s.table_name LIKE '%_TEMP_%')\n   AND t.owner = s.owner\n   AND t.table_name = s.table_name\n   AND t.temporary = 'N'\n   AND NOT EXISTS (\nSELECT NULL\n  FROM dba_external_tables e\n WHERE e.owner = s.owner\n   AND e.table_name = s.table_name\n)\n ORDER BY\n       s.owner, s.table_name", '//', {}, '')
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        self.result_raw = ['(' + x[0] + '.' + x[1] + ')' + ('/,:(' + str(x[3]) + ')' if x[3] is not None else '') for x in resultSet]

    def is_failed(self):
        return self.result_raw.__len__() > 0

    def set_result(self):
        self.result = '//,SQLCBO,' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          ':\n        \n' + ('\n        \n').join(self.result_raw)]}
        self.exe_advise = {}


class Check_Triggers(Oracle_Performance_Rule):

    def __init__(self, id, name):
        super(Check_Triggers, self).__init__("\nSELECT *\n  FROM (SELECT OWNER,\n               TRIGGER_NAME,\n               TABLE_NAME,\n               d.trigger_type,\n               d.triggering_event,\n               d.when_clause,\n               TRIGGER_BODY,\n               DENSE_RANK() over(partition by d.owner ORDER BY d.trigger_name) o\n          FROM dba_triggers d\n         WHERE owner NOT IN ('ANONYMOUS','APEX_030200','APEX_040000','APEX_SSO','APPQOSSYS','CTXSYS','DBSNMP','DIP','EXFSYS','FLOWS_FILES','MDSYS','OLAPSYS','ORACLE_OCM','ORDDATA','ORDPLUGINS','ORDSYS','OUTLN','OWBSYS','SI_INFORMTN_SCHEMA','SQLTXADMIN','SQLTXPLAIN','SYS','SYSMAN','SYSTEM','TRCANLZR','WMSYS','XDB','XS$NULL','PERFSTAT','STDBYPERF')\n           AND  owner NOT LIKE '%SYS%'\n        ) wd\n WHERE o <= 10\n ORDER BY wd.owner", '', {}, '')
        self.priority = ''
        self.score = 5
        self.total_score = 5
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        self.result_raw = [':' + x[0] + '.' + x[1] + ' :' + x[2] + ' :' + x[4] + ' : \n' + x[-2] for x in resultSet]

    def is_failed(self):
        return self.result_raw.__len__() > 0

    def set_result(self):
        self.result = '' + str(self.result_raw.__len__()) + ',' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          ',:\n        \n' + ('\n        \n').join(self.result_raw)]}
        self.exe_advise = {}


class Check_Invaild_Triggers(Oracle_Secure_Rule):

    def __init__(self, id, name):
        super(Check_Invaild_Triggers, self).__init__("\nSELECT OWNER,\n               TRIGGER_NAME,\n               TABLE_NAME,\n               trigger_type,\n               triggering_event,\n               when_clause,\n               TRIGGER_BODY\n          from dba_triggers where status='DISABLED' and owner not in  ('ANONYMOUS','APEX_030200','APEX_040000','APEX_SSO','APPQOSSYS','CTXSYS','DBSNMP','DIP','EXFSYS','FLOWS_FILES','MDSYS','OLAPSYS','ORACLE_OCM','ORDDATA','ORDPLUGINS','ORDSYS','OUTLN','OWBSYS','SI_INFORMTN_SCHEMA','SQLTXADMIN','SQLTXPLAIN','SYS','SYSMAN','SYSTEM','TRCANLZR','WMSYS','XDB','XS$NULL','PERFSTAT','STDBYPERF')", '', {}, '')
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        self.result_raw = [':' + x[0] + '.' + x[1] + ' :' + str(x[2]) + ' :' + str(x[4]) + ' : \n' + str(x[-1]) for x in resultSet]

    def is_failed(self):
        return self.result_raw.__len__() > 0

    def set_result(self):
        self.result = '' + str(self.result_raw.__len__()) + ',' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          ',:\n        \n' + ('\n        \n').join(self.result_raw)]}
        self.exe_advise = {}


class Check_Invaild_Constraints(Oracle_Secure_Rule):

    def __init__(self, id, name):
        super(Check_Invaild_Constraints, self).__init__("\nselect   owner,constraint_name,constraint_type,\n               table_name,status,deferred,delete_rule\n          from dba_constraints where status='DISABLED' and table_name  not like 'BIN$%' and owner not in  ('ANONYMOUS','APEX_030200','APEX_040000','APEX_SSO','APPQOSSYS','CTXSYS','DBSNMP','DIP','EXFSYS','FLOWS_FILES','MDSYS','OLAPSYS','ORACLE_OCM','ORDDATA','ORDPLUGINS','ORDSYS','OUTLN','OWBSYS','SI_INFORMTN_SCHEMA','SQLTXADMIN','SQLTXPLAIN','SYS','SYSMAN','SYSTEM','TRCANLZR','WMSYS','XDB','XS$NULL','PERFSTAT','STDBYPERF')", '', {}, '')
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        self.result_raw = [':' + x[0] + '.' + x[1] + ' :' + str(x[3]) + ' :' + x[2] for x in resultSet]

    def is_failed(self):
        return self.result_raw.__len__() > 0

    def set_result(self):
        self.result = '' + str(self.result_raw.__len__()) + ',' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          ':\n        \n' + ('\n        \n').join(self.result_raw)]}
        self.exe_advise = {}


class Check_Index_Missing_Statistics(Oracle_Performance_Rule):

    def __init__(self, id, name):
        super(Check_Index_Missing_Statistics, self).__init__("\nSELECT /*+ NO_MERGE */\n       s.owner, s.table_name, s.index_name, s.stale_stats, to_char(s.last_analyzed,'YYYY/MM/DD HH24:MI:SS')\n  FROM dba_ind_statistics s,\n       dba_indexes t\n WHERE s.OBJECT_TYPE = 'INDEX'\n   AND s.owner NOT IN ('ANONYMOUS','APEX_030200','APEX_040000','APEX_SSO','APPQOSSYS','CTXSYS','DBSNMP','DIP','EXFSYS','FLOWS_FILES','MDSYS','OLAPSYS','ORACLE_OCM','ORDDATA','ORDPLUGINS','ORDSYS','OUTLN','OWBSYS','SI_INFORMTN_SCHEMA','SQLTXADMIN','SQLTXPLAIN','SYS','SYSMAN','SYSTEM','TRCANLZR','WMSYS','XDB','XS$NULL','PERFSTAT','STDBYPERF')\n   AND (s.last_analyzed IS NULL or  s.stale_stats = 'YES' or s.last_analyzed < sysdate -7)\n   AND s.table_name NOT LIKE 'BIN%'\n   AND NOT (s.table_name LIKE '%TEMP' OR s.table_name LIKE '%_TEMP_%' )\n   AND t.owner = s.owner\n   AND t.index_name = s.INDEX_NAME\n   AND t.table_name = s.table_name\n   AND t.temporary = 'N'\n   and t.index_type != 'LOB'\n   AND NOT EXISTS (\nSELECT NULL\n  FROM dba_external_tables e\n WHERE e.owner = s.owner\n   AND e.table_name = s.table_name\n)\n ORDER BY\n       s.owner, s.table_name", '//', {}, '')
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        self.result_raw = ['' + x[0] + '.' + x[1] + '(' + x[2] + ')' + (',:(' + str(x[4]) + ')' if x[4] is not None else '') for x in resultSet]

    def is_failed(self):
        return self.result_raw.__len__() > 0

    def set_result(self):
        self.result = '//,SQLCBO,' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          ':\n        \n' + ('\n        \n').join(self.result_raw)]}
        self.exe_advise = {}


class Check_Temptable_With_Statistics(Oracle_Performance_Rule):

    def __init__(self, id, name):
        super(Check_Temptable_With_Statistics, self).__init__("SELECT /*+ NO_MERGE */\n       s.owner, s.table_name\n  FROM dba_tab_statistics s,\n       dba_tables t\n WHERE s.object_type = 'TABLE'\n   AND s.owner NOT IN ('ANONYMOUS','APEX_030200','APEX_040000','APEX_SSO','APPQOSSYS','CTXSYS','DBSNMP','DIP','EXFSYS','FLOWS_FILES','MDSYS','OLAPSYS','ORACLE_OCM','ORDDATA','ORDPLUGINS','ORDSYS','OUTLN','OWBSYS','SI_INFORMTN_SCHEMA','SQLTXADMIN','SQLTXPLAIN','SYS','SYSMAN','SYSTEM','TRCANLZR','WMSYS','XDB','XS$NULL','PERFSTAT','STDBYPERF')\n   AND s.last_analyzed IS NOT NULL\n   /*AND s.stale_stats = 'YES'*/\n   AND (s.table_name LIKE '%TEMP' OR s.table_name LIKE '%_TEMP_%' )\n   AND s.table_name NOT LIKE 'BIN%'\n   AND t.owner = s.owner\n   AND t.table_name = s.table_name\n   AND NOT EXISTS (\nSELECT NULL\n  FROM dba_external_tables e\n WHERE e.owner = s.owner\n   AND e.table_name = s.table_name\n)\n ORDER BY\n       s.owner, s.table_name", '', {}, '')
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        self.result_raw = [' ' + x[0] + '.' + x[1] + ',' for x in resultSet]

    def is_failed(self):
        return self.result_raw.__len__() > 0

    def set_result(self):
        self.result = ',SQLCBO,' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          ',:\n        \n' + ('\n        \n').join(self.result_raw)]}
        self.exe_advise = {}


class Check_Invalid_Objects(Oracle_Secure_Rule):

    def __init__(self, id, name):
        super(Check_Invalid_Objects, self).__init__("select OWNER,OBJECT_NAME FROM dba_objects WHERE status = 'INVALID' AND owner NOT IN ('ANONYMOUS','APEX_030200','APEX_040000','APEX_SSO','APPQOSSYS','CTXSYS','DBSNMP','DIP','EXFSYS','FLOWS_FILES','MDSYS','OLAPSYS','ORACLE_OCM','ORDDATA','ORDPLUGINS','ORDSYS','OUTLN','OWBSYS','SI_INFORMTN_SCHEMA','SQLTXADMIN','SQLTXPLAIN','SYS','SYSMAN','SYSTEM','TRCANLZR','WMSYS','XDB','XS$NULL','PERFSTAT','STDBYPERF')", ' ', {}, '')
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        self.result_raw = [':' + x[0] + '.' + x[1] + ',' for x in resultSet]

    def is_failed(self):
        return self.result_raw.__len__() > 0

    def set_result(self):
        self.result = ',' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          ',:\n        \n' + ('\n        \n').join(self.result_raw)]}
        self.exe_advise = {}


class Check_Invalid_PartionIndex(Oracle_Secure_Rule):

    def __init__(self, id, name):
        super(Check_Invalid_PartionIndex, self).__init__("\nSELECT t2.owner,\n       t1.INDEX_NAME,\n       t2.table_name,\n       t1.PARTITION_NAME,\n       t1.STATUS\n  FROM dba_ind_partitions t1, dba_indexes t2\nwhere t1.index_name = t2.index_name\n   AND  t1.STATUS = 'UNUSABLE'\n AND  owner NOT IN ('SI_INFORMTN_SCHEMA', 'SQLTXADMIN', 'SQLTXPLAIN',\n                          'SYS',\n                          'SYSMAN', 'SYSTEM', 'TRCANLZR', 'WMSYS',\n                          'XDB', 'XS$NULL', 'PERFSTAT', 'STDBYPERF',\n                          'ANONYMOUS', 'APEX_030200', 'APEX_040000', 'APEX_SSO',\n                          'APPQOSSYS', 'CTXSYS', 'DBSNMP', 'DIP',\n                          'EXFSYS', 'FLOWS_FILES', 'MDSYS', 'OLAPSYS',\n                          'ORACLE_OCM', 'ORDDATA', 'ORDPLUGINS', 'ORDSYS',\n                          'OUTLN', 'OWBSYS')", '', {}, '')
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        self.result_raw = ['(' + x[0] + '.' + x[2] + ')(' + x[3] + '):' + x[1] + ' ' for x in resultSet]

    def is_failed(self):
        return self.result_raw.__len__() > 0

    def set_result(self):
        self.result = ',,' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          ',:\n        \n' + ('\n        \n').join(self.result_raw)]}
        self.exe_advise = {}


class Check_DG(Oracle_Secure_Rule):

    def __init__(self, id, name):
        super(Check_DG, self).__init__("\nSELECT case\n         WHEN d.VALUE is null then\n          'NO'\n         else\n          d.VALUE\n       end DG_INFO\n  FROM v$parameter d\n WHERE d.NAME = 'log_archive_config'\n ", 'DG ', {}, 'DG')
        self.set_id_and_db_name(id, name)

    def is_failed(self):
        return self.result_raw == 'NO'

    def set_result_raw(self, resultSet):
        self.result_raw = resultSet[0][0]

    def set_result(self):
        self.result = 'DG,' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          'ADG,,\n        \n']}
        self.exe_advise = {}


class Check_DG_GAP(Oracle_Secure_Rule):

    def __init__(self, id, name):
        super(Check_DG_GAP, self).__init__("\n            SELECT a.thread#,  b.last_seq-a.applied_seq ARC_DIFF, dest_name\n FROM\n        (SELECT  thread#, dest_name, MAX(sequence#) applied_seq, MAX(next_time) last_app_timestamp\n        FROM    gv$archived_log log,\n                v$ARCHIVE_DEST dest WHERE log.applied = 'YES' and dest.dest_name is not null and log.dest_id = dest.dest_id GROUP BY dest.dest_name, thread#) a,\n        (SELECT  thread#, MAX (sequence#) last_seq FROM gv$archived_log GROUP BY thread#) b\nWHERE a.thread# = b.thread#  and  b.last_seq-a.applied_seq > 5\n ", 'DGDG ', {}, 'DG')
        self.priority = ''
        self.score = 20
        self.total_score = 20
        self.set_id_and_db_name(id, name)

    def is_failed(self):
        return self.result_raw.__len__() > 0

    def set_result_raw(self, resultSet):
        self.result_raw = [' :' + str(x[0]) + '(' + x[2] + ')SEQ :' + str(x[1]) for x in resultSet]

    def set_result(self):
        self.result = 'DGGAP,' if self.is_failed() else ''

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          'ADG,:\n        \n' + ('\n        \n').join(self.result_raw)]}
        self.exe_advise = {}


class Check_Unusable_Index(Oracle_Secure_Rule):

    def __init__(self, id, name):
        super(Check_Unusable_Index, self).__init__("select owner, index_name from dba_indexes where status = 'UNUSABLE' ", ' ', {}, '')
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        self.result_raw = [' ' + x[0] + '.' + x[1] + ',' for x in resultSet]

    def is_failed(self):
        return self.result_raw.__len__() > 0

    def set_result(self):
        self.result = ',' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          ',:\n        \n' + ('\n        \n').join(self.result_raw)]}
        self.exe_advise = {}


class Check_Block_Curruption(Oracle_Secure_Rule):

    def __init__(self, id, name):
        super(Check_Block_Curruption, self).__init__('select file#,block# from v$database_block_corruption', '', {}, '')
        self.priority = ''
        self.score = 20
        self.total_score = 20
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        self.result_raw = ['' + x[0] + ' :' + x[1] + ',' for x in resultSet]

    def is_failed(self):
        return self.result_raw.__len__() > 0

    def set_result(self):
        self.result = ',,' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          ',:\n        \n' + ('\n        \n').join(self.result_raw)]}
        self.exe_advise = {}


class Check_DBLinks(Oracle_Secure_Rule):

    def __init__(self, id, name):
        super(Check_DBLinks, self).__init__("SELECT\n   owner\n  , db_link\n  , username\n  , host\n  ,  TO_CHAR(CREATED, 'yyyy-mm-dd HH24:MI:SS')\nFROM dba_db_links\nORDER BY owner, db_link", 'DBLINK', {}, 'DBLINK')
        self.priority = ''
        self.score = 5
        self.total_score = 5
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        self.result_raw = ['DBLINK: :' + x[0] + ' :' + x[1] + ' :' + x[2] + ' :' + x[3] + ' :' + x[4] for x in resultSet]

    def is_failed(self):
        return self.result_raw.__len__() > 0

    def set_result(self):
        self.result = '' + str(self.result_raw.__len__()) + 'DBLINK ,DBLINK scn ' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          'DBLINK,SCN,dropDBLINK:\n        \n' + ('\n        \n').join(self.result_raw)]}
        self.exe_advise = {}


class Check_Nologging_Objects(Oracle_Secure_Rule):

    def __init__(self, id, name):
        super(Check_Nologging_Objects, self).__init__("WITH\nobjects AS (\nSELECT 1 record_type,\n       'TABLESPACE' object_type,\n       tablespace_name,\n       NULL owner,\n       NULL name,\n       NULL column_name,\n       NULL partition,\n       NULL subpartition\n  FROM dba_tablespaces\n WHERE logging = 'NOLOGGING'\n   AND contents != 'TEMPORARY'\nUNION ALL\nSELECT 2 record_type,\n       'TABLE' object_type,\n       tablespace_name,\n       owner,\n       table_name name,\n       NULL column_name,\n       NULL partition,\n       NULL subpartition\n  FROM dba_all_tables\n WHERE logging = 'NO'\n   AND temporary = 'N'\n   AND owner NOT IN ( 'SI_INFORMTN_SCHEMA', 'SQLTXADMIN', 'SQLTXPLAIN',\n                          'SYS',\n                          'SYSMAN', 'SYSTEM', 'TRCANLZR', 'WMSYS',\n                          'XDB', 'XS$NULL', 'PERFSTAT', 'STDBYPERF',\n                          'ANONYMOUS', 'APEX_030200', 'APEX_040000', 'APEX_SSO',\n                          'APPQOSSYS', 'CTXSYS', 'DBSNMP', 'DIP',\n                          'EXFSYS', 'FLOWS_FILES', 'MDSYS', 'OLAPSYS',\n                          'ORACLE_OCM', 'ORDDATA', 'ORDPLUGINS', 'ORDSYS',\n                          'OUTLN', 'OWBSYS' )\nUNION ALL\nSELECT 3 record_type,\n       'INDEX' object_type,\n       tablespace_name,\n       owner,\n       index_name name,\n       NULL column_name,\n       NULL partition,\n       NULL subpartition\n  FROM dba_indexes\n WHERE logging = 'NO'\n   AND temporary = 'N'\n   AND owner NOT IN ( 'SI_INFORMTN_SCHEMA', 'SQLTXADMIN', 'SQLTXPLAIN',\n                          'SYS',\n                          'SYSMAN', 'SYSTEM', 'TRCANLZR', 'WMSYS',\n                          'XDB', 'XS$NULL', 'PERFSTAT', 'STDBYPERF',\n                          'ANONYMOUS', 'APEX_030200', 'APEX_040000', 'APEX_SSO',\n                          'APPQOSSYS', 'CTXSYS', 'DBSNMP', 'DIP',\n                          'EXFSYS', 'FLOWS_FILES', 'MDSYS', 'OLAPSYS',\n                          'ORACLE_OCM', 'ORDDATA', 'ORDPLUGINS', 'ORDSYS',\n                          'OUTLN', 'OWBSYS' )\nUNION ALL\nSELECT 4 record_type,\n       'LOB' object_type,\n       tablespace_name,\n       owner,\n       table_name name,\n       SUBSTR(column_name, 1, 30) column_name,\n       NULL partition,\n       NULL subpartition\n  FROM dba_lobs\n WHERE logging = 'NO'\n AND owner NOT IN ( 'SI_INFORMTN_SCHEMA', 'SQLTXADMIN', 'SQLTXPLAIN',\n                          'SYS',\n                          'SYSMAN', 'SYSTEM', 'TRCANLZR', 'WMSYS',\n                          'XDB', 'XS$NULL', 'PERFSTAT', 'STDBYPERF',\n                          'ANONYMOUS', 'APEX_030200', 'APEX_040000', 'APEX_SSO',\n                          'APPQOSSYS', 'CTXSYS', 'DBSNMP', 'DIP',\n                          'EXFSYS', 'FLOWS_FILES', 'MDSYS', 'OLAPSYS',\n                          'ORACLE_OCM', 'ORDDATA', 'ORDPLUGINS', 'ORDSYS',\n                          'OUTLN', 'OWBSYS' )\nUNION ALL\nSELECT 5 record_type,\n       'TAB_PARTITION' object_type,\n       tablespace_name,\n       table_owner owner,\n       table_name name,\n       NULL column_name,\n       partition_name partition,\n       NULL subpartition\n  FROM dba_tab_partitions\n WHERE logging = 'NO'\n AND TABLE_OWNER NOT IN ( 'SI_INFORMTN_SCHEMA', 'SQLTXADMIN', 'SQLTXPLAIN',\n                          'SYS',\n                          'SYSMAN', 'SYSTEM', 'TRCANLZR', 'WMSYS',\n                          'XDB', 'XS$NULL', 'PERFSTAT', 'STDBYPERF',\n                          'ANONYMOUS', 'APEX_030200', 'APEX_040000', 'APEX_SSO',\n                          'APPQOSSYS', 'CTXSYS', 'DBSNMP', 'DIP',\n                          'EXFSYS', 'FLOWS_FILES', 'MDSYS', 'OLAPSYS',\n                          'ORACLE_OCM', 'ORDDATA', 'ORDPLUGINS', 'ORDSYS',\n                          'OUTLN', 'OWBSYS' )\nUNION ALL\nSELECT 6 record_type,\n       'IND_PARTITION' object_type,\n       tablespace_name,\n       index_owner owner,\n       index_name name,\n       NULL column_name,\n       partition_name partition,\n       NULL subpartition\n  FROM dba_ind_partitions\n WHERE logging = 'NO'\n AND INDEX_OWNER NOT IN ( 'SI_INFORMTN_SCHEMA', 'SQLTXADMIN', 'SQLTXPLAIN',\n                          'SYS',\n                          'SYSMAN', 'SYSTEM', 'TRCANLZR', 'WMSYS',\n                          'XDB', 'XS$NULL', 'PERFSTAT', 'STDBYPERF',\n                          'ANONYMOUS', 'APEX_030200', 'APEX_040000', 'APEX_SSO',\n                          'APPQOSSYS', 'CTXSYS', 'DBSNMP', 'DIP',\n                          'EXFSYS', 'FLOWS_FILES', 'MDSYS', 'OLAPSYS',\n                          'ORACLE_OCM', 'ORDDATA', 'ORDPLUGINS', 'ORDSYS',\n                          'OUTLN', 'OWBSYS' )\nUNION ALL\nSELECT 7 record_type,\n       'LOB_PARTITION' object_type,\n       tablespace_name,\n       table_owner owner,\n       table_name name,\n       SUBSTR(column_name, 1, 30) column_name,\n       partition_name partition,\n       NULL subpartition\n  FROM dba_lob_partitions\n WHERE logging = 'NO'\n AND TABLE_OWNER NOT IN ( 'SI_INFORMTN_SCHEMA', 'SQLTXADMIN', 'SQLTXPLAIN',\n                          'SYS',\n                          'SYSMAN', 'SYSTEM', 'TRCANLZR', 'WMSYS',\n                          'XDB', 'XS$NULL', 'PERFSTAT', 'STDBYPERF',\n                          'ANONYMOUS', 'APEX_030200', 'APEX_040000', 'APEX_SSO',\n                          'APPQOSSYS', 'CTXSYS', 'DBSNMP', 'DIP',\n                          'EXFSYS', 'FLOWS_FILES', 'MDSYS', 'OLAPSYS',\n                          'ORACLE_OCM', 'ORDDATA', 'ORDPLUGINS', 'ORDSYS',\n                          'OUTLN', 'OWBSYS' )\nUNION ALL\nSELECT 8 record_type,\n       'TAB_SUBPARTITION' object_type,\n       tablespace_name,\n       table_owner owner,\n       table_name name,\n       NULL column_name,\n       partition_name partition,\n       subpartition_name subpartition\n  FROM dba_tab_subpartitions\n WHERE logging = 'NO'\n AND TABLE_OWNER NOT IN ( 'SI_INFORMTN_SCHEMA', 'SQLTXADMIN', 'SQLTXPLAIN',\n                          'SYS',\n                          'SYSMAN', 'SYSTEM', 'TRCANLZR', 'WMSYS',\n                          'XDB', 'XS$NULL', 'PERFSTAT', 'STDBYPERF',\n                          'ANONYMOUS', 'APEX_030200', 'APEX_040000', 'APEX_SSO',\n                          'APPQOSSYS', 'CTXSYS', 'DBSNMP', 'DIP',\n                          'EXFSYS', 'FLOWS_FILES', 'MDSYS', 'OLAPSYS',\n                          'ORACLE_OCM', 'ORDDATA', 'ORDPLUGINS', 'ORDSYS',\n                          'OUTLN', 'OWBSYS' )\nUNION ALL\nSELECT 9 record_type,\n       'IND_SUBPARTITION' object_type,\n       tablespace_name,\n       index_owner owner,\n       index_name name,\n       NULL column_name,\n       partition_name partition,\n       subpartition_name subpartition\n  FROM dba_ind_subpartitions\n WHERE logging = 'NO'\n AND INDEX_OWNER NOT IN ( 'SI_INFORMTN_SCHEMA', 'SQLTXADMIN', 'SQLTXPLAIN',\n                          'SYS',\n                          'SYSMAN', 'SYSTEM', 'TRCANLZR', 'WMSYS',\n                          'XDB', 'XS$NULL', 'PERFSTAT', 'STDBYPERF',\n                          'ANONYMOUS', 'APEX_030200', 'APEX_040000', 'APEX_SSO',\n                          'APPQOSSYS', 'CTXSYS', 'DBSNMP', 'DIP',\n                          'EXFSYS', 'FLOWS_FILES', 'MDSYS', 'OLAPSYS',\n                          'ORACLE_OCM', 'ORDDATA', 'ORDPLUGINS', 'ORDSYS',\n                          'OUTLN', 'OWBSYS' )\nUNION ALL\nSELECT 10 record_type,\n       'LOB_SUBPARTITION' object_type,\n       tablespace_name,\n       table_owner owner,\n       table_name name,\n       SUBSTR(column_name, 1, 30) column_name,\n       lob_partition_name partition,\n       subpartition_name subpartition\n  FROM dba_lob_subpartitions\n WHERE logging = 'NO'\n AND TABLE_OWNER NOT IN ( 'SI_INFORMTN_SCHEMA', 'SQLTXADMIN', 'SQLTXPLAIN',\n                          'SYS',\n                          'SYSMAN', 'SYSTEM', 'TRCANLZR', 'WMSYS',\n                          'XDB', 'XS$NULL', 'PERFSTAT', 'STDBYPERF',\n                          'ANONYMOUS', 'APEX_030200', 'APEX_040000', 'APEX_SSO',\n                          'APPQOSSYS', 'CTXSYS', 'DBSNMP', 'DIP',\n                          'EXFSYS', 'FLOWS_FILES', 'MDSYS', 'OLAPSYS',\n                          'ORACLE_OCM', 'ORDDATA', 'ORDPLUGINS', 'ORDSYS',\n                          'OUTLN', 'OWBSYS' )\n)\nSELECT object_type,\n       tablespace_name,\n       owner,\n       name,\n       column_name,\n       partition,\n       subpartition\n  FROM objects\n ORDER BY\n       record_type,\n       tablespace_name,\n       owner,\n       name,\n       column_name,\n       partition,\n       subpartition", 'Nologging', {}, 'Nologging')
        self.priority = ''
        self.score = 20
        self.total_score = 20
        self.set_id_and_db_name(id, name)
        self.pre_check_sql = 'select force_logging from v$database'
        self.pre_check_pass_condition = 'YES'

    def pre_check_compare(self, database):
        try:
            flagt, resultt = run_sql(database, self.pre_check_sql)
            if flagt:
                if resultt[0]['FORCE_LOGGING'] == self.pre_check_pass_condition:
                    self.result = 'FORCE LOGGING'
                    return False
        except Exception as e:
            logger.exception('health check queries, error: %s', e)
            print(self.check_sql)
            return False

        return True

    def set_result_raw(self, resultSet):
        self.result_raw = [':' + x[0] + ' (' + (x[2] + '.' + x[3] if x[2] is not None else x[1]) + '),' for x in resultSet]

    def is_failed(self):
        return self.result_raw.__len__() > 0

    def set_result(self):
        self.result = 'Nologging,REDO' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          'Nologging,,:\n        \n' + ('\n        \n').join(self.result_raw)]}
        self.exe_advise = {}


class Check_SCN_HeadRoom(Oracle_Secure_Rule):

    def __init__(self, id, name):
        super(Check_SCN_HeadRoom, self).__init__("SELECT TO_CHAR(SYSDATE,'YYYY/MM/DD HH24:MI:SS') DATE_TIME,\n ((((\n ((TO_NUMBER(TO_CHAR(SYSDATE,'YYYY'))-1988)*12*31*24*60*60) +\n ((TO_NUMBER(TO_CHAR(SYSDATE,'MM'))-1)*31*24*60*60) +\n (((TO_NUMBER(TO_CHAR(SYSDATE,'DD'))-1))*24*60*60) +\n (TO_NUMBER(TO_CHAR(SYSDATE,'HH24'))*60*60) +\n (TO_NUMBER(TO_CHAR(SYSDATE,'MI'))*60) +\n (TO_NUMBER(TO_CHAR(SYSDATE,'SS')))\n ) * (16*1024)) - (SELECT current_scn FROM V$DATABASE))\n / (16*1024*60*60*24)\n ) INDICATOR\nFROM V$INSTANCE", 'SCNSCN', {}, 'SCN')
        self.priority = ''
        self.score = 20
        self.total_score = 20
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        self.result_raw = round(resultSet[0][1], 1)

    def is_failed(self):
        return self.result_raw < 61

    def set_result(self):
        self.result = 'SCN:' + str(self.result_raw) + ' ,!' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':['SCN,)']}
        self.exe_advise = {}


class Check_ObjectID_Increase(Oracle_Secure_Rule):

    def __init__(self, id, name):
        super(Check_ObjectID_Increase, self).__init__("SELECT Max(s),\n       Max(d1)\n         keep(dense_rank first ORDER BY s DESC)\nFROM   (SELECT d1,\n               m_id - Lag(m_id, 1, 0)\n                        over( ORDER BY d1) s ,\n               ROW_NUMBER() over( ORDER BY d1) rn\n        FROM   (SELECT To_char(created, 'yyyy-mm-dd') d1,\n                       Max(object_id)                 m_id\n                FROM   dba_objects\n                WHERE  created > SYSDATE - 14\n                GROUP  BY To_char(created, 'yyyy-mm-dd'))\n        ORDER  BY 1 DESC) t\nWHERE  rn<>1", 'OBJECT_ID', {}, 'OBJECT_ID')
        self.priority = ''
        self.score = 20
        self.total_score = 20
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        self.result_raw = resultSet

    def is_failed(self):
        return int(round(self.result_raw[0][0], 1)) > 100000

    def set_result(self):
        self.result = ' ' + self.result_raw[0][1] + ' OBJECT_ID:' + str(round(self.result_raw[0][0], 1)) + 'OBJECT_ID,OBJECT_ID,' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[' TruncateDrop/Create ( MOSID 76746.1)']}
        self.exe_advise = {}


class Check_Backup(Oracle_Backup_Rule):

    def __init__(self, id, name):
        super(Check_Backup, self).__init__("select  count(*) from v$backup_set where BACKUP_TYPE in ('D','I') and COMPLETION_TIME > sysdate -1", '', {'title':' :',  'content':[{}]}, '')
        self.priority = ''
        self.score = 20
        self.total_score = 20
        self.set_id_and_db_name(id, name)

    def is_failed(self):
        return self.result_raw == 0

    def set_result(self):
        self.result = '' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          ',,,']}
        self.exe_advise = {}


class Check_Block_Change_Tracking(Oracle_Backup_Rule):

    def __init__(self, id, name):
        super(Check_Block_Change_Tracking, self).__init__('select status FROM v$block_change_tracking', '', {}, '')
        self.priority = ''
        self.score = 5
        self.total_score = 5
        self.set_id_and_db_name(id, name)

    def is_failed(self):
        return self.result_raw == 'DISABLED'

    def set_result(self):
        self.result = ',,' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          '']}
        self.exe_advise = "alter database enable block change tracking using file '/xxxx/blk_ch_trc.trc'"


class Check_Tablespace_Usage(Oracle_Management_Rule):

    def __init__(self, id, name):
        super(Check_Tablespace_Usage, self).__init__("select * from (select  a.tablespace_name, round(b.used_size/a.total_size,2) * 100 used_pct from (select a.tablespace_name,sum( decode(b.autoextensible,'YES',decode(sign(maxbytes  - b.bytes),1,trunc(b.maxbytes / 1024 / 1024),trunc(b.bytes / 1024 / 1024)),'NO',trunc(b.bytes / 1024 / 1024))) as total_size ,count(*) cnt ,max(b.autoextensible) aet ,max(a.status) status, max(a.CONTENTS) CONTENTS,max(a.EXTENT_MANAGEMENT) EXTENT_MANAGEMENT,max(a.ALLOCATION_TYPE) ALLOCATION_TYPE from dba_tablespaces a,dba_data_files b where a.tablespace_name = b.tablespace_name  and a.status = 'ONLINE' and b.status in ('AVAILABLE','ONLINE','SYSTEM') and b.bytes is not null and a.CONTENTS = 'PERMANENT' group by a.tablespace_name) a, (select tablespace_name, trunc(sum(bytes) / 1024 / 1024) as used_size from dba_segments group by tablespace_name) b where a.tablespace_name = b.tablespace_name(+)) where used_pct > 90", '90% ', {}, '')
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        self.result_raw = [':' + x[0] + ' :' + str(x[1]) + ' ,' for x in resultSet]

    def is_failed(self):
        return self.result_raw.__len__() > 0

    def set_result(self):
        self.result = '90%,,SQL,' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          ':\n        \n' + ('\n        \n').join(self.result_raw)]}
        self.exe_advise = {}


class Check_TABLE_DOP(Oracle_Management_Rule):

    def __init__(self, id, name):
        super(Check_TABLE_DOP, self).__init__("SELECT t.owner, t.table_name, degree\n  FROM dba_tables t\nwhere (trim(t.degree) >'1' or trim(t.degree)='DEFAULT') and owner NOT IN ('ANONYMOUS','APEX_030200','APEX_040000','APEX_SSO','APPQOSSYS','CTXSYS','DBSNMP','DIP','EXFSYS','FLOWS_FILES','MDSYS','OLAPSYS','ORACLE_OCM','ORDDATA','ORDPLUGINS','ORDSYS','OUTLN','OWBSYS','SI_INFORMTN_SCHEMA','SQLTXADMIN','SQLTXPLAIN','SYS','SYSMAN','SYSTEM','TRCANLZR','WMSYS','XDB','XS$NULL','PERFSTAT','STDBYPERF')", '1', {}, 'DOP')
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        self.result_raw = [':' + x[0] + '.' + x[1] + ':' + str(x[2]) for x in resultSet]

    def is_failed(self):
        return self.result_raw.__len__() > 0

    def set_result(self):
        self.result = '' + str(self.result_raw.__len__()) + '1,1,' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          '(),,1:\n        \n' + ('\n        \n').join(self.result_raw)]}
        self.exe_advise = {}


class Check_INDEX_DOP(Oracle_Management_Rule):

    def __init__(self, id, name):
        super(Check_INDEX_DOP, self).__init__("SELECT t.owner, t.table_name, index_name, degree, status\n  FROM dba_indexes t\nwhere (trim(t.degree) >'1' or trim(t.degree)='DEFAULT') and owner NOT IN ('ANONYMOUS','APEX_030200','APEX_040000','APEX_SSO','APPQOSSYS','CTXSYS','DBSNMP','DIP','EXFSYS','FLOWS_FILES','MDSYS','OLAPSYS','ORACLE_OCM','ORDDATA','ORDPLUGINS','ORDSYS','OUTLN','OWBSYS','SI_INFORMTN_SCHEMA','SQLTXADMIN','SQLTXPLAIN','SYS','SYSMAN','SYSTEM','TRCANLZR','WMSYS','XDB','XS$NULL','PERFSTAT','STDBYPERF')\n", '1', {}, 'DOP')
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        self.result_raw = [':' + x[0] + '.' + x[1] + '' + x[2] + ':' + str(x[3]) for x in resultSet]

    def is_failed(self):
        return self.result_raw.__len__() > 0

    def set_result(self):
        self.result = '' + str(self.result_raw.__len__()) + '1,1,' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          '(),,1:\n        \n' + ('\n        \n').join(self.result_raw)]}
        self.exe_advise = {}


class Check_ALERT_LOG(Oracle_Management_Rule):

    def __init__(self, id, name):
        super(Check_ALERT_LOG, self).__init__("select message_text ,to_char(ORIGINATING_TIMESTAMP,'yyyy-mm-dd HH24:mi:ss'),INST_ID from sys.v_alert_log where  ORIGINATING_TIMESTAMP > (sysdate -30) and (message_text like '%ORA-%' ) and trim (component_id) = 'rdbms'\n", 'ORA', {}, 'Alert')
        self.priority = ''
        self.score = 20
        self.total_score = 20
        self.supported_db_versions = ['11', '12']
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        self.result_raw = ['' + str(x[2]) + 'alert(' + x[1] + '):' + x[0] for x in resultSet]

    def is_failed(self):
        return self.result_raw.__len__() > 0

    def set_result(self):
        self.result = '' + str(self.result_raw.__len__()) + 'ORA, ' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          '\n        \n' + ('\n        \n').join(self.result_raw)]}
        self.exe_advise = {}


class Check_Idle_Session(Oracle_Management_Rule):

    def __init__(self, id, name):
        super(Check_Idle_Session, self).__init__("\n SELECT A.INST_ID,\n       A.STATUS,\n       A.SID,\n       A.SERIAL#,\n       A.USERNAME,\n       A.MACHINE,\n       A.PROGRAM ,\n       to_char(A.LOGON_TIME,'yyyy-mm-dd hh24:mi:ss'),\n       ROUND(A.LAST_CALL_ET / 60 / 60, 2),\n       (SELECT NB.SPID\n          FROM GV$PROCESS NB\n         WHERE NB.ADDR = A.PADDR\n           AND NB.INST_ID = A.INST_ID) SPID,\n       (SELECT TRUNC(NB.PGA_USED_MEM / 1024 / 1024)\n          FROM GV$PROCESS NB\n         WHERE NB.ADDR = A.PADDR\n           AND NB.INST_ID = A.INST_ID) PGA_USED_MEM,\n       A.OSUSER,\n       ' ALTER SYSTEM  DISCONNECT SESSION ''' || A.SID || ',' || A.SERIAL# ||\n       ''' IMMEDIATE' KILL_SESSION\n  FROM GV$SESSION A\n WHERE A.STATUS IN ('INACTIVE')\n   AND A.USERNAME IS NOT NULL\n   AND A.USERNAME NOT IN ('SYS')\n   AND A.LAST_CALL_ET >= 60 * 60 * 24 * 7\n ORDER BY A.INST_ID, ROUND(A.LAST_CALL_ET / 60 / 60, 2) DESC\n ", '', {}, '')
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        self.result_raw = resultSet

    def is_failed(self):
        return self.result_raw.__len__() > 0

    def set_result(self):
        self.result = '(' + str(self.result_raw.__len__()) + '),,' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          ':\n        \n' + ('\n        \n').join([':(' + str(x[2]) + ',' + str(x[3]) + ') (' + str(x[4]) + ') :(' + str(x[5]) + '):(' + str(x[6]) + '):(' + str(x[7]) + ' :(' + str(x[8]) + ') h' for x in self.result_raw]) + '\n        \n :' + '\n        \n' + ('\n        \n').join([':' + str(x[0]) + ':' + str(x[-1]) + ';' for x in self.result_raw])]}
        self.exe_advise = {}


class Check_System_Tablespace_Usage(Oracle_Management_Rule):

    def __init__(self, id, name):
        super(Check_System_Tablespace_Usage, self).__init__("\n select username,default_tablespace,temporary_tablespace,account_status\nFROM\n    dba_users d\nWHERE\n    (default_tablespace = 'SYSTEM' or temporary_tablespace = 'SYSTEM') and username not in ('SYS','SYSTEM','MGMT_VIEW','OUTLN')\nORDER BY\n    username\n ", '/system', {}, '/')
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        self.result_raw = ['(' + x[0] + ') :' + x[1] + ') :' + x[2] for x in resultSet]

    def is_failed(self):
        return self.result_raw.__len__() > 0

    def set_result(self):
        self.result = '(' + str(self.result_raw.__len__()) + ')schema ,system,,' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          ':\n         \n' + ('\n         \n').join(self.result_raw)]}
        self.exe_advise = {}


class Check_Unproper_Located_Objects(Oracle_Management_Rule):

    def __init__(self, id, name):
        super(Check_Unproper_Located_Objects, self).__init__("\nSELECT DISTINCT ( owner ),\n                table_name\nFROM   dba_tables\nWHERE  tablespace_name = 'SYSTEM'\n       AND owner NOT IN ( 'SI_INFORMTN_SCHEMA', 'SQLTXADMIN', 'SQLTXPLAIN',\n                          'SYS',\n                          'SYSMAN', 'SYSTEM', 'TRCANLZR', 'WMSYS',\n                          'XDB', 'XS$NULL', 'PERFSTAT', 'STDBYPERF',\n                          'ANONYMOUS', 'APEX_030200', 'APEX_040000', 'APEX_SSO',\n                          'APPQOSSYS', 'CTXSYS', 'DBSNMP', 'DIP',\n                          'EXFSYS', 'FLOWS_FILES', 'MDSYS', 'OLAPSYS',\n                          'ORACLE_OCM', 'ORDDATA', 'ORDPLUGINS', 'ORDSYS',\n                          'OUTLN', 'OWBSYS' )\nUNION\nSELECT DISTINCT ( owner ),\n                index_name\nFROM   dba_indexes\nWHERE  tablespace_name = 'SYSTEM'\n       AND owner NOT IN ( 'SI_INFORMTN_SCHEMA', 'SQLTXADMIN', 'SQLTXPLAIN',\n                          'SYS',\n                          'SYSMAN', 'SYSTEM', 'TRCANLZR', 'WMSYS',\n                          'XDB', 'XS$NULL', 'PERFSTAT', 'STDBYPERF',\n                          'ANONYMOUS', 'APEX_030200', 'APEX_040000', 'APEX_SSO',\n                          'APPQOSSYS', 'CTXSYS', 'DBSNMP', 'DIP',\n                          'EXFSYS', 'FLOWS_FILES', 'MDSYS', 'OLAPSYS',\n                          'ORACLE_OCM', 'ORDDATA', 'ORDPLUGINS', 'ORDSYS',\n                          'OUTLN', 'OWBSYS' ) ", 'system', {}, '')
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        self.result_raw = ['(' + x[0] + '.' + x[1] + ')' for x in resultSet]

    def is_failed(self):
        return self.result_raw.__len__() > 0

    def set_result(self):
        self.result = 'system ' + str(len(self.result_raw)) + ',,' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          ':\n        \n' + ('\n        \n').join(self.result_raw)]}
        self.exe_advise = {}


class Check_DiskGroup_Usage(Oracle_Management_Rule):

    def __init__(self, id, name):
        super(Check_DiskGroup_Usage, self).__init__('select * from ( select NAME,\n            round((TOTAL_MB-FREE_MB)/TOTAL_MB*100) used_pct\n        FROM\n            V$ASM_DISKGROUP) where used_pct > 90', '90% ', {}, '')
        self.pre_check_sql = 'select count(*) C from v$asm_diskgroup'
        self.pre_check_pass_condition = 0
        self.priority = ''
        self.score = 20
        self.total_score = 20
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        self.result_raw = [':' + x[0] + ' :' + str(x[1]) + ' ,' for x in resultSet]

    def is_failed(self):
        return self.result_raw.__len__() > 0

    def pre_check_compare(self, database):
        try:
            flagt, resultt = run_sql(database, self.pre_check_sql)
            if flagt:
                if resultt[0]['C'] == self.pre_check_pass_condition:
                    self.result = 'asm,'
                    return False
        except Exception as e:
            logger.exception('health check queries, error: %s', e)
            print(self.check_sql)
            return False

        return True

    def set_result(self):
        self.result = '90%,,SQL,' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          ':\n        \n' + ('\n        \n').join(self.result_raw)]}
        self.exe_advise = {}


class Check_ASM_Parameter(Oracle_Management_Rule):

    def __init__(self, id, name):
        super(Check_ASM_Parameter, self).__init__("SELECT /*+ NO_MERGE */    name,value,group_number  FROM v$asm_attribute where name='disk_repair_time' and value='3.6h'", '', {}, '')
        self.pre_check_sql = 'select count(*) C from v$asm_diskgroup'
        self.priority = ''
        self.score = 5
        self.total_score = 5
        self.pre_check_pass_condition = 0
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        self.result_raw = resultSet

    def is_failed(self):
        return self.result_raw.__len__() > 0

    def pre_check_compare(self, database):
        try:
            flagt, resultt = run_sql(database, self.pre_check_sql)
            if flagt:
                if resultt[0]['C'] == self.pre_check_pass_condition:
                    self.result = 'asm,'
                    return False
        except Exception as e:
            logger.exception('health check queries, error: %s', e)
            print(self.check_sql)
            return False

        return True

    def set_result(self):
        self.result = 'disk_repair_time,,rebalance,IO' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          ',36:\n        \n' + ('\n        \n').join(['(' + x[0] + '),' for x in self.result_raw])]}
        self.exe_advise = ['ALTER DISKGROUP ' + str(x[2]) + "SET ATTRIBUTE 'DISK_REPAIR_TIME'='36H';" for x in self.result_raw]


class Check_Failed_Parse(Oracle_Management_Rule):

    def __init__(self, id, name):
        super(Check_Failed_Parse, self).__init__('WITH\nper_instance AS (\nSELECT /*+ MATERIALIZE NO_MERGE DYNAMIC_SAMPLING(4) */\n       snap_id,\n       instance_number,\n       TRUNC(begin_time, \'HH\') begin_time_hh,\n       maxval,\n       ROW_NUMBER () OVER (PARTITION BY dbid, instance_number, group_id, metric_id, TRUNC(begin_time, \'HH\') ORDER BY maxval DESC NULLS LAST, begin_time DESC) rn\n  FROM dba_hist_sysmetric_summary\n WHERE\n   group_id = 2 /* 1 minute intervals */\n   AND metric_name = \'Parse Failure Count Per Sec\'\n)\nSELECT /*+ NO_MERGE */\n       MIN(snap_id) snap_id,\n       TO_CHAR(begin_time_hh, \'YYYY-MM-DD HH24:MI\') begin_time,\n       TO_CHAR(begin_time_hh + (1/24), \'YYYY-MM-DD HH24:MI\') end_time,\n       ROUND(SUM(maxval), 1) "Max Value"\n  FROM per_instance\n WHERE rn = 1\n having ROUND(SUM(maxval), 1)  > 2\n GROUP BY\n       begin_time_hh\n ORDER BY\n       begin_time_hh', '', {}, '')
        self.priority = ''
        self.score = 20
        self.total_score = 20
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        self.result_raw = [':' + x[1] + ' :' + x[2] + ':' + str(x[3]) for x in resultSet]

    def is_failed(self):
        return self.result_raw.__len__() > 0

    def set_result(self):
        self.result = '' + str(self.result_raw.__len__()) + ' ,SQL,' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          '(:http://59.110.157.215/?p=11 ):\n        \n' + ('\n        \n').join(self.result_raw) + '\n ']}
        self.exe_advise = {}


class Check_Long_Transaction(Oracle_Management_Rule):

    def __init__(self, id, name):
        super(Check_Long_Transaction, self).__init__('\nselect s.username,s.sid,s.serial#,s.program,s.sql_id,s.seconds_in_wait,t.used_ublk\n        from v$transaction t,v$session s\n        where t.ses_addr=s.saddr\n        and s.seconds_in_wait > 3600\n        and t.used_ublk > 1000', '1', {}, '')
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        self.result_raw = [':' + str(x[1]) + ',' + str(x[2]) + ':' + str(x[5]) + '(s),' + str(x[3]) for x in resultSet]

    def is_failed(self):
        return self.result_raw.__len__() > 0

    def set_result(self):
        self.result = '' + str(self.result_raw.__len__()) + ',' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          '(1),SQL:\n        \n' + ('\n        \n').join(self.result_raw) + '\n ']}
        self.exe_advise = {}


class Check_Slow_SQL(Oracle_Performance_Rule):

    def __init__(self, id, name):
        super(Check_Slow_SQL, self).__init__("\nselect sql_id, round(buff_exec)*exec_times gets_total, round(buff_exec) gets_exec,\n               round(disk_exec) disk_exec, exec_times, start_time, end_time\n          from (select sql_id, avg(buffer_gets_exec) buff_exec, avg(disk_reads_exec) disk_exec,\n                       sum(executions_total) exec_times,\n\t\t\t\t\t   min(begin_interval_time) start_time,\n\t\t\t\t\t   max(begin_interval_time) end_time\n                  from (select begin_interval_time, sql_id, buffer_gets_total,\n\t\t\t\t               disk_reads_total, executions_total,\n                               round(buffer_gets_total / nvl(executions_total,1)) buffer_gets_exec,\n                               round(disk_reads_total / nvl(executions_total,1))  disk_reads_exec\n                  from dba_hist_sqlstat s, dba_hist_snapshot n\n                 where s.snap_id = n.snap_id and executions_total > 0\n\t\t\t\t   and parsing_schema_name not in ('ANONYMOUS','APEX_030200','APEX_040000','APEX_SSO','APPQOSSYS','CTXSYS','DBSNMP','DIP','EXFSYS','FLOWS_FILES','MDSYS','OLAPSYS','ORACLE_OCM','ORDDATA','ORDPLUGINS','ORDSYS','OUTLN','OWBSYS','SI_INFORMTN_SCHEMA','SQLTXADMIN','SQLTXPLAIN','SYS','SYSMAN','SYSTEM','TRCANLZR','WMSYS','XDB','XS$NULL','PERFSTAT','STDBYPERF','YUNQU')\n                   and (round(buffer_gets_total / nvl(executions_total,1) ) > 99999\n\t\t\t\t     or round(disk_reads_total / nvl(executions_total,1)) > 9999)\n\t\t\t\t   and executions_total > 9)\n        group by sql_id) ", ',SQL', {}, 'SQL')
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        self.result_raw = ['SQL_ID:(' + str(x[0]) + '): :' + str(x[2]) + ' :' + str(x[3]) for x in resultSet]

    def is_failed(self):
        return self.result_raw.__len__() > 0

    def set_result(self):
        self.result = '' + str(self.result_raw.__len__()) + 'SQL,' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          'SQL,:\n        \n' + ('\n        \n').join(self.result_raw) + '\n ']}
        self.exe_advise = {}


class Check_ASM_Disk_State(Oracle_Management_Rule):

    def __init__(self, id, name):
        super(Check_ASM_Disk_State, self).__init__("select name from V$ASM_DISK where MODE_STATUS='OFFLINE'", 'ASM', {}, '')
        self.pre_check_sql = 'select count(*) C from v$asm_diskgroup'
        self.pre_check_pass_condition = 0
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        self.result_raw = [x[0] + ',' for x in resultSet]

    def is_failed(self):
        return self.result_raw.__len__() > 0

    def pre_check_compare(self, database):
        try:
            flagt, resultt = run_sql(database, self.pre_check_sql)
            if flagt:
                if resultt[0]['C'] == self.pre_check_pass_condition:
                    self.result = 'asm,'
                    return False
        except Exception as e:
            logger.exception('health check queries, error: %s', e)
            print(self.check_sql)
            return False

        return True

    def set_result(self):
        self.result = 'offline,,' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[
          ',onlineonline:\n        ' + ('\n        \n').join(self.result_raw)]}
        self.exe_advise = {}


class Check_FRA_Usage(Oracle_Backup_Rule):

    def __init__(self, id, name):
        super(Check_FRA_Usage, self).__init__('select (space_used - SPACE_RECLAIMABLE)/space_limit*100 from v$recovery_file_dest', '80%', {}, '')
        self.pre_check_sql = "select name,value from v$parameter where regexp_like(name,'db_recovery_file_dest')"
        self.pre_check_pass_condition = 0
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        self.result_raw = round(resultSet[0][0], 2)

    def is_failed(self):
        return int(self.result_raw) > 80

    def pre_check_compare(self, database):
        try:
            flagt, resultt = run_sql(database, self.pre_check_sql)
            if flagt:
                if resultt[0]['NAME'] != '':
                    if resultt[0]['NAME'] != '':
                        self.advise = {'title': ' ,'}
                        self.result = ','
                        return False
        except Exception as e:
            logger.exception('health check queries, error: %s', e)
            print(self.check_sql)
            return False

        return True

    def set_result(self):
        self.result = '' + str(self.result_raw) + ',,' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':[',']}
        self.exe_advise = {}


class Check_CFile_Backup(Oracle_Backup_Rule):

    def __init__(self, id, name):
        super(Check_CFile_Backup, self).__init__("select VALUE from v$rman_configuration where name ='CONTROLFILE AUTOBACKUP'", '', {}, '')
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        if resultSet:
            self.result_raw = resultSet[0][0]
        else:
            self.result_raw = ''

    def is_failed(self):
        return self.result_raw != 'ON'

    def set_result(self):
        self.result = ',,' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':['']}
        self.exe_advise = {}


class Check_Backup_Opt(Oracle_Backup_Rule):

    def __init__(self, id, name):
        super(Check_Backup_Opt, self).__init__("select VALUE from v$rman_configuration where name ='BACKUP OPTIMIZATION'", '', {}, '')
        self.priority = ''
        self.score = 5
        self.total_score = 5
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        if resultSet:
            self.result_raw = resultSet[0][0]
        else:
            self.result_raw = ''

    def is_failed(self):
        return self.result_raw != 'ON'

    def set_result(self):
        self.result = ',,' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':['']}
        self.exe_advise = {}


class Check_Backup_Parallel(Oracle_Backup_Rule):

    def __init__(self, id, name):
        super(Check_Backup_Parallel, self).__init__("select VALUE from v$rman_configuration where name ='DEVICE TYPE'", '', {}, '')
        self.priority = ''
        self.score = 5
        self.total_score = 5
        self.set_id_and_db_name(id, name)

    def set_result_raw(self, resultSet):
        if resultSet:
            self.result_raw = resultSet[0][0]
        else:
            self.result_raw = ''

    def is_failed(self):
        return ' 1 ' in self.result_raw

    def set_result(self):
        self.result = ',,' if self.is_failed() else ' '

    def set_advise(self):
        self.advise = {'title':':', 
         'content':['']}
        self.exe_advise = {}
# okay decompiling ./restful/hawkeye/api/v1/heathcheck/rules/oracle_rule.pyc
