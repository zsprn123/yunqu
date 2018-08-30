# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/monitor/services/schemaService.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 14018 bytes
from monitor.models import Database, Table_Rows
import json
from _collections import defaultdict, OrderedDict
from api.enum.database_enum import Driver
from datetime import datetime
from monitor.models import DB_SCHEMA, Table_Rows
from django.core.exceptions import ObjectDoesNotExist
from api.enum.schema_enum import Schema_Query, DDL_Query, Object_Detail_Query, Type_TO_CN, get_object_type, Ordered_List, CN_TO_Type, sqlserver_schema_data, Rows_Query, sqlserver_rows_data
from api.v1.monitor.services.runsqlService import run_sql, run_batch_sql
from common.util import build_exception_from_java, execute_return_json
from common.storages import redis

def refresh_schema(pk):
    try:
        database = Database.objects.get(pk=pk)
        schema_query = Schema_Query.get(database.db_type)
        schema_data = []
        if database.db_type != 'sqlserver':
            flag, schema_data = run_sql(database, schema_query)
            if not flag:
                raise build_exception_from_java(schema_data)
            else:
                schema_data = sqlserver_schema_data(database)
            schema_dic = defaultdict(OrderedDict)
            type_map = Type_TO_CN.get(database.db_type)
            for x in schema_data:
                owner = x.get('OWNER')
                object_type = type_map.get(x.get('OBJECT_TYPE'))
                object_name = x.get('OBJECT_NAME')
                if not schema_dic.get(owner) or not schema_dic.get(owner).get(object_type):
                    schema_dic[owner][object_type] = []
                schema_dic[owner][object_type].append(object_name)

            detail = OrderedDict(sorted(schema_dic.items()))
            created_at = datetime.now().replace(microsecond=0)
            schema = DB_SCHEMA.objects.update_or_create(database=database, defaults={'detail':detail,  'created_at':created_at})
            Key_Template = f'''{pk}:schema:*'''
            for key in redis.scan_iter(Key_Template):
                redis.delete(key)

            get_table_rows(database)
        return detail
    except ObjectDoesNotExist:
        return {'error_message': ''}
    except Exception as err:
        return {'error_message': str(err)}


def get_schema(pk):
    try:
        database = Database.objects.get(pk=pk)
        schema = (DB_SCHEMA.objects.filter(database=database)).first()
        if not schema:
            return refresh_schema(pk)
        return schema.detail
    except ObjectDoesNotExist:
        return {'error_message': ''}
    except Exception as err:
        return {'error_message': str(err)}


def object_detail(pk, owner, object_name, object_type=None, subobject_name=None, cache=False):
    try:
        schema_name = owner
        key = f'''{pk}:schema:{owner}:{object_name}:{subobject_name}'''
        if cache:
            cache_data = redis.get(key)
            if cache_data:
                return json.loads(cache_data)
            database = Database.objects.get(pk=pk)
            db_type = database.db_type
            type_map = Type_TO_CN.get(database.db_type)
            schema_name = owner
            db_name = None
            if db_type == 'sqlserver':
                db_name, owner = owner.split('.')
            options = {'OWNER':owner, 
             'OBJECT_NAME':object_name, 
             'SUBOBJECT_NAME':subobject_name}
            if not object_type:
                object_type = get_object_type(database, owner, object_name, options, db_name)
                if not object_type:
                    raise Exception('.')
                else:
                    object_type = type_map.get(object_type)
                options['OBJECT_TYPE'] = CN_TO_Type.get(db_type).get(object_type)
                detail_query = {}
                if Object_Detail_Query.get(db_type):
                    if Object_Detail_Query.get(db_type).get(object_type):
                        detail_query = Object_Detail_Query.get(db_type).get(object_type)
                ddl_query = DDL_Query.get(db_type) if DDL_Query.get(db_type) else {}
                if not subobject_name:
                    query = {**detail_query, **ddl_query}
                else:
                    query = detail_query
                if db_type == 'sqlserver':
                    if detail_query:
                        query.pop('DDL')
                query = {k:(v.format(**options)) for k, v in query.items()}
                flag, schema_data = run_batch_sql(database, query, db_name)
                if not flag:
                    raise build_exception_from_java(schema_data)
                if schema_data.get('DDL'):
                    if db_type != 'mysql':
                        schema_data['DDL'] = schema_data.get('DDL')[0].get('DDL') if schema_data.get('DDL') else ''
                if schema_data.get('DDL'):
                    if db_type == 'mysql':
                        ddl_data = schema_data.get('DDL')[0]
                        schema_data['DDL'] = None
                        for k, v in ddl_data.items():
                            if 'create ' in k.lower():
                                schema_data['DDL'] = v

                        if not schema_data['DDL']:
                            for k, v in ddl_data.items():
                                if 'SQL Original Statement' in k:
                                    schema_data['DDL'] = v

                delta_list = []
                total_list = []
                if object_type == '':
                    query_delta = f'''
            select extract(epoch from created_at)*1000 created_at, rows - lag(rows) over (order by created_at) as rows
            from monitor_table_rows where database_id = '{pk}'
            and owner = '{schema_name}' and table_name = '{object_name}'
            order by created_at
            '''
                    query_total = f'''
            select extract(epoch from created_at)*1000 created_at, rows
            from monitor_table_rows where database_id = '{pk}'
            and owner = '{schema_name}' and table_name = '{object_name}'
            order by created_at
            '''
                    delta_list = execute_return_json(query_delta)
                    total_list = execute_return_json(query_total)
                new_schema = OrderedDict()
                for x in Ordered_List:
                    if x in schema_data:
                        new_schema[x] = schema_data.get(x)

                if delta_list:
                    new_schema[''] = {'delta':[[x.get('CREATED_AT'), x.get('ROWS')] for x in delta_list if x.get('ROWS') != None],  'total':[[x.get('CREATED_AT'), x.get('ROWS')] for x in total_list if x.get('ROWS') != None]}
                redis.set(key, json.dumps(new_schema))
        return new_schema
    except ObjectDoesNotExist:
        return {'error_message': ''}
    except Exception as err:
        return {'error_message': str(err)}


def get_table_rows(database):
    try:
        rows_query = Rows_Query.get(database.db_type)
        rows_data = []
        if database.db_type != 'sqlserver':
            flag, rows_data = run_sql(database, rows_query)
            if not flag:
                raise build_exception_from_java(rows_data)
            else:
                rows_data = sqlserver_rows_data(database)
            table_rows_save_list = []
            created_at = datetime.now().replace(microsecond=0)
            for r in rows_data:
                owner = r.get('OWNER')
                table_name = r.get('TABLE_NAME')
                rows = r.get('ROWS')
                table_rows_obj = Table_Rows(database=database, owner=owner, table_name=table_name, rows=rows, created_at=created_at)
                table_rows_save_list.append(table_rows_obj)

            Table_Rows.objects.bulk_create(table_rows_save_list)
    except Exception as err:
        print(err)


def schema_table_rows(pk, owner, time_span=None):
    try:
        if not time_span:
            query_time_span = f'''
            select max(extract(epoch from created_at)) time_span from monitor_table_rows where database_id = '{pk}' and owner = '{owner}'
            '''
            time_span_result = execute_return_json(query_time_span)
            if time_span_result:
                time_span = time_span_result[0].get('TIME_SPAN')
                if time_span is None:
                    return {'error_message': ''}
            else:
                return {'error_message': ''}
            query_total = f'''select sum(rows) as total
     from monitor_table_rows where database_id = '{pk}' and owner = '{owner}' and created_at = to_timestamp({time_span})'''
            query_delta_list = f'''
    select extract(epoch from created_at)*1000 created_at, delta
    from
    (
     select created_at, rows - lag(rows) over (order by created_at) delta, row_number() over(order by created_at) as id
     from
    (
    select created_at, sum(rows) as rows
    from monitor_table_rows where database_id = '{pk}' and owner = '{owner}'
    group by created_at
    ) a
    order by created_at
    ) b where delta is not null and id > 1'''
            query_total_list = f'''
    select extract(epoch from created_at)*1000 created_at, sum(rows) as rows
    from monitor_table_rows where database_id = '{pk}' and owner = '{owner}'
    group by created_at
    order by created_at'''
            query_table_rows_list = f'''
        select owner, table_name, rows,
      rows - (select rows from monitor_table_rows b where '{pk}' = b.database_id and a.table_name = b.table_name and '{owner}' = b.owner and b.created_at = (select max(created_at) from monitor_table_rows where '{pk}' = database_id and '{owner}' = owner and created_at < to_timestamp({time_span}))) rows_lag,
      date_part('day',(to_timestamp({time_span}) - (select max(created_at) from monitor_table_rows where '{pk}' = database_id and '{owner}' = owner and created_at < to_timestamp({time_span})))) +
      round(date_part('hour',(to_timestamp({time_span}) - (select max(created_at) from monitor_table_rows where '{pk}' = database_id and '{owner}' = owner and created_at < to_timestamp({time_span}))))::numeric/24, 1) time_lag      from monitor_table_rows a where database_id = '{pk}' and owner = '{owner}' and created_at = to_timestamp({time_span}) order by rows desc'''
            delta_total_result = execute_return_json(query_total)
            query_delta_result = execute_return_json(query_delta_list)
            query_total_result = execute_return_json(query_total_list)
            query_table_rows_result = execute_return_json(query_table_rows_list)
        return {'total':delta_total_result[0].get('TOTAL') if delta_total_result else None, 
         'time_span':datetime.fromtimestamp(time_span).strftime('%Y-%m-%d %H:%M:%S'), 
         'delta_list':[[x.get('CREATED_AT'), x.get('DELTA')] for x in query_delta_result if x.get('DELTA') != None], 
         'total_list':[[x.get('CREATED_AT'), x.get('ROWS')] for x in query_total_result if x.get('ROWS') != None], 
         'table_rows':query_table_rows_result}
    except ObjectDoesNotExist:
        return {'error_message': ''}
    except Exception as err:
        return {'error_message': str(err)}


def overall_table_rows(pk, time_span=None):
    try:
        if not time_span:
            query_time_span = f'''
            select max(extract(epoch from created_at)) time_span from monitor_table_rows where database_id = '{pk}'
            '''
            time_span_result = execute_return_json(query_time_span)
            if time_span_result:
                time_span = time_span_result[0].get('TIME_SPAN')
                if time_span is None:
                    return {'error_message': ''}
            else:
                return {'error_message': ''}
            query_total = f'''select sum(rows) as total
     from monitor_table_rows where database_id = '{pk}' and created_at = to_timestamp({time_span})'''
            query_delta_list = f'''
    select extract(epoch from created_at)*1000 created_at, delta
    from
    (
     select created_at, rows - lag(rows) over (order by created_at) delta, row_number() over(order by created_at) as id
     from
    (
    select created_at, sum(rows) as rows
    from monitor_table_rows where database_id = '{pk}'
    group by created_at
    ) a
    order by created_at
    ) b where delta is not null and id > 1'''
            query_total_list = f'''
    select extract(epoch from created_at)*1000 created_at, sum(rows) as rows
    from monitor_table_rows where database_id = '{pk}'
    group by created_at
    order by created_at'''
            query_table_rows_list = f'''
with v as (
select created_at, table_name, sum(rows) as rows
from monitor_table_rows where '{pk}' = database_id and created_at = to_timestamp({time_span})
group by created_at, table_name
),
v1 as (
select created_at, table_name, sum(rows) as rows
from monitor_table_rows where '{pk}' = database_id and created_at = (select max(created_at) from monitor_table_rows where '{pk}' = database_id and created_at < to_timestamp({time_span}))
group by created_at, table_name
)
select
  table_name, rows,
  rows - (select rows from v1 where v1.table_name = v.table_name) rows_lag,
  date_part('day',(to_timestamp({time_span}) - (select created_at from v1 limit 1))) +
  round(date_part('hour',(to_timestamp({time_span}) - (select created_at from v1 limit 1)))::numeric/24, 1) time_lag
  from v order by rows desc
  '''
            delta_total_result = execute_return_json(query_total)
            query_delta_result = execute_return_json(query_delta_list)
            query_total_result = execute_return_json(query_total_list)
            query_table_rows_result = execute_return_json(query_table_rows_list)
        return {'total':delta_total_result[0].get('TOTAL') if delta_total_result else None, 
         'time_span':datetime.fromtimestamp(time_span).strftime('%Y-%m-%d %H:%M:%S'), 
         'delta_list':[[x.get('CREATED_AT'), x.get('DELTA')] for x in query_delta_result if x.get('DELTA') != None], 
         'total_list':[[x.get('CREATED_AT'), x.get('ROWS')] for x in query_total_result if x.get('ROWS') != None], 
         'table_rows':query_table_rows_result}
    except ObjectDoesNotExist:
        return {'error_message': ''}
    except Exception as err:
        return {'error_message': str(err)}
# okay decompiling ./restful/hawkeye/api/v1/monitor/services/schemaService.pyc
