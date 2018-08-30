# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/monitor/views/database.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 7175 bytes
import requests
from rest_framework import status
from common.aes import aes_decode
from common.util import get_java_response
from monitor.models import type2jdbcurl, Database
from api.enum.database_enum import Driver
from rest_framework.decorators import api_view
from api.v1.monitor.services.runsqlService import run_sql
from rest_framework.response import Response
from api.enum.translate_enum import Column_Header

@api_view(['POST'])
def translate(request):
    return Response(Column_Header, status=status.HTTP_200_OK)


@api_view(['POST'])
def testconn(request):
    need_decode = request.data.get('need_decode', '')
    username = request.data.get('username', '').strip()
    db_name = request.data.get('db_name', '').strip()
    db_type = request.data.get('db_type', '')
    hostname = request.data.get('hostname', '').strip()
    port = request.data.get('port')
    password = request.data.get('password', '').strip()
    if need_decode:
        try:
            password = aes_decode(password)
        except:
            pass

        url = type2jdbcurl(db_type, hostname, port, db_name=db_name)
        jsonobj = {'user':username, 
         'password':password, 
         'jdbc_url':url, 
         'driver':Driver[db_type].value}
        r = get_java_response('test-conn/', jsonobj)
        result = r.json()
    if r.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        return Response(r.json(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif result.get('message') == False:
        return Response({'message': ''}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        (Database.objects.filter(db_name=db_name, db_type=db_type, hostname=hostname, port=port)).update(disabled=False)
        return Response(r.json(), status=r.status_code)


@api_view(['POST'])
def execsql(request):
    database_id = request.data.get('database_id')
    database = Database.objects.get(pk=database_id)
    query = "\n    select COUNTER_NAME,CNTR_VALUE from sys.dm_os_performance_counters where object_name like '%sql statistics%' and counter_name = 'batch requests/sec'\n    union all\n    select COUNTER_NAME,CNTR_VALUE from sys.dm_os_performance_counters where object_name like '%sql statistics%' and counter_name = 'sql compilations/sec'\n    union all\n    select COUNTER_NAME,CNTR_VALUE from sys.dm_os_performance_counters where object_name like '%sql statistics%' and counter_name = 'sql re-compilations/sec'\n    union all\n    select COUNTER_NAME,CNTR_VALUE from sys.dm_os_performance_counters where object_name like '%buffer manager%' and counter_name = 'lazy writes/sec'\n    union all\n    select COUNTER_NAME,CNTR_VALUE from sys.dm_os_performance_counters where object_name like '%buffer manager%' and counter_name = 'page life expectancy'\n    union all\n    select COUNTER_NAME,CNTR_VALUE from sys.dm_os_performance_counters where object_name like '%memory manager%' and counter_name = 'connection memory (kb)'\n    union all\n    select COUNTER_NAME,CNTR_VALUE from sys.dm_os_performance_counters where object_name like '%memory manager%' and counter_name = 'memory grants pending'\n    union all\n    select COUNTER_NAME,CNTR_VALUE from sys.dm_os_performance_counters where object_name like '%memory manager%' and counter_name = 'sql cache memory (kb)'\n    union all\n    select COUNTER_NAME,CNTR_VALUE from sys.dm_os_performance_counters where object_name like '%memory manager%' and counter_name = 'target server memory (kb)'\n    union all\n    select COUNTER_NAME,CNTR_VALUE from sys.dm_os_performance_counters where object_name like '%memory manager%' and counter_name = 'total server memory (kb)'\n    union all\n    select COUNTER_NAME,CNTR_VALUE from sys.dm_os_performance_counters where object_name like '%access methods%' and counter_name = 'full scans/sec'\n    union all\n    select COUNTER_NAME,CNTR_VALUE from sys.dm_os_performance_counters where object_name like '%access methods%' and counter_name = 'forwarded records/sec'\n    union all\n    select COUNTER_NAME,CNTR_VALUE from sys.dm_os_performance_counters where object_name like '%access methods%' and counter_name = 'mixed page allocations/sec'\n    union all\n    select COUNTER_NAME,CNTR_VALUE from sys.dm_os_performance_counters where object_name like '%access methods%' and counter_name = 'page splits/sec'\n    union all\n    select COUNTER_NAME,CNTR_VALUE from sys.dm_os_performance_counters where object_name like '%access methods%' and counter_name = 'table lock escalations/sec'\n    union all\n    select COUNTER_NAME,CNTR_VALUE from sys.dm_os_performance_counters where object_name like '%general statistics%' and counter_name = 'logins/sec'\n    union all\n    select COUNTER_NAME,CNTR_VALUE from sys.dm_os_performance_counters where object_name like '%general statistics%' and counter_name = 'logouts/sec'\n    union all\n    select COUNTER_NAME,CNTR_VALUE from sys.dm_os_performance_counters where object_name like '%general statistics%' and counter_name = 'user connections'\n    union all\n    select COUNTER_NAME,CNTR_VALUE from sys.dm_os_performance_counters where object_name like '%general statistics%' and counter_name = 'processes blocked'\n    union all\n    select COUNTER_NAME,CNTR_VALUE from sys.dm_os_performance_counters where object_name like '%latches%' and counter_name = 'latch waits/sec'\n    union all\n    select COUNTER_NAME,CNTR_VALUE from sys.dm_os_performance_counters where object_name like '%latches%' and counter_name = 'average latch wait time (ms)'\n    union all\n    select COUNTER_NAME,CNTR_VALUE from sys.dm_os_performance_counters where object_name like '%access methods%' and counter_name = 'workfiles created/sec'\n    union all\n    select COUNTER_NAME,CNTR_VALUE from sys.dm_os_performance_counters where object_name like '%access methods%' and counter_name = 'worktables created/sec'\n    union all\n    select COUNTER_NAME,CNTR_VALUE from sys.dm_os_performance_counters where object_name like '%general statistics%' and counter_name = 'active temp tables'\n    union all\n    select COUNTER_NAME,CNTR_VALUE from sys.dm_os_performance_counters where object_name like '%general statistics%' and counter_name = 'temp tables creation rate'\n    union all\n    select COUNTER_NAME,CNTR_VALUE from sys.dm_os_performance_counters where object_name like '%general statistics%' and counter_name = 'temp tables for destruction'\n    union all\n    select COUNTER_NAME,CNTR_VALUE from sys.dm_os_performance_counters where object_name like '%databases%' and counter_name ='active transactions' and instance_name = '_Total\n    union all\n    select COUNTER_NAME,CNTR_VALUE from sys.dm_os_performance_counters where object_name like '%databases%' and counter_name ='log flushes/sec' and instance_name = '_Total'\n    union all\n    select COUNTER_NAME,CNTR_VALUE from sys.dm_os_performance_counters where object_name like '%databases%' and counter_name ='cache hit ratio' and instance_name = '_Total'\n    union all\n    select COUNTER_NAME,CNTR_VALUE from sys.dm_os_performance_counters where object_name like '%SQLServer:Locks%' and counter_name like '%Lock%' and instance_name = '_Total'\n    "
    flag, json_data_1 = run_sql(database, query)
    return Response(json_data_1)
# okay decompiling ./restful/hawkeye/api/v1/monitor/views/database.pyc
