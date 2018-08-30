# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/monitor/services/summary/mysqlSummary.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 1830 bytes
import json
from api.celery.common.space import get_space
from api.enum.space_enum import Space_Total_Query, reprocess_query
from api.enum.summary_enum import SummaryQuery
from api.v1.monitor.services.runsqlService import run_batch_sql
from common.storages import redis
from common.util import build_exception_from_java, execute_return_json
from monitor.models import Database

def get_mysql_summary(pk):
    conn = Database.objects.get(pk=pk)
    db_type = conn.db_type
    query = reprocess_query(Space_Total_Query, {'pk': pk})
    total_space = execute_return_json(query)
    if not total_space:
        get_space(conn)
        total_space = execute_return_json(query)
    query = SummaryQuery.get(db_type)
    flag, json_data = run_batch_sql(conn, query)
    if not flag:
        raise build_exception_from_java(json_data)
    database_json = {x.get('Variable_name'):x.get('Value') for x in json_data.get('database') if x.get('Variable_name') in ('version',
                                                                                                                            'version_comment',
                                                                                                                            'version_compile_machine',
                                                                                                                            'version_compile_os',
                                                                                                                            'default_storage_engine',
                                                                                                                            'general_log',
                                                                                                                            'log_bin',
                                                                                                                            'slow_query_log')}
    memory_json = {x.get('Variable_name'):x.get('Value') for x in json_data.get('database') if x.get('Variable_name') in ('innodb_buffer_pool_size',
                                                                                                                          'join_buffer_size',
                                                                                                                          'key_buffer_size',
                                                                                                                          'query_cache_size',
                                                                                                                          'sort_buffer_size',
                                                                                                                          'thread_cache_size')}
    summary_data = {'space':total_space, 
     'database':database_json, 
     'memory':memory_json}
    return summary_data
# okay decompiling ./restful/hawkeye/api/v1/monitor/services/summary/mysqlSummary.pyc
