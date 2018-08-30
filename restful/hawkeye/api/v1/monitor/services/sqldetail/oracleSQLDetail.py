# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/monitor/services/sqldetail/oracleSQLDetail.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 9265 bytes
from api.enum.sqldetail_enum import get_realtime_sql, get_hist_sql, gen_sql_mononitor_and_binds
from api.v1.monitor.services.runsqlService import run_sql, run_batch_sql
from common.util import execute_return_json
from monitor.models import Database
from collections import defaultdict
from api.v1.monitor.services.activityService import get_database_activity
from api.v1.monitor.services.sqltuneService import get_sql_audit, get_sql_tune
from api.v1.monitor.services.sqldetail.common import get_default_sql_detail_format
from common.storages import redis
import json
from api.v1.monitor.services.sqldetail.common import get_sql_text
SQLTEXT_RETENTION = 604800
MAX_SQLMON_FOR_SQL_AUDIT = 3

def oracle_sql_detail(pk, sql_id, sql_text=None, instance_id=None, time_span=None, begin_time=None, end_time=None, cache=True, activity=True, sql_audit=True, only_tune=False):
    database = Database.objects.get(pk=pk)
    if instance_id == 'null':
        instance_id = database.db_name
    inst_id = database.instance_id_list.split(',')[0] if not instance_id or instance_id == database.db_name or instance_id == '0' else instance_id
    if sql_audit:
        inst_id = database.instance_id_list
    key_audit = f'''{pk}:sql_detail:{sql_id}:audit'''
    audit_data = None
    audit_data_json = {}
    if cache:
        audit_data = redis.get(key_audit)
        if audit_data != None:
            audit_data_json = json.loads(audit_data)
    sql_detail = get_default_sql_detail_format(database.db_type)
    if sql_id != 'null':
        if time_span == 'realtime':
            sqldetail_sql = get_realtime_sql(sql_id, inst_id)
            if only_tune:
                sqldetail_sql.pop('binds')
            flag, sqldetail_data = run_batch_sql(database, sqldetail_sql)
            if not flag:
                return sqldetail_data
            stat_data = sqldetail_data.get('stats')
            plan_data = sqldetail_data.get('plans')
            sqlmon_data = sqldetail_data.get('sqlmon')
            bind_data = only_tunesqldetail_data.get('binds')[]
            for x in stat_data:
                key = ('{}-{}-{}').format(x.get('INST_ID'), x.get('CHILD_NUMBER'), x.get('PLAN_HASH_VALUE'))
                child_summary = {k:v for k, v in x.items() if k in ('CHILD_NUMBER',
                                                                    'PLAN_HASH_VALUE',
                                                                    'PARSING_SCHEMA_NAME',
                                                                    'LAST_LOAD_TIME',
                                                                    'MODULE', 'ACTION',
                                                                    'SERVICE')}
                pie_chart_data = {k:v for k, v in x.items() if k in ('ON CPU', 'Application',
                                                                     'Cluster', 'Concurrency',
                                                                     'User I/O')}
                execution_stats = {k:v for k, v in x.items() if k in ('EXECUTIONS',
                                                                      'ELAPSED_TIME',
                                                                      'CPU_TIME',
                                                                      'BUFFER_GETS',
                                                                      'DISK_READS',
                                                                      'DIRECT_WRITES',
                                                                      'ROWS_PROCESSED',
                                                                      'FETCHES')}
                metric_dict = {'EXECUTIONS':'', 
                 'ELAPSED_TIME':'()', 
                 'CPU_TIME':'CPU()', 
                 'BUFFER_GETS':'', 
                 'DISK_READS':'', 
                 'DIRECT_WRITES':'', 
                 'ROWS_PROCESSED':'', 
                 'FETCHES':''}
                total_executions = execution_stats.get('EXECUTIONS') if execution_stats.get('EXECUTIONS') != 0 else 1
                total_rows = execution_stats.get('ROWS_PROCESSED') if execution_stats.get('ROWS_PROCESSED') != 0 else 1
                execution_data = [{u'\u6307\u6807':metric_dict.get(k),  u'\u603b\u6570':v,  u'\u5e73\u5747\u6bcf\u6b21\u6267\u884c':round(v / total_executions),  u'\u5e73\u5747\u6bcf\u884c\u8bb0\u5f55':round(v / total_rows)} for k, v in execution_stats.items()]
                sql_detail['stats'][key] = {'child_summary':child_summary, 
                 'pie_chart_data':pie_chart_data, 
                 'execution_stats':{'header':[
                   '', '', '', ''], 
                  'data':execution_data}}

            plan_dic = defaultdict(list)
            for x in plan_data:
                key = ('{}-{}-{}').format(x.get('INST_ID'), x.get('CHILD_NUMBER'), x.get('PLAN_HASH_VALUE'))
                x.pop('INST_ID')
                plan_dic[key].append(x)

            sql_detail['plans']['data'] = plan_dic
            if sql_audit:
                if sqlmon_data:
                    sqlmon_data = sqlmon_data[:MAX_SQLMON_FOR_SQL_AUDIT]
                    binds_from_sqlmon = gen_sql_mononitor_and_binds(database, sqlmon_data)
                    bind_data = bind_data + binds_from_sqlmon
            sql_detail['sqlmon']['data'] = sqlmon_data
            sql_detail['binds']['data'] = bind_data
        else:
            sqldetail_sql = get_hist_sql(sql_id, inst_id, begin_time, end_time)
            query_sqlmon = f'''
                select
                ID,
                STATUS,
                SQL_ID,
                ELAPSED_TIME,
                DB_TIME,
                DB_CPU,
                SQL_EXEC_ID,
                SQL_EXEC_START,
                SQL_PLAN_HASH_VALUE,
                INST_ID,
                USERNAME
                from monitor_sqlmon
                where created_at BETWEEN to_timestamp({begin_time}) and to_timestamp({end_time})
                and sql_id = '{sql_id}' and database_id = '{pk}'
            '''
            flag, sqldetail_data = run_batch_sql(database, sqldetail_sql)
            if not flag:
                return sqldetail_data
            stat_data = sqldetail_data.get('stats')
            plan_data = sqldetail_data.get('plans')
            bind_data = sqldetail_data.get('binds')
            sqlmon_data = execute_return_json(query_sqlmon)
            exec_delta = defaultdict(list)
            avg_elapse_time = defaultdict(list)
            avg_cpu_time = defaultdict(list)
            avg_crs = defaultdict(list)
            avg_reads = defaultdict(list)
            plan_dic = defaultdict(list)
            stats_dict = defaultdict(dict)
            for x in stat_data:
                phv = str(x.get('PLAN_HASH_VALUE'))
                snap_time = x.get('SNAP_TIME')
                exec_delta[phv].append([snap_time, x.get('EXEC_DELTA')])
                avg_elapse_time[phv].append([snap_time, x.get('AVG_ELAPSE_TIME')])
                avg_cpu_time[phv].append([snap_time, x.get('AVG_CPU_TIME')])
                avg_crs[phv].append([snap_time, x.get('AVG_CRS')])
                avg_reads[phv].append([snap_time, x.get('AVG_READS')])

            stats_dict[''] = exec_delta
            stats_dict['(s)'] = avg_elapse_time
            stats_dict['CPU(s)'] = avg_elapse_time
            stats_dict[''] = avg_crs
            stats_dict[''] = avg_reads
            for x in plan_data:
                phv = str(x.get('PLAN_HASH_VALUE'))
                plan_dic[phv].append(x)

            sql_detail['stats'] = stats_dict
            sql_detail['plans']['data'] = plan_dic
            sql_detail['sqlmon']['data'] = sqlmon_data
            sql_detail['binds']['data'] = bind_data
        if cache == True:
            if audit_data != None:
                if not only_tune:
                    sql_detail['audit'] = audit_data_json
                audit_data_json = get_sql_audit(pk, sql_id, only_tune=only_tune)
                sql_detail['audit'] = audit_data_json
                redis.setex(key_audit, SQLTEXT_RETENTION, json.dumps(audit_data_json))
            if audit_data:
                new_plan_dict = {}
                if plan_dic:
                    new_plan_dict = {k[k.rfind('-') + 1:]:v for k, v in plan_dic.items()}
                tune_data = get_sql_tune(database, audit_data_json, new_plan_dict)
                if tune_data:
                    sql_detail['tune'] = tune_data
        return sql_detail
# okay decompiling ./restful/hawkeye/api/v1/monitor/services/sqldetail/oracleSQLDetail.pyc
