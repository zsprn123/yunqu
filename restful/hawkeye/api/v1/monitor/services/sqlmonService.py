# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/monitor/services/sqlmonService.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 1131 bytes
from monitor.models import Database
from common.util import build_exception_from_java
from django.core.exceptions import ObjectDoesNotExist
from api.enum.sqlmon_list_enum import SQLMON_QUERY
from api.v1.monitor.services.runsqlService import run_sql
from common.util import execute_return_json

def get_sqlmon_list(pk, time_span=None, begin_time=None, end_time=None):
    try:
        database = Database.objects.get(pk=pk)
        json_data = []
        if time_span == 'realtime':
            query = SQLMON_QUERY.get('realtime')
            flag, json_data = run_sql(database, query)
            if not flag:
                raise build_exception_from_java(json_data)
            else:
                options = {'begin_time':begin_time,  'end_time':end_time, 
                 'pk':pk}
                query = SQLMON_QUERY.get('history').format(**options)
                json_data = execute_return_json(query)
        return json_data
    except ObjectDoesNotExist:
        return {'error_message': ''}
    except Exception as err:
        return {'error_message': str(err)}
# okay decompiling ./restful/hawkeye/api/v1/monitor/services/sqlmonService.pyc
