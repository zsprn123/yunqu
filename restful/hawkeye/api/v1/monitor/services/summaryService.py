# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/monitor/services/summaryService.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 1108 bytes
from django.core.exceptions import ObjectDoesNotExist
import json
from api.v1.monitor.services.summary.OracleSummary import get_oracle_summary
from api.v1.monitor.services.summary.DB2Summary import get_db2_summary
from api.v1.monitor.services.summary.mysqlSummary import get_mysql_summary
from api.v1.monitor.services.summary.sqlserverSummary import get_sqlserver_summary
from monitor.models import Database

def get_summary(pk, time_span=None, begin_time=None, end_time=None):
    try:
        database = Database.objects.get(pk=pk)
        db_type = database.db_type
        if db_type == 'oracle':
            return get_oracle_summary(pk)
        if db_type == 'db2':
            return get_db2_summary(pk)
        if db_type == 'mysql':
            return get_mysql_summary(pk)
        if db_type == 'sqlserver':
            return get_sqlserver_summary(pk)
    except ObjectDoesNotExist:
        return {'error_message': ''}
    except Exception as err:
        return {'error_message': str(err)}
# okay decompiling ./restful/hawkeye/api/v1/monitor/services/summaryService.pyc
