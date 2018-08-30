# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/db_tasks.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 1827 bytes
import json
from channels import Group
from api.celery.db2.perf_activity import db2_performance, db2_activity
from api.celery.mysql.perf_activity import mysql_performance, mysql_activity
from api.celery.oracle.perf_activity import oracle_performance, oracle_activity
from api.celery.sqlserver.perf_activity import sqlserver_performance
from api.celery.common.lock_history import lock_history
from api.v1.monitor.services.activityService import get_activity_realtime, get_database_activity
from api.v1.monitor.services.performance.performanceService import MysqlPerformance, OraclePerformance, Performance, DB2Performance

def get_performance(database):
    text = {}
    if database.db_type == 'mysql':
        mysql_performance(database)
        text = MysqlPerformance(database).get_history_data()
    else:
        if database.db_type == 'oracle':
            oracle_performance(database)
            text = OraclePerformance(database).get_history_data()
        else:
            if database.db_type == 'sqlserver':
                sqlserver_performance(database)
                text = Performance(database).get_history_data()
            else:
                if database.db_type == 'db2':
                    db2_performance(database)
                    text = DB2Performance(database).get_history_data()
            Group('performance-' + str(database.id)).send({'text': json.dumps(text)}, immediately=True)


def get_activity(database):
    if database.db_type == 'mysql':
        mysql_activity(database)
    else:
        if database.db_type == 'oracle':
            oracle_activity(database)
        else:
            if database.db_type == 'db2':
                db2_activity(database)
        text = get_database_activity(database.id, time_span='realtime')
        Group('activity-' + str(database.id)).send({'text': json.dumps(text)}, immediately=True)


def get_lock_history(database):
    lock_history(database)
# okay decompiling ./restful/hawkeye/api/db_tasks.pyc
