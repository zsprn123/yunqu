# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/monitor/services/lockService.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 2844 bytes
from django.core.exceptions import ObjectDoesNotExist
from api.enum.lock_history_enum import Lock_History_Local_Query, Lock_History_Count_Query, Blocker_Header, Waiter_Header, get_lock_query, get_unlock_data
from api.enum.transaction_enum import Local_Transaction_Query
from api.v1.monitor.services.runsqlService import run_batch_sql
from monitor.models import Database
from common.util import execute_return_json, build_exception_from_java

def get_lock_session(pk, time_span=None):
    try:
        database = Database.objects.get(pk=pk)
        db_type = database.db_type
        json_data = {}
        command_list = []
        if time_span == 'realtime':
            query = get_lock_query(database)
            flag, json_data = run_batch_sql(database, query)
            if not flag:
                raise build_exception_from_java(json_data)
            cmd_data = get_unlock_data(database)
            command_list = [x.get('CMD') for x in cmd_data]
        else:
            query_lock = Lock_History_Local_Query[database.db_type].value.format(pk, time_span)
            query_trans = Local_Transaction_Query.format(pk, time_span)
            json_data['lock'] = execute_return_json(query_lock)
            trans = execute_return_json(query_trans)
            if trans:
                json_data['transaction'] = trans[0].get('TRANSACTIONS')
        return {'lock':{'blocker_header':Blocker_Header[database.db_type].value, 
          'waiter_header':Waiter_Header[database.db_type].value, 
          'blocker_id':[
           'B_BLOCKER', 'W_WAITER'], 
          'waiter_id':'W_WAITER', 
          'session_detail_keys':[
           'B_BLOCKER', 'W_WAITER'], 
          'sql_detail_keys':[
           'B_SQL_ID', 'B_PREV_SQL_ID', 'W_SQL_ID', 'W_PREV_SQL_ID'], 
          'data':json_data.get('lock'), 
          'advice':command_list}, 
         'transaction':{'data':json_data.get('transaction'), 
          'sql_detail_keys':[
           'SQL_ID'], 
          'session_detail_keys':[
           'SESSION_ID']}}
    except ObjectDoesNotExist:
        return {'error_message': ''}
    except Exception as err:
        return {'error_message': str(err)}


def get_lock_trend(pk, begin_time=None, end_time=None):
    try:
        database = Database.objects.get(pk=pk)
        query = Lock_History_Count_Query[database.db_type].value.format(pk, begin_time, end_time)
        result = execute_return_json(query)
        data = []
        for x in result:
            data.append([x.get('CREATED_AT'), x.get('BLOCKED_SESSION_COUNT')])

        return data
    except ObjectDoesNotExist:
        return {'error_message': ''}
    except Exception as err:
        return {'error_message': str(err)}
# okay decompiling ./restful/hawkeye/api/v1/monitor/services/lockService.pyc
