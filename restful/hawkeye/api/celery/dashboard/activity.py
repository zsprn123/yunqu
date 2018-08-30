# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/celery/dashboard/activity.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 1536 bytes
from alarm.models import Warn_Result
from api.v1.monitor.serializers import DatabaseSerializer
from api.v1.monitor.services.activityService import get_database_activity
from monitor.models import Database
import datetime
from common.util import get_1s_timestamp
Dashboard_RANGE = 600

def update_dashboard_data(database_list):
    if database_list == None:
        return []
    else:
        db_filter_set = database_list
        db_id_set = db_filter_set.values_list('id', flat=True)
        result = []
        warn_result_set = (Warn_Result.objects.filter(database_id__in=db_id_set)).filter(created_at__gte=datetime.datetime.now() - (datetime.timedelta(minutes=10)))
        for db in db_filter_set:
            now_timestamp = get_1s_timestamp()
            activity_data = get_database_activity(str(db.id), begin_time=now_timestamp - Dashboard_RANGE, end_time=now_timestamp)
            top_activity = activity_data.get(db.db_name) or activity_data.get(db.alias)
            if not top_activity:
                continue
            top_activity = top_activity.get('data')
            database_dict = dict(DatabaseSerializer(db).data)
            database_dict.update({'id': str(db.id)})
            database_dict.update({'owner': str(db.owner.id)})
            result.append({'top_activity':top_activity, 
             'database':database_dict, 
             'alarm_count':(warn_result_set.filter(database=db)).count()})

        return result
# okay decompiling ./restful/hawkeye/api/celery/dashboard/activity.pyc
