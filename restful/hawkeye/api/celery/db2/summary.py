# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/celery/db2/summary.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 768 bytes
from api.v1.monitor.services.runsqlService import run_sql
from monitor.models import DB2_Summary, Database
from datetime import datetime
from common.storages import redis
from celery import shared_task

@shared_task()
def get_dbsummary(pk):
    database = Database.objects.get(pk=pk)
    query = 'call monreport.dbsummary(10)'
    flag, json_data = run_sql(database, query)
    created_at = datetime.now().replace(microsecond=0)
    if flag:
        text = ('\n').join([x.get('TEXT') for x in json_data])
        dbs = DB2_Summary()
        dbs.database = database
        dbs.summary = text
        dbs.created_at = created_at
        dbs.save()
        key = ('dbsummary:{}').format(str(database.id))
        redis.set(key, text)
    else:
        print(json_data)
# okay decompiling ./restful/hawkeye/api/celery/db2/summary.pyc
