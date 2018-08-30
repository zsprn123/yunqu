# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/alarm/services/warnJudgerService.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 3364 bytes
import datetime
from alarm.enum.alarm_warn_enum import WARN_ENUM
from alarm.models import Warn_Config
from common.storages import redis

def alarm_judger(database, alarm_type, alarm_data, data=None):
    if not database:
        print('database is None')
        return
    else:
        string_match = False
        try:
            warn_config = Warn_Config.objects.get(category=alarm_type, database=database)
        except Exception as e:
            print('alarm_type:' + alarm_type)
            print(str(e))
            return (None, None)

        from monitor.models import Space
        if isinstance(alarm_data, Space):
            redis_key = str(database.id) + str(warn_config.id) + alarm_data.name
        else:
            redis_key = str(database.id) + str(warn_config.id)
        alarm_attr = alarm_data and getattr(WARN_ENUM.get(database.db_type), alarm_type).value.get('alarm_attr')
        data = getattr(alarm_data, alarm_attr)
        if data is None:
            return (None, None)
            try:
                data = float(data)
            except ValueError:
                string_match = True

            if warn_config.optional:
                exclude_optional = warn_config.optional.get('exclude', [])
                if hasattr(alarm_data, 'name'):
                    if alarm_data.name in exclude_optional:
                        return (None, None)
                    last_datetime = redis.hmget(redis_key, 'last_send_datetime')[0]
                    if last_datetime != 'None':
                        last_datetime = datetime.datetime.strptime(last_datetime[:19], '%Y-%m-%d %H:%M:%S') if last_datetime is not None else last_datetime
                        key = redis.hmget(redis_key, 'alarm_times')[0]
                        alarm_times = int(key) if key else 0
                        if not warn_config.status:
                            return (None, None)
                        if last_datetime is not None:
                            pass
        if last_datetime != 'None':
            if (datetime.datetime.now() - last_datetime).seconds < int(warn_config.warning_interval):
                return (None, None)
            if alarm_times < int(str(warn_config.pre_warning_times)):
                cache_data = {'last_send_datetime':last_datetime, 
                 'alarm_times':alarm_times + 1}
                redis.hmset(redis_key, cache_data)
                return (None, None)
            if not string_match:
                if data > float(warn_config.critical_threshold):
                    level = ''
                if not string_match:
                    if data > float(warn_config.warn_threshold):
                        level = ''
                    if string_match:
                        if data.upper() == warn_config.critical_threshold:
                            level = ''
                        if string_match:
                            if data.upper() == warn_config.warn_threshold:
                                level = ''
                            level = None
            if level is not None:
                cache_data = {'last_send_datetime':datetime.datetime.now(),  'alarm_times':0}
                redis.hmset(redis_key, cache_data)
            else:
                cache_data = {'last_send_datetime':last_datetime, 
                 'alarm_times':alarm_times}
                redis.hmset(redis_key, cache_data)
        return (level, warn_config)
# okay decompiling ./restful/hawkeye/api/v1/alarm/services/warnJudgerService.pyc
