# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/celery/common/space.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 1625 bytes
from monitor.models import Space, Space_Detail, Performance, Database
from api.enum.space_enum import Space_Query
from api.v1.monitor.services.runsqlService import run_sql
from datetime import datetime
from api.v1.alarm.services.warnService import customized_warn_scanner
from alarm.enum.alarm_warn_enum import WARN_ENUM
from common.util import build_exception_from_java

def get_space(database):
    query = Space_Query.get(database.db_type)
    flag, space_data = run_sql(database, query)
    if not flag:
        print(str(build_exception_from_java(space_data)))
        return
    created_at = datetime.now().replace(microsecond=0)
    space_detail = Space_Detail.objects.update_or_create(database=database, defaults={'detail':space_data, 
     'created_at':created_at})
    for x in space_data:
        space = Space()
        space.database = database
        space.name = x.get('TABLESPACE_NAME')
        space.total_mb = x.get('TOTAL_MB')
        space.free = x.get('FREE')
        space.used = x.get('USED')
        space.type = x.get('CONTENTS')
        space.used_pct = x.get('USED_PCT')
        space.created_at = created_at
        space.save()
        options = {'name':x.get('TABLESPACE_NAME'), 
         'total':x.get('TOTAL_MB'), 
         'used':x.get('USED'), 
         'used_pct':x.get('USED_PCT')}
        if database.db_type not in ('mysql', 'sqlserver'):
            warn = WARN_ENUM.get(database.db_type).Tablespace_Warn
            customized_warn_scanner(warn, space, database, False, options)
# okay decompiling ./restful/hawkeye/api/celery/common/space.pyc
