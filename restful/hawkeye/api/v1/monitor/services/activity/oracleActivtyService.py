# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/monitor/services/activity/oracleActivtyService.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 7295 bytes
from api.enum.activity_enum import MysqlActivityType, OracleActivityType, get_default_ash
from api.v1.monitor.services.runsqlService import data2result, data2result_json
from common.util import execute_ash_return_json, has_instance, get_timestamp, get_1s_timestamp
import requests, time
NUM_RANGE = {'realtime':360, 
 'day':144, 
 'week':1008, 
 'month':744, 
 'quarter':2232, 
 'year':8784}
GRANULE_RANGE = {'realtime':10, 
 'day':600, 
 'week':600, 
 'month':3600, 
 'quarter':3600, 
 'year':3600}
INTERVAL_RANGE = {'realtime':'1 hours', 
 'day':'1 days', 
 'week':'7 days', 
 'month':'1 months', 
 'quarter':'3 months', 
 'year':'1 years'}

def get_oracle_activity(database, time_span=None, instance_id=None, sql_id_filter=None, begin_time=None, end_time=None):
    result = {}
    database_id = database.id
    instance_id_list_str = database.instance_id_list
    instance_id_list = instance_id_list_str.split(',')
    if database.instance_count > 1:
        instance_id_list.append(instance_id_list_str)
    if time_span == 'realtime':
        for inst_id in instance_id_list:
            now_timestamp = get_1s_timestamp()
            query = f'''WITH RECURSIVE
                      cnt(x) AS (
                         values(1)
                         UNION ALL
                         SELECT x+1 FROM cnt
                          where x < 360
                      ),
                    ashdata as(
                        select
                            wait_class ,  count(*) aas, extract(epoch from created_at) created_at
                        from monitor_oracle_ash
                        where created_at > TIMESTAMP 'now' - interval '1 hours'
                                and database_id = '{database_id}'
                                and inst_id in ({inst_id}) {sql_id_filter}
                        group by
                            wait_class,  created_at order by created_at desc),
                    ash_state as (select 'ON CPU' wait_class union all select 'Other' union all select 'Application' union all select 'Configuration' union all select 'Cluster' union all select 'Administrative' union all select 'Concurrency' union all select 'Commit' union all select 'Network' union all select 'User I/O' union all select 'System I/O' union all select 'Scheduler' union all select 'Queueing'),
                    ash_placehoder as (select {now_timestamp}
                                  - x*10 created_at, wait_class from cnt, ash_state)
                    select
                        t1.wait_class,cast(COALESCE(t2.aas, 0) as real) aas, cast(COALESCE(t1.created_at) as bigint) *1000 created_at
                    from
                        ash_placehoder t1 left outer join ashdata t2
                    on t1.wait_class = t2.wait_class and t1.created_at = t2.created_at
                    order by t1.wait_class, t1.created_at'''
            data_dict = execute_ash_return_json(query)
            if inst_id == instance_id_list_str or not has_instance(database):
                result[database.db_name] = data2result_json(data_dict, OracleActivityType)
            else:
                result[inst_id] = data2result_json(data_dict, OracleActivityType)

        return result
    inst_id_list = database.instance_id_list if not instance_id or instance_id == database.db_name else instance_id
    key = instance_id if instance_id else database.db_name
    time = int(end_time) - int(begin_time)
    if time <= 3600:
        num1 = int(time / 10)
        num2 = 10
    else:
        if time <= 86400:
            num1 = 144
            num2 = 600
        else:
            if time <= 604800:
                num1 = 1008
                num2 = 600
            else:
                if time <= 2678400:
                    num1 = 744
                    num2 = 3600
                else:
                    if time <= 8035200:
                        num1 = 2232
                        num2 = 3600
                    else:
                        if time <= 31622400:
                            num1 = 8784
                            num2 = 3600
                        else:
                            num1 = 144
                            num2 = 600
                        max_point = int(end_time) - int(end_time) % num2
                        query = f'''WITH RECURSIVE
                  cnt(x) AS (
                     values(1)
                     UNION ALL
                     SELECT x+1 FROM cnt
                      where x < {num1}
                  ),
                ashdata as(
                    select wait_class , cast(extract(epoch from created_at) as bigint) - mod(cast(extract(epoch from created_at) as bigint),{num2}) created_at, 10.0*count(*)/{num2} aas
                    from monitor_oracle_ash
                    where created_at between to_timestamp({begin_time}) and to_timestamp({end_time})
                            and database_id = '{database_id}' and inst_id in ({inst_id_list}) {sql_id_filter}
                    group by
                        wait_class, cast(extract(epoch from created_at) as bigint) - mod(cast(extract(epoch from created_at) as bigint),{num2}) order by created_at desc),
                ash_state as (select distinct wait_class from ashdata union select 'ON CPU' wait_class),
                ash_placehoder as (select {max_point} - x*{num2} created_at, wait_class from cnt, ash_state)
                select
                    t1.wait_class, cast(COALESCE(t2.aas, 0) as real) aas, cast(t1.created_at as bigint) *1000 created_at
                from
                    ash_placehoder t1 left outer join ashdata t2
                on t1.wait_class = t2.wait_class and t1.created_at = t2.created_at
                order by t1.wait_class, t1.created_at'''
                        data_dict = execute_ash_return_json(query)
                        result[key] = data2result_json(data_dict, OracleActivityType)
                        return result


def get_oracle_activity_ws(database):
    result = {}
    database_id = database.id
    instance_id_list_str = database.instance_id_list
    instance_id_list = instance_id_list_str.split(',')
    now_timestamp = get_1s_timestamp()
    if database.instance_count > 1:
        instance_id_list.append(instance_id_list_str)
    for inst_id in instance_id_list:
        query = f'''select
                    wait_class, count(*) aas , cast(extract(epoch from created_at) as bigint) * 1000 created_at
                from monitor_oracle_ash
                where database_id = '{database_id}'
                    and inst_id in ({inst_id})
                    and created_at = to_timestamp({now_timestamp})
                group by
                    wait_class, created_at'''
        data = execute_ash_return_json(query)
        if inst_id == instance_id_list_str or not has_instance(database):
            result[database.db_name] = (data2result_json(data, OracleActivityType, is_open=False, is_realtime=True)) if data else get_default_ash('oracle')
        else:
            result[inst_id] = (data2result_json(data, OracleActivityType, is_open=False, is_realtime=True)) if data else get_default_ash('oracle')

    return result
# okay decompiling ./restful/hawkeye/api/v1/monitor/services/activity/oracleActivtyService.pyc
