# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/monitor/services/performance/performanceService.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 14270 bytes
from api.enum.database_enum import DatabaseType
from api.enum.performance_enum import MySQLPerformanceType, SQLServerPerformanceType, DB2PerformanceType, OraclePerformanceType
from api.v1.monitor.services.runsqlService import data2result, data2result_oracle
from common.util import new_execute_ash_return_json, has_instance, enum2str, new_execute_performance_return_json, new_execute_cpu_return_json, get_1s_timestamp
from monitor.models import Database
from django.core.cache import cache
PERFORMANCE_DICT = {DatabaseType.MYSQL.value: MySQLPerformanceType, 
 DatabaseType.SQLSERVER.value: SQLServerPerformanceType, 
 DatabaseType.DB2.value: DB2PerformanceType}

class Performance(object):
    """
    
    """

    def __init__(self, database):
        if not isinstance(database, Database):
            raise AssertionError(('The `database` argument must be an instance of `monitor.models.Database`, not `{}.{}`.').format(database.__class__.__module__, database.__class__.__name__))
        self.database = database

    def get_realtime_data(self):
        """
        
        
        :param
        :return:
        """
        pass

    def get_history_data(self, instance_id=None):
        """
        ()
        
        :param
        :return:
        """
        database = self.database
        performance_name = enum2str(PERFORMANCE_DICT.get(database.db_type))
        query = f'''select name_id, avg(value), cast(extract(epoch from created_at) as bigint)*1000 from monitor_performance 
                where database_id = '{(database.id)}' and created_at > TIMESTAMP 'now' - interval '1 hours' 
                and name_id in ({performance_name}) group by database_id,name_id,created_at order by name_id, created_at
                '''
        return self.run_query(query)

    def get_history_data_by_range(self, begin_time, end_time, instance_id=None):
        """
        
        :param instance_id:  id
        :param begin_time: 
        :param end_time: 
        
        :return:
        """
        database = self.database
        performance_name = enum2str(PERFORMANCE_DICT.get(database.db_type))
        group_by_clause = "group by database_id, name_id, date_trunc('minute', created_at)" if int(end_time) - int(begin_time) <= 604800 else "group by database_id, name_id, date_trunc('hour', created_at)"
        filter_by_clause = f'''created_at between to_timestamp({begin_time}) and to_timestamp({end_time})'''
        query = f'''select name_id, avg(value), cast(extract(epoch from min(created_at)) as bigint)*1000 from monitor_performance 
                where database_id = '{(database.id)}' and {filter_by_clause}
                and name_id in ({performance_name}) {group_by_clause} order by name_id, 3'''
        result = {}
        data = new_execute_ash_return_json(query)
        result = data2result(data, PERFORMANCE_DICT.get(database.db_type))
        return result

    def run_query(self, query):
        database = self.database
        result = {}
        data = new_execute_ash_return_json(query)
        result[database.alias] = data2result(data, PERFORMANCE_DICT.get(database.db_type))
        return result


class OraclePerformance(Performance):
    """
    Oracle 
    """
    PERFORMANCE_NAME = enum2str(OraclePerformanceType)
    PERFORMANCE_CPU_NAME = OraclePerformanceType['CPU'].value
    PERFORMANCE_WAIT_NAME = OraclePerformanceType['WAIT'].value

    def get_history_data(self, instance_id=None):
        database = self.database
        data = {}
        result = {}
        instance_id_list_str = instance_id if instance_id else database.instance_id_list
        instance_id_list = instance_id_list_str.split(',')
        instance_id_list.append(instance_id_list_str)
        database_id = str(database.id)
        for inst_id in instance_id_list:
            query_sum = f'''select name_id, sum(value), cast(extract(epoch from min(created_at)) as bigint)*1000
                            from monitor_performance
                            where database_id = '{database_id}' and inst_id in ({inst_id}) and created_at > TIMESTAMP 'now' - interval '1 hours' and name_id in ({(self.PERFORMANCE_NAME)})
                            group by database_id,name_id,created_at order by name_id, min(created_at)'''
            data.update(new_execute_ash_return_json(query_sum))
            query_cpu = f'''select name_id, inst_id, value, cast(extract(epoch from created_at) as bigint)*1000 
                            from monitor_performance
                            where database_id = '{database_id}' and inst_id in ({inst_id}) and created_at > TIMESTAMP 'now' - interval '1 hours' and name_id in ({(self.PERFORMANCE_CPU_NAME)})
                            order by inst_id, created_at'''
            data.update(new_execute_cpu_return_json(query_cpu))
            query_avg = f'''select name_id, max(value), cast(extract(epoch from min(created_at)) as bigint)*1000
                            from monitor_performance 
                            where database_id = '{database_id}' and inst_id in ({inst_id}) and created_at > TIMESTAMP 'now' - interval '1 hours' and name_id in ({(self.PERFORMANCE_WAIT_NAME)})
                            group by database_id,name_id,created_at order by name_id, min(created_at)'''
            data.update(new_execute_ash_return_json(query_avg))
            if not has_instance(database):
                result[database.db_name] = data2result_oracle(data, OraclePerformanceType)
            elif inst_id == instance_id_list_str:
                result[database.db_name] = data2result_oracle(data, OraclePerformanceType)
            else:
                result[inst_id] = data2result_oracle(data, OraclePerformanceType)

        return result

    def get_history_data_by_range(self, begin_time, end_time, instance_id=None):
        database = self.database
        data = {}
        result = {}
        cache_key_prefix = ''
        need_cache = True
        span_time = int(end_time) - int(begin_time)
        if span_time <= 3600:
            date_trunc = 'minute'
            need_cache = False
        else:
            if span_time <= 86400:
                date_trunc = 'minute'
                cache_key_prefix = 'day'
            else:
                if span_time <= 604800:
                    date_trunc = 'hour'
                    cache_key_prefix = 'week'
                else:
                    if span_time <= 2592000:
                        date_trunc = 'hour'
                        cache_key_prefix = 'month'
                    else:
                        if span_time <= 7776000:
                            date_trunc = 'hour'
                            cache_key_prefix = '3month'
                        else:
                            date_trunc = 'hour'
                            cache_key_prefix = 'year'
                        database_id = database.id
                        instance_id_list = database.instance_id_list if not instance_id or instance_id == database.db_name else instance_id
                        list_for_count = database.instance_id_list.split(',')
                        instance_count = len(list_for_count)
                        if need_cache:
                            if cache.get('performance-data' + str(database_id) + str(instance_id_list) + cache_key_prefix, None):
                                return cache.get('performance-data' + str(database_id) + str(instance_id_list) + cache_key_prefix)
                            group_by_clause = f'''group by database_id, name_id, date_trunc('{date_trunc}', created_at)'''
                            group_by_clause_cpu = f'''group by database_id, inst_id, name_id, date_trunc('{date_trunc}', created_at)'''
                            filter_by_clause = f'''created_at between to_timestamp({begin_time}) and to_timestamp({end_time})'''
                            query_sum = f'''select name_id, avg(value)*{instance_count}, cast(extract(epoch from min(created_at)) as bigint)*1000 from monitor_performance
                    where database_id = '{database_id}' and inst_id in ({instance_id_list}) and {filter_by_clause}
                    and name_id in ({(self.PERFORMANCE_NAME)}) {group_by_clause} order by name_id, 3'''
                            data.update(new_execute_ash_return_json(query_sum))
                            query_cpu = f'''select name_id,inst_id, max(value), cast(extract(epoch from min(created_at)) as bigint)*1000 from monitor_performance 
                    where database_id = '{database_id}' and inst_id in ({instance_id_list}) and {filter_by_clause} 
                    and name_id in ({(self.PERFORMANCE_CPU_NAME)}) {group_by_clause_cpu} order by inst_id, min(created_at)'''
                            data.update(new_execute_cpu_return_json(query_cpu))
                            query_avg = f'''select name_id, max(value), cast(extract(epoch from min(created_at)) as bigint)*1000 from monitor_performance 
                    where database_id = '{database_id}' and inst_id in ({instance_id_list}) and {filter_by_clause} 
                    and name_id in ({(self.PERFORMANCE_WAIT_NAME)}) {group_by_clause} order by name_id, 3'''
                            data.update(new_execute_ash_return_json(query_avg))
                            result = data2result_oracle(data, OraclePerformanceType)
                            cache.set('performance-data' + str(database_id) + str(instance_id_list) + cache_key_prefix, result, timeout=3600)
                            return result

    def get_realtime_data(self):
        database = self.database
        data_dic = {}
        result = {}
        instance_id_list_str = database.instance_id_list
        instance_id_list = instance_id_list_str.split(',')
        instance_id_list.append(instance_id_list_str)
        database_id = database.id
        now_timestamp = get_1s_timestamp()
        for inst_id in instance_id_list:
            query_sum = f'''select name_id, sum(value), cast(extract(epoch from min(created_at)) as bigint)*1000 from monitor_performance
                        where database_id ='{database_id}' and inst_id in ({inst_id}) 
                        and created_at = to_timestamp({now_timestamp})
                        and name_id in ({(self.PERFORMANCE_NAME)})
                        group by database_id,name_id,created_at'''
            data_dic.update(new_execute_ash_return_json(query_sum))
            query_cpu = f'''select name_id, inst_id, value, cast(extract(epoch from created_at) as bigint)*1000 from monitor_performance
                        where database_id = '{database_id}' and inst_id in ({inst_id}) 
                        and created_at = to_timestamp({now_timestamp})
                        and name_id in ({(self.PERFORMANCE_CPU_NAME)})'''
            data_dic.update(new_execute_cpu_return_json(query_cpu))
            query_avg = f'''select name_id, max(value), cast(extract(epoch from min(created_at)) as bigint)*1000 from monitor_performance
                        where database_id = '{database_id}' and inst_id in ({inst_id}) 
                        and created_at = to_timestamp({now_timestamp})
                        and name_id in ({(self.PERFORMANCE_WAIT_NAME)})
                        group by database_id,name_id,created_at'''
            data_dic.update(new_execute_ash_return_json(query_avg))
            if not has_instance(database):
                result[database.db_name] = data2result_oracle(data_dic, OraclePerformanceType, is_open=False, is_realtime=True)
            elif inst_id == instance_id_list_str:
                result[database.db_name] = data2result_oracle(data_dic, OraclePerformanceType, is_open=False, is_realtime=True)
            else:
                result[inst_id] = data2result_oracle(data_dic, OraclePerformanceType, is_open=False, is_realtime=True)

        return result


class MysqlPerformance(Performance):

    def get_realtime_data(self):
        database = self.database
        result = {}
        query = ("select name_id, avg(value), cast(extract(epoch from created_at) as bigint)*1000  from monitor_performance where database_id = '{}'  and created_at = timestamp 'now' - EXTRACT(SECOND FROM TIMESTAMP 'now') * interval '1 seconds' and name_id in ({}) group by database_id,name_id,created_at").format(database.id, enum2str(MySQLPerformanceType))
        data_dic = new_execute_performance_return_json(query)
        result[database.alias] = data2result(data_dic, MySQLPerformanceType, is_open=False)
        return result


class DB2Performance(Performance):

    def get_realtime_data(self):
        database = self.database
        result = {}
        query = ("with max_t as (select max(created_at) t from monitor_performance where database_id = '{}') select name_id, avg(value), cast(extract(epoch from created_at) as bigint)*1000 from monitor_performance, max_t where database_id = '{}' and created_at = t and name_id in ({}) group by database_id,name_id,created_at").format(database.id, database.id, enum2str(DB2PerformanceType))
        data_dic = new_execute_performance_return_json(query)
        result[database.alias] = data2result(data_dic, DB2PerformanceType, is_open=False)
        return result


class SqlserverPerformance(Performance):

    def get_realtime_data(self):
        database = self.database
        result = {}
        query = ("select name_id, avg(value), cast(extract(epoch from created_at) as bigint)*1000  from monitor_performance where database_id = '{}'  and created_at = timestamp 'now' - EXTRACT(SECOND FROM TIMESTAMP 'now') * interval '1 seconds' and name_id in ({}) group by database_id,name_id,created_at").format(database.id, enum2str(SQLServerPerformanceType))
        data_dic = new_execute_performance_return_json(query)
        result[database.alias] = data2result(data_dic, SQLServerPerformanceType, is_open=False)
        return result


PERFORMANCE_FUNCTION = {DatabaseType.ORACLE.value: OraclePerformance, 
 DatabaseType.DB2.value: DB2Performance, 
 DatabaseType.MYSQL.value: MysqlPerformance, 
 DatabaseType.SQLSERVER.value: SqlserverPerformance}
# okay decompiling ./restful/hawkeye/api/v1/monitor/services/performance/performanceService.pyc
