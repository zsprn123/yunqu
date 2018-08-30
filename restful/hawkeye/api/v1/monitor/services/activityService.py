# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/monitor/services/activityService.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 15372 bytes
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from api.enum.activity_enum import MysqlActivityType, get_default_ash, DB2ActivityType, ash_dimension_data, get_sql_id_filter_str, ASH_CHAIN_QUERY, Activity_Table_Name, Wait_Class_Column, Wait_Class, Activity_Type
from api.enum.database_enum import DatabaseType
from api.v1.monitor.services.activity.oracleActivtyService import get_oracle_activity, get_oracle_activity_ws
from api.v1.monitor.services.runsqlService import data2result_json, run_sql
from common.util import execute_ash_return_json, execute_query_return_top_dimension, get_1s_timestamp
from monitor.models import Database
from common.util import execute_return_json

def get_database_activity(pk, time_span=None, instance_id=None, sql_id=None, session_id=None, begin_time=None, end_time=None):
    try:
        conn = Database.objects.get(pk=pk)
        db_type = conn.db_type
        sql_id_filter = get_sql_id_filter_str(db_type, sql_id, session_id) if sql_id or session_id else ''
        result = {}
        now_timestamp = get_1s_timestamp()
        ash_table = Activity_Table_Name.get(db_type)
        wait_class = Wait_Class_Column.get(db_type)
        all_wait_class = (' union all ').join([("select '{}'").format(x) if idx != 0 else ("select '{}' {}").format(x, wait_class) for idx, x in enumerate(Wait_Class.get(db_type))])
        first_wait_class = ("select '{}' {}").format(Wait_Class.get(db_type)[0], wait_class)
        activity_type = Activity_Type.get(db_type)
        if conn.db_type != DatabaseType.ORACLE.value:
            if time_span == 'realtime':
                query = f'''WITH RECURSIVE
                          cnt(x) AS (
                             values(1)
                             UNION ALL
                             SELECT x+1 FROM cnt
                              where x < 360
                          ),
                        ashdata as(
                            select
                                {wait_class},  count(*) aas, extract(epoch from created_at) created_at
                            from {ash_table}
                            where created_at > TIMESTAMP 'now' - interval '1 hours'
                                    and database_id = '{pk}'
                                    {sql_id_filter}
                            group by
                                {wait_class},  created_at order by created_at desc),
                        ash_state as ({all_wait_class}),
                        ash_placehoder as (select {now_timestamp}
                                      - x*10 created_at, {wait_class} from cnt, ash_state)
                        select
                            t1.{wait_class},cast(COALESCE(t2.aas, 0) as real) aas, cast(COALESCE(t1.created_at) as bigint) *1000 created_at
                        from
                            ash_placehoder t1 left outer join ashdata t2
                        on t1.{wait_class} = t2.{wait_class} and t1.created_at = t2.created_at
                        order by t1.{wait_class}, t1.created_at'''
            else:
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
                            select {wait_class} , cast(extract(epoch from created_at) as bigint) - mod(cast(extract(epoch from created_at) as bigint),{num2}) created_at, 10.0*count(*)/{num2} aas
                            from {ash_table}
                            where created_at between to_timestamp({begin_time}) and to_timestamp({end_time})
                                    and database_id = '{pk}' {sql_id_filter}
                            group by
                                {wait_class}, cast(extract(epoch from created_at) as bigint) - mod(cast(extract(epoch from created_at) as bigint),{num2}) order by created_at desc),
                        ash_state as (select distinct {wait_class} from ashdata union {first_wait_class}),
                        ash_placehoder as (select {max_point} - x*{num2} created_at, {wait_class} from cnt, ash_state)
                        select
                            t1.{wait_class}, cast(COALESCE(t2.aas, 0) as real) aas, cast(t1.created_at as bigint) *1000 created_at
                        from
                            ash_placehoder t1 left outer join ashdata t2
                        on t1.{wait_class} = t2.{wait_class} and t1.created_at = t2.created_at
                        order by t1.{wait_class}, t1.created_at'''
                data_dict = execute_ash_return_json(query)
                result[conn.alias] = data2result_json(data_dict, activity_type)
            return result
        if conn.db_type == DatabaseType.ORACLE.value:
            result = get_oracle_activity(conn, time_span, instance_id, sql_id_filter, begin_time, end_time)
            return result
    except ObjectDoesNotExist:
        return {'error_message': ''}
    except Exception as err:
        return {'error_message': str(err)}


def get_activity_realtime(pk):
    try:
        conn = Database.objects.get(pk=pk)
        result = {}
        db_type = conn.db_type
        now_timestamp = get_1s_timestamp()
        ash_table = Activity_Table_Name.get(db_type)
        wait_class = Wait_Class_Column.get(db_type)
        activity_type = Activity_Type.get(db_type)
        if db_type != 'oracle':
            query = f'''select
                        {wait_class}, count(*) aas , cast(extract(epoch from created_at) as bigint) * 1000 created_at
                    from {ash_table}
                    where database_id = '{pk}'
                        and created_at = to_timestamp({now_timestamp})
                    group by
                        {wait_class}, created_at'''
            data = execute_ash_return_json(query)
            if data:
                result[conn.alias] = data2result_json(data, activity_type, is_open=False, is_realtime=True)
            else:
                result[conn.db_name] = get_default_ash(db_type)
            return result
        if db_type == 'oracle':
            result = get_oracle_activity_ws(conn)
            return result
    except ObjectDoesNotExist:
        return {'message': ''}
    except Exception as err:
        return {'error_message': str(err)}


def get_activity_dimension(pk, instance_id=None, sql_id=None, session_id=None, begin_time=None, end_time=None, dim=0, limit=10):
    try:
        data, wait_class_list, table_header = ash_dimension_data(pk, instance_id, sql_id, session_id, begin_time, end_time, dim)
        data['limit'] = limit
        query = '\n            with v as (\n                select count(*) cnt FROM %(ash_name)s\n                    where created_at between to_timestamp(%(start_time)s)\n                        and to_timestamp(%(end_time)s)\n                        and %(id_filter)s %(sql_id_filter)s)\n            select * from\n            (\n                select\n                    %(group_list)s,\n                    cast(round(100.0*count(*)/max(v.cnt)::numeric,1) as real) pct,\n                    cast(round(10.0*COUNT(*)/(%(end_time)s-%(start_time)s)::numeric,1) as real) AAS,\n                    %(wait_class_list)s\n                FROM %(ash_name)s, v\n                    where created_at between to_timestamp(%(start_time)s)\n                        and to_timestamp(%(end_time)s)\n                        and %(id_filter)s %(sql_id_filter)s\n                group by %(group_by_list)s\n                order by count(*) desc) as foo limit %(limit)s' % data
        result = execute_query_return_top_dimension(query, wait_class_list, len(table_header) - 2, table_header)
        return {'data':result, 
         'header':table_header}
    except ObjectDoesNotExist:
        return {'error_message': ''}
    except Exception as err:
        return {'error_message': str(err)}


def get_activity_tuning_report(pk, instance_id=None, begin_time=None, end_time=None, limit=20):
    from api.v1.monitor.services.sqldetail.oracleSQLDetail import oracle_sql_detail
    database = Database.objects.get(pk=pk)
    if instance_id == database.db_name:
        instance_id = None
    result = get_activity_dimension(pk, instance_id=instance_id, begin_time=begin_time, end_time=end_time, dim=0, limit=limit)
    sql_tune_result = {}
    tune_impact = {}
    sql_activity_list = result.get('data')
    topsql_list = []
    for x in sql_activity_list:
        sql_id = x.get('SQL_ID')
        if sql_id != 'null':
            detail_data = oracle_sql_detail(pk, sql_id, time_span='realtime', only_tune=True)
            stats = detail_data.get('stats')
            tune_data = detail_data.get('tune')
            if tune_data:
                sql_tune_result[sql_id] = tune_data
                tune_impact[sql_id] = x.get('(%)')
                if stats:
                    stats_dict = next(iter(stats.values()))
                    execution_stats_data = stats_dict.get('execution_stats').get('data')
                    if execution_stats_data:
                        x[''] = execution_stats_data[0].get('')
                        x['()'] = execution_stats_data[1].get('')
                        x['CPU()'] = execution_stats_data[2].get('')
                        x[''] = execution_stats_data[3].get('')
                        x[''] = execution_stats_data[4].get('')
                        x[''] = execution_stats_data[6].get('')
                        topsql_list.append(x)

    tune_result_list = []
    tune_result = {}
    for sql_id, tune_data in sql_tune_result.items():
        for tune_type, tune_list in tune_data.items():
            for x in tune_list:
                tune_item = tune_result.get(x)
                if tune_item:
                    tune_result[x] = {u'\u5f71\u54cdsql\u5217\u8868':tune_result[x].get('sql') + ', ' + sql_id, 
                     u'\u6d3b\u52a8\u6bd4\u4f8b(%)':merge_activity_percent(tune_result[x].get('(%)'), tune_impact[sql_id]), 
                     u'\u4f18\u5316\u7c7b\u578b':tune_type}
                else:
                    tune_result[x] = {u'\u5f71\u54cdsql\u5217\u8868':sql_id, 
                     u'\u6d3b\u52a8\u6bd4\u4f8b(%)':tune_impact[sql_id],  u'\u4f18\u5316\u7c7b\u578b':tune_type}

    for k, v in tune_result.items():
        v[''] = k
        tune_result_list.append(v)

    sorted_tune_result_list = sorted(tune_result_list, key=lambda k: k.get('(%)').get('percent'), reverse=True)
    total_pct = sum([x.get('(%)').get('percent') for x in sql_activity_list])
    tune_pct = sum([x.get('(%)').get('percent') for x in tune_result_list])
    activity_result = {'tuning_list':sorted_tune_result_list, 
     'topsql_list':topsql_list, 
     'total_pct':total_pct, 
     'tune_pct':tune_pct}
    return activity_result


def get_sql_perf(pk, sql_id_list):
    from api.v1.monitor.services.sqldetail.oracleSQLDetail import oracle_sql_detail
    if not sql_id_list:
        return
    else:
        sql_id_list_splitted = list(set(sql_id_list.split(',')))
        topsql_list = []
        for x in sql_id_list_splitted:
            if x:
                sql_id = x
                sql_element = {}
                sql_element['sql_id'] = sql_id
                if sql_id != 'null':
                    detail_data = oracle_sql_detail(pk, sql_id, time_span='realtime', only_tune=True)
                    stats = detail_data.get('stats')
                    tune_data = detail_data.get('tune')
                    if stats:
                        stats_dict = next(iter(stats.values()))
                        execution_stats_data = stats_dict.get('execution_stats').get('data')
                        if execution_stats_data:
                            sql_element[''] = execution_stats_data[0].get('')
                            sql_element['()'] = execution_stats_data[1].get('')
                            sql_element['CPU()'] = execution_stats_data[2].get('')
                            sql_element[''] = execution_stats_data[3].get('')
                            sql_element[''] = execution_stats_data[4].get('')
                            sql_element[''] = execution_stats_data[6].get('')
                            topsql_list.append(sql_element)

        return topsql_list


def merge_activity_percent(d1, d2):
    pct = d1.get('percent') + d2.get('percent')
    bar_data1 = d1.get('bar_data')
    bar_data2 = d2.get('bar_data')
    bar_dict = {}
    for x in bar_data1:
        bar_dict = {**bar_dict, **x}

    for x in bar_data2:
        bar_dict = {k:x.get(k, 0) + bar_dict.get(k, 0) for k in set(x) | set(bar_dict)}

    return {'percent':pct, 
     'bar_data':[{k: v} for k, v in bar_dict.items()]}


def get_ash_chain(pk, instance_id=None, begin_time=None, end_time=None):
    try:
        conn = Database.objects.get(pk=pk)
        inst_id_pred = ''
        if conn.instance_count > 1:
            if instance_id != None or instance_id != conn.db_name:
                if instance_id == conn.db_name:
                    instance_id = conn.instance_id_list
                inst_id_pred = (' and inst_id in ({})').format(instance_id)
        options = {'pk':pk,  'begin_time':begin_time, 
         'end_time':end_time, 
         'inst_id_pred':inst_id_pred}
        query = ASH_CHAIN_QUERY.get(conn.db_type).format(**options)
        result = execute_return_json(query)
        return result
    except ObjectDoesNotExist:
        return {'error_message': ''}
    except Exception as err:
        return {'error_message': str(err)}
# okay decompiling ./restful/hawkeye/api/v1/monitor/services/activityService.pyc
