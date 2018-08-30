# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/monitor/services/spaceService.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 4338 bytes
from django.core.exceptions import ObjectDoesNotExist
from api.celery.common.space import get_space
from api.enum.space_enum import Space_Total_Query, SQLServer_Space_Total_Query, Space_Detail_Lag_Query, Space_Realtime_Query, Space_Total_Lag_Query, reprocess_query, Space_Detail_Realtime_Query, is_temp
from api.v1.monitor.services.runsqlService import run_batch_sql
from common.util import execute_return_json, build_exception_from_java
from monitor.models import Space_Detail, Database

def space_info(pk, days=7):
    try:
        database = Database.objects.get(pk=pk)
        db_type = database.db_type
        options = {'pk':pk, 
         'days':days}
        space_detail = (Space_Detail.objects.filter(database=database)).first()
        if not space_detail:
            get_space(database)
            space_detail = (Space_Detail.objects.filter(database=database)).first()
        space_detail = space_detail.detail if space_detail else {}
        space_total_query = Space_Total_Query if db_type != 'sqlserver' else SQLServer_Space_Total_Query
        query = reprocess_query(space_total_query, options)
        total_space = execute_return_json(query)
        query = reprocess_query(Space_Total_Lag_Query, options)
        total_trend = execute_return_json(query)
        if db_type == 'oracle':
            query = reprocess_query(Space_Realtime_Query.get(db_type), options)
            flag, json_data = run_batch_sql(database, query)
            if not flag:
                raise build_exception_from_java(json_data)
            else:
                json_data = {}
        local_data = {'space_detail':space_detail, 
         'total_space':total_space[0] if total_space else {}, 
         'total_trend':{'name':'(MB)', 
          'data':[[x.get('CREATED_AT'), x.get('DELTA')] for x in total_trend]}}
        json_data['switch_trend'] = {'name':'', 
         'data':[[x.get('TIME'), x.get('COUNT')] for x in json_data.get('switch_trend', [])]}
        space_summary = {**local_data, **json_data}
        return space_summary
    except ObjectDoesNotExist:
        return {'error_message': ''}
    except Exception as err:
        return {'error_message': str(err)}


def detail_info(pk, name, days=7, limit=200):
    try:
        database = Database.objects.get(pk=pk)
        db_type = database.db_type
        options = {'pk':pk, 
         'days':days, 
         'limit':limit, 
         'name':name}
        space_detail = (Space_Detail.objects.filter(database=database)).first()
        if not space_detail:
            get_space(database)
            space_detail = (Space_Detail.objects.filter(database=database)).first()
        name_detail = {}
        for x in space_detail.detail:
            if x.get('TABLESPACE_NAME') == name:
                name_detail = x
                break

        query = reprocess_query(Space_Detail_Lag_Query, options)
        space_trend = execute_return_json(query)
        query = reprocess_query(Space_Detail_Realtime_Query.get(db_type), options)
        if not is_temp(db_type, name_detail):
            if db_type in ('db2', 'oracle'):
                query.pop('temp')
        if db_type == 'sqlserver':
            flag, json_data = run_batch_sql(database, query, name)
        else:
            flag, json_data = run_batch_sql(database, query)
        if not flag:
            raise build_exception_from_java(json_data)
        detail_data = {'space_detail':name_detail, 
         'space_trend':{'name':'(MB)', 
          'data':[[x.get('CREATED_AT'), x.get('DELTA')] for x in space_trend]}, 
         'table_data':json_data.get('segment') if json_data else [], 
         'temp':json_data.get('temp') if json_data else []}
        if db_type != 'mysql':
            detail_data['datafile'] = json_data.get('datafile') if json_data.get('datafile') else []
        return detail_data
    except ObjectDoesNotExist:
        return {'error_message': ''}
# okay decompiling ./restful/hawkeye/api/v1/monitor/services/spaceService.pyc
