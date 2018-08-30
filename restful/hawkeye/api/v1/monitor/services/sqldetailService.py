# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/monitor/services/sqldetailService.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 1778 bytes
from django.core.exceptions import ObjectDoesNotExist
from monitor.models import Database, DB2_ASH, MySQL_ASH
from api.v1.monitor.services.sqldetail.oracleSQLDetail import oracle_sql_detail
from api.v1.monitor.services.sqldetail.generalSQLDetail import get_or_gen_sql_detail
from api.v1.monitor.services.activityService import get_database_activity
import traceback
from api.v1.monitor.services.sqldetail.common import get_sql_text
dimension_json = {'oracle':11, 
 'db2':6, 
 'mysql':5, 
 'sqlserver':7}

def get_sql_detail(pk, sql_id, instance_id=None, time_span=None, begin_time=None, end_time=None, cache=True, activity=True, sql_audit=True):
    try:
        database = Database.objects.get(pk=pk)
        sql_detail = {}
        db_type = database.db_type
        sql_text, schema = get_sql_text(database, sql_id)
        if db_type == 'oracle':
            sql_detail = oracle_sql_detail(pk, sql_id, sql_text, instance_id, time_span, begin_time, end_time, cache, activity, sql_audit=True)
        else:
            sql_detail = get_or_gen_sql_detail(database, sql_id, sql_text, schema)
        return sql_detail
    except ObjectDoesNotExist:
        return {'error_message': ''}
    except Exception as err:
        tb = traceback.format_exc()
        print(tb)
        return {'error_message': str(err)}
# okay decompiling ./restful/hawkeye/api/v1/monitor/services/sqldetailService.pyc
