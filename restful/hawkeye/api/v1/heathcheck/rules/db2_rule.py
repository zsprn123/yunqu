# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/heathcheck/rules/db2_rule.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 21412 bytes
import paramiko
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from datetime import datetime
import logging
from api.v1.monitor.services.runsqlService import run_sql, run_cmd
from common.aes import aes_decode
logger = logging.getLogger('api')
from .base_rule import Rule

class DB2_Rule(Rule):

    def __init__(self, check_sql, check_cmd, category, description, advise, title):
        super(DB2_Rule, self).__init__()
        self.check_sql = check_sql
        self.check_cmd = check_cmd
        self.description = description
        self.category = category
        self.advise = advise
        self.database_type = 'DB2'
        self.supported_db_versions = ['9.5.0.0', '9.7.0.0']
        self.title = title
        self.db_id = ''
        self.score = 10
        self.total_score = 10

    def _check(self, database):
        if self.check_sql:
            try:
                flag, result = run_sql(database, self.check_sql)
                if flag:
                    if result:
                        res = [list(r.values()) for r in result]
                        self.set_result(res)
            except Exception as e:
                logger.exception('health check db2 queries, error: %s', e)

        else:
            try:
                s = paramiko.SSHClient()
                s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                s.connect(database.hostname, database.port, database.username, aes_decode(database.password))
            except Exception as e:
                logger.error(str(e))
                logger.warning('is not support run cmd !')

            try:
                res = run_cmd(database, self.check_cmd)
                self.set_result_cmd(res)
            except Exception as e:
                logger.exception('health check db2 commands, error: %s', e)

            if self.is_failed():
                self.resize_result_raw()
                self.set_score()

    def set_result(self, resultSet):
        self.result = resultSet[0][0]

    def is_failed(self):
        pass

    def set_score(self):
        self.score = 0

    def is_checked(self):
        return self.result != ''

    def set_result_cmd(self, res):
        pass

    def is_right_version(self, db_version):
        return True


class DB2_Config_Rule(DB2_Rule):

    def __init__(self, check_sql, check_cmd, description, advise, title):
        super(DB2_Config_Rule, self).__init__(check_sql, check_cmd, '', description, advise, title)


class DB2_Secure_Rule(DB2_Rule):

    def __init__(self, check_sql, check_cmd, description, advise, title):
        super(DB2_Secure_Rule, self).__init__(check_sql, check_cmd, '', description, advise, title)


class DB2_Backup_Rule(DB2_Rule):

    def __init__(self, check_sql, check_cmd, description, advise, title):
        super(DB2_Backup_Rule, self).__init__(check_sql, check_cmd, '', description, advise, title)


class DB2_Management_Rule(DB2_Rule):

    def __init__(self, check_sql, check_cmd, description, advise, title):
        super(DB2_Management_Rule, self).__init__(check_sql, check_cmd, '', description, advise, title)


class DB2_Performance_Rule(DB2_Rule):

    def __init__(self, check_sql, check_cmd, description, advise, title):
        super(DB2_Performance_Rule, self).__init__(check_sql, check_cmd, '', description, advise, title)


class DB2_Check_Backup(DB2_Backup_Rule):

    def __init__(self, id, db_name):
        super(DB2_Check_Backup, self).__init__('', 'db2 list history backup since %s for %s' % (
         datetime.now().strftime('%Y%m%d'), db_name), '', {}, '')
        self.set_id_and_db_name(id, db_name)
        self.priority = ''
        self.score = 20
        self.total_score = 20

    def set_result_cmd(self, res):
        for line in res:
            self.result_raw = self.result + line
            if 'Status' in line:
                if line.split(':')[1].strip() == 'A':
                    self.result = ','
                    return

        self.score = 0
        self.result = ','
        self.advise = {'title':' :',  'content':[
          ',,,: ' + 'db2 list history backup since %s for %s' % (
           datetime.now().strftime('%Y%m%d'), self.db_name)]}


class DB2_Check_Hadr(DB2_Secure_Rule):

    def __init__(self, id, db_name):
        super(DB2_Check_Hadr, self).__init__('', 'db2pd -db %s -hadr | grep HADR_STATE' % db_name, 'hadr', {}, 'HADR')
        self.set_id_and_db_name(id, db_name)
        self.priority = ''
        self.score = 20
        self.total_score = 20

    def set_result_cmd(self, res):
        for line in res:
            self.result_raw = line
            if 'isconn' in line.lower() or 'pend' in line.lower():
                self.score = 0
                self.result = 'HDR :%s, ,' % self.result_raw
                self.advise = {'title':' :',  'content':['HADR,,']}
                return

        self.result = 'HDR :%s, ' % self.result_raw if self.result_raw is not None else 'HADR'


class DB2_Check_Incr_Backup(DB2_Backup_Rule):

    def __init__(self, id, db_name):
        super(DB2_Check_Incr_Backup, self).__init__("select value from  sysibmadm.dbcfg where name='trackmod'", '', '', {}, '')
        self.set_id_and_db_name(id, db_name)
        self.priority = ''
        self.score = 5
        self.total_score = 5

    def set_result(self, res):
        self.result_raw = res
        self.result = ','

    def is_failed(self):
        if self.result_raw:
            return 'OFF' in self.result_raw[0][0]
        else:
            return False

    def set_score(self):
        self.score = 0
        self.result = ',,IO'
        self.advise = {'title':' :',  'content':[',,,,']}


class DB2_Check_Memory(DB2_Performance_Rule):

    def __init__(self, id, db_name):
        super(DB2_Check_Memory, self).__init__('SELECT DBPARTITIONNUM, MAX_PARTITION_MEM/1048576 AS MAX_MEM_MB, CURRENT_PARTITION_MEM/1048576 AS CURRENT_MEM_MB, PEAK_PARTITION_MEM/1048576 AS PEAK_MEM_MB FROM TABLE (SYSPROC.ADMIN_GET_DBP_MEM_USAGE()) AS T', '', '80%', {}, '')
        self.set_id_and_db_name(id, db_name)

    def set_result(self, res):
        self.result_raw = float(round(res[0][2] / res[0][1], 2))
        self.result = ':%s,' % str(self.result_raw)

    def is_failed(self):
        if self.result_raw:
            return self.result_raw > 0.8
        else:
            return False

    def set_score(self):
        self.score = 0
        self.result = ':%s,,' % str(self.result_raw)
        self.advise = {'title':' :',  'content':[',']}


class DB2_Check_Sheapthres(DB2_Config_Rule):

    def __init__(self, id, db_name):
        super(DB2_Check_Sheapthres, self).__init__('', 'db2 get dbm cfg', ':SHEAPTHRES ', {}, '')
        self.set_id_and_db_name(id, db_name)

    def set_result_cmd(self, res):
        for line in res:
            if 'SHEAPTHRES' in line:
                self.result_raw = int(line.split('=')[1].strip())

        self.result = ':SHEAPTHRES (%s) ' % self.result_raw

    def is_failed(self):
        if self.result_raw != '':
            return self.result_raw < 20000
        else:
            return False

    def set_score(self):
        self.score = 0
        self.result = ':SHEAPTHRES (%s) ' % self.result_raw
        self.advise = {'title':' :',  'content':[
          ':SHEAPTHRES OLTP  20000,OLAP  40000~60000,']}


class DB2_Check_Audit(DB2_Secure_Rule):

    def __init__(self, id, db_name):
        super(DB2_Check_Audit, self).__init__('', 'db2audit describe', '', {}, '')
        self.set_id_and_db_name(id, db_name)
        self.priority = ''
        self.score = 5
        self.total_score = 5

    def set_result_cmd(self, res):
        for line in res:
            if 'Audit active' in line:
                self.result_raw = line.split(':')[1].strip()

        self.result = ','

    def is_failed(self):
        return 'FALSE' in self.result_raw

    def set_score(self):
        self.score = 0
        self.result = ','
        self.advise = {'title':' :',  'content':[',']}


class DB2_Check_Monheapsz(DB2_Config_Rule):

    def __init__(self, id, db_name):
        super(DB2_Check_Monheapsz, self).__init__('', 'db2 get dbm cfg', ':MON_HEAP_SZ ', {}, '')
        self.set_id_and_db_name(id, db_name)

    def set_result_cmd(self, res):
        for line in res:
            if 'SHEAPTHRES' in line:
                self.result_raw = line.split('=')[1].strip()

        self.result = ':MON_HEAP_SZ %s ' % str(self.result_raw)

    def is_failed(self):
        return 'AUTOMATIC' in self.result_raw

    def set_score(self):
        self.score = 0
        self.result = ':MON_HEAP_SZ %s ' % str(self.result_raw)
        self.advise = {'title':' :',  'content':[':MON_HEAP_SZ ,v9  AUTOMATIC']}


class DB2_Check_Lock(DB2_Management_Rule):

    def __init__(self, id, db_name):
        super(DB2_Check_Lock, self).__init__('', 'db2 -v get snapshot for database on %s' % db_name, '', {}, '')
        self.set_id_and_db_name(id, db_name)

    def set_result_cmd(self, res):
        self.result_raw = []
        for line in res:
            if 'Lock escalations' in line:
                self.result_raw = line

        self.result = ''

    def is_failed(self):
        if self.result_raw:
            return '0' != self.result_raw.split('=')[1].strip()
        else:
            return True

    def set_score(self):
        self.score = 0
        self.result = ',,: %s' % str(self.result)
        self.advise = {'title':' :',  'content':[',sql,,']}


class DB2_Check_Bhit_Ratio(DB2_Performance_Rule):

    def __init__(self, id, db_name):
        super(DB2_Check_Bhit_Ratio, self).__init__("select substr(bp_name,1,30) as bp_name, data_hit_ratio_percent,index_hit_ratio_percent,total_hit_ratio_percent from sysibmadm.bp_hitratio where bp_name not like 'IBMSYSTEM%'", '', 'BUFFER CACHE90%', {}, '')
        self.set_id_and_db_name(id, db_name)

    def set_result(self, res):
        self.result_raw = res
        self.result = ':' + ('\n').join(['(%s):%s' % (rest[0].strip(), str(rest[3])) for rest in self.result])

    def is_failed(self):
        if not self.result_raw:
            return False
        else:
            for x in self.result_raw:
                if float(x[3] if x[3] else 100) < 90:
                    return True

            return False

    def set_score(self):
        self.score = 0
        self.result = ',IO'
        self.advise = {'title':' :',  'content':[
          ',:\n' + ('\n\n').join(['(%s):%s' % (rest[0].strip(), str(rest[3])) for rest in self.result_raw])]}


class DB2_Check_PKG_Ratio(DB2_Performance_Rule):

    def __init__(self, id, db_name):
        super(DB2_Check_PKG_Ratio, self).__init__('select  100*(1 - pkg_cache_inserts/pkg_cache_lookups) from sysibmadm.snapdb', '', '90%', {}, 'PACKAGE')
        self.set_id_and_db_name(id, db_name)

    def set_result(self, res):
        self.result_raw = res
        self.result = 'PACKAGE:%s,' % str(self.result_raw[0][0])

    def is_failed(self):
        for x in self.result_raw:
            if float(x[0]) < 90:
                return True

        return False

    def set_score(self):
        self.score = 0
        self.result = 'PACKAGE:%s,,' % str(self.result_raw[0][0])
        self.advise = {'title':' :',  'content':['package,package']}


class DB2_Check_Log_Percent(DB2_Management_Rule):

    def __init__(self, id, db_name):
        super(DB2_Check_Log_Percent, self).__init__('select int((float(total_log_used)/float(total_log_used+total_log_available))*100) from sysibmadm.snapdb', '', '90%', {}, '')
        self.set_id_and_db_name(id, db_name)

    def set_result(self, res):
        self.result_raw = res[0][0]
        self.result = ':%s,' % str(self.result_raw)

    def is_failed(self):
        if self.result_raw:
            return self.result_raw > 90
        else:
            return False

    def set_score(self):
        self.score = 0
        self.result = ':%s,,' % str(self.result_raw)
        self.advise = {'title':' :',  'content':[',']}


class DB2_Check_Tablespace_Usage(DB2_Management_Rule):

    def __init__(self, id, db_name):
        super(DB2_Check_Tablespace_Usage, self).__init__("select substr(tbsp_name,1,18),tbsp_utilization_percent from sysibmadm.tbsp_utilization where tbsp_type <> 'SMS'", '', 'SMS90%', {}, '')
        self.set_id_and_db_name(id, db_name)

    def set_result(self, res):
        self.result_raw = res
        self.result = ('\n\n').join([x[0] + ':' + str(x[1]) + ' ,' for x in res if float(x[1]) < 90])

    def is_failed(self):
        return not [x for x in self.result_raw if float(x[1]) < 90]

    def set_score(self):
        self.score = 0
        self.result = ',:\n' + ('\n\n').join([x[0] + ':' + str(x[1]) + ' ,' for x in self.result_raw if float(x[1]) > 90])
        self.advise = {'title':' :',  'content':[',']}


class DB2_Check_Table_ReORG(DB2_Management_Rule):

    def __init__(self, id, db_name):
        super(DB2_Check_Table_ReORG, self).__init__("call REORGCHK_TB_STATS('T','ALL')", '', 'reorg', {}, 'REORG')
        self.set_id_and_db_name(id, db_name)

    def set_result(self, res):
        self.result_raw = res
        if self.result_raw.__len__() > 100:
            self.result_raw = self.result_raw[0:100]
        self.result = 'reorg:' + ('\n\n').join([x[0].strip() + '.' + x[1] + ',' for x in res if '---' in x[12]])

    def is_failed(self):
        return [' REORG:' + str(x[12]) + ',' for x in self.result_raw if '*' in x[12]]

    def set_score(self):
        self.score = 0
        self.result = 'reorg,'
        self.advise = {'title':' :',  'content':[
          'reorg:\n' + ('\n\n').join([x[0].strip() + '.' + x[1] + ',' for x in self.result_raw if '*' in x[12]])]}


class DB2_Check_Index_ReORG(DB2_Management_Rule):

    def __init__(self, id, db_name):
        super(DB2_Check_Index_ReORG, self).__init__("call REORGCHK_IX_STATS('T','ALL')", '', 'reorg', {}, 'REORG')
        self.set_id_and_db_name(id, db_name)

    def set_result(self, res):
        self.result_raw = res
        if self.result_raw.__len__() > 100:
            self.result_raw = self.result_raw[0:100]
        self.result = 'reorg:' + ('\n\n').join([x[0].strip() + '.' + x[3] + ',' for x in res if '---' in x[21]])

    def is_failed(self):
        if self.result_raw:
            return not [' REORG:' + str(x[12]) + ',' for x in self.result_raw if '*' in x[21]]
        else:
            return False

    def set_score(self):
        self.score = 0
        self.result = 'reorg,'
        self.advise = {'title':' :',  'content':[
          'reorg:\n' + ('\n\n').join([x[0].strip() + '.' + x[3] + ',' for x in self.result_raw if '*' in x[21]])]}


class DB2_Check_Table_Stats(DB2_Performance_Rule):

    def __init__(self, id, db_name):
        super(DB2_Check_Table_Stats, self).__init__('select  TABSCHEMA,TABNAME,stats_time from syscat.tables where stats_time is null or stats_time < current date - 30 days', '', '', {}, '')
        self.set_id_and_db_name(id, db_name)

    def set_result(self, res):
        self.result_raw = res
        if self.result_raw.__len__() > 100:
            self.result_raw = self.result_raw[0:100]
        self.result = ''

    def is_failed(self):
        return not self.result_raw

    def set_score(self):
        self.score = 0
        self.result = ',,'
        self.advise = {'title':' :',  'content':[
          'reorg:\n' + ('\n\n').join([' :' + x[0] + '.' + x[1] + ' :' + x[2].strftime('%Y-%m-%d %H:%M:%S') + ',' for x in self.result_raw])]}


class DB2_Check_Audit_Buff(DB2_Secure_Rule):

    def __init__(self, id, db_name):
        super(DB2_Check_Audit_Buff, self).__init__("select value from  sysibmadm.dbmcfg where name='audit_buf_sz'", '', '', {}, '')
        self.set_id_and_db_name(id, db_name)
        self.priority = ''
        self.score = 5
        self.total_score = 5

    def set_result(self, res):
        self.result_raw = res
        self.result = ','

    def is_failed(self):
        return self.result_raw == '0'

    def set_score(self):
        self.score = 0
        self.result = ' audit_buf_sz ,,'
        self.advise = {'title':' :',  'content':[',']}
# okay decompiling ./restful/hawkeye/api/v1/heathcheck/rules/db2_rule.pyc
