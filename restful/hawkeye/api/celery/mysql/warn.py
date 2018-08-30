# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/celery/mysql/warn.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 1129 bytes
from monitor.models import Performance
from api.v1.monitor.services.runsqlService import run_sql
from datetime import datetime
from api.v1.alarm.services.warnService import customized_warn_scanner
from alarm.enum.alarm_warn_enum import WARN_ENUM
from common.util import build_exception_from_java

def mysql_standby_warn(database):
    query = 'show slave status'
    flag, json_data = run_sql(database, query)
    if not flag:
        print(str(build_exception_from_java(json_data)))
        return json_data
    created_at = datetime.now().replace(microsecond=0)
    warn = WARN_ENUM.get(database.db_type).Standby_Latency_Warn
    if json_data:
        if json_data[0].get('Seconds_Behind_Master'):
            options = {'master_host':json_data.get('Master_Host'), 
             'master_user':json_data.get('Master_User'), 
             'master_port':json_data.get('Master_Port')}
            p = Performance(inst_id=database.db_name, name=warn.name, value=json_data.get('Seconds_Behind_Master'), created_at=created_at)
            customized_warn_scanner(warn, p, database, False, options)
# okay decompiling ./restful/hawkeye/api/celery/mysql/warn.pyc
