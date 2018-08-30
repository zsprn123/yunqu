# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/alarm/services/warnService.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 7159 bytes
from channels import Group
from alarm.enum.alarm_warn_enum import WARN_ENUM, History_Timestamp_GAP_Hour, History_Timestamp_GAP_Minute
from alarm.models import Warn_Result
import logging
from api.v1.alarm.services.warnJudgerService import alarm_judger
import json
from common.util import send_alarm, get_performance_name
logger = logging.getLogger(__name__)

def general_warn_scanner(instance, database, warn, realtime=True, p_options={}, transaction=False):
    if instance.name in warn.value.get('alarm_name'):
        message_template = warn.value.get('message_template')
        warn_level, warn_config = alarm_judger(database, warn.name, instance)
        if not warn_level:
            return False
        options = {'warn_level':warn_level, 
         'message':instance.value, 
         'created_at':instance.created_at, 
         'alias':database.alias, 
         'inst_id':instance.inst_id}
        if p_options:
            options = {**options, **p_options}
        warn_message = message_template.format(**options)
        link = warn.value.get('link')
        link['database'] = {'id':str(database.id), 
         'alias':database.alias, 
         'db_type':database.db_type, 
         'instance_id_list':database.instance_id_list, 
         'db_name':database.db_name}
        link['json']['instance_id'] = instance.inst_id
        if 'sql_id' in options:
            link['json']['begin_time'] = instance.created_at.timestamp() - History_Timestamp_GAP_Hour
            link['json']['end_time'] = instance.created_at.timestamp() + History_Timestamp_GAP_Hour
        else:
            link['json']['begin_time'] = instance.created_at.timestamp() - History_Timestamp_GAP_Minute
            link['json']['end_time'] = instance.created_at.timestamp() + History_Timestamp_GAP_Minute
        link['json']['time_span'] = instance.created_at.timestamp()
        if p_options:
            link['json'] = {**(link['json']), **p_options}
        if transaction:
            link['json']['transaction'] = True
        warn_result = Warn_Result(database=database, warn_message=warn_message, warn=warn_config, link=link)
        warn_result.save()
        if realtime:
            link['json']['time_span'] = 'realtime'
        warn_alert = {'warn_message':warn_message, 
         'link':link}
        send_alarm(database.id, json.dumps(warn_alert))
        return True


def performance_warn_scanner(**kwargs):
    instance = kwargs.get('instance')
    instance.name = get_performance_name(instance.name_id)
    database = instance.database
    if not database:
        logger.error('database is required in performance instance.')
        return
    if database.db_type == 'oracle':
        db_type = database.db_type
        warn_list = [
         WARN_ENUM.get(db_type).IO_Latency_Warn,
         WARN_ENUM.get(db_type).Parse_Failure_Warn,
         WARN_ENUM.get(db_type).Session_Count_Warn,
         WARN_ENUM.get(db_type).Hard_Parse_Warn,
         WARN_ENUM.get(db_type).Host_CPU_Warn,
         WARN_ENUM.get(db_type).RAC_Interconnect_Warn,
         WARN_ENUM.get(db_type).Standby_Gap_Warn,
         WARN_ENUM.get(db_type).READ_IOPS_Warn,
         WARN_ENUM.get(db_type).WRITE_IOPS_Warn]
        for w in warn_list:
            options = {'name': instance.name}
            if w == WARN_ENUM.get(db_type).Host_CPU_Warn:
                options['name'] = instance.inst_id
            general_warn_scanner(instance, database, w, p_options=options)

    if database.db_type == 'db2':
        db_type = database.db_type
        warn_list = [
         WARN_ENUM.get(db_type).Connection_Warn]
        for w in warn_list:
            options = {'name': instance.name}
            general_warn_scanner(instance, database, w, p_options=options)

    if database.db_type == 'mysql':
        db_type = database.db_type
        warn_list = [
         WARN_ENUM.get(db_type).Connection_Warn]
        for w in warn_list:
            options = {'name': instance.name}
            general_warn_scanner(instance, database, w, p_options=options)

    if database.db_type == 'sqlserver':
        db_type = database.db_type
        warn_list = [
         WARN_ENUM.get(db_type).Connection_Warn]
        for w in warn_list:
            options = {'name': instance.name}
            general_warn_scanner(instance, database, w, p_options=options)

    instance.name = None


def object_warn_scanner(instance, database, warn, realtime=True, p_options={}):
    warn_level, warn_config = alarm_judger(database, warn.name, instance)
    if not warn_level:
        return False
    else:
        alarm_attr = getattr(WARN_ENUM.get(database.db_type), warn.name).value.get('alarm_attr')
        options = {'warn_level':warn_level, 
         'message':getattr(instance, alarm_attr), 
         'created_at':instance.created_at, 
         'alias':database.alias}
        if p_options:
            options = {**options, **p_options}
        message_template = warn.value.get('message_template')
        warn_message = message_template.format(**options)
        link = warn.value.get('link')
        link['database'] = {'id':str(database.id), 
         'alias':database.alias, 
         'db_type':database.db_type, 
         'instance_id_list':database.instance_id_list, 
         'db_name':database.db_name}
        link['json']['instance_id'] = ''
        if 'sql_id' in options:
            link['json']['begin_time'] = instance.created_at.timestamp() - History_Timestamp_GAP_Hour
            link['json']['end_time'] = instance.created_at.timestamp() + History_Timestamp_GAP_Hour
        else:
            link['json']['begin_time'] = instance.created_at.timestamp() - History_Timestamp_GAP_Minute
            link['json']['end_time'] = instance.created_at.timestamp() + History_Timestamp_GAP_Minute
        link['json']['time_span'] = instance.created_at.timestamp()
        if p_options:
            link['json'] = {**(link['json']), **p_options}
        warn_result = Warn_Result(database=database, warn_message=warn_message, warn=warn_config, link=link)
        if realtime:
            link['json']['time_span'] = 'realtime'
        warn_alert = {'warn_message':warn_message, 
         'link':link}
        send_alarm(database.id, json.dumps(warn_alert))
        warn_result.save()
        return True


def customized_warn_scanner(warn, instance, database, realtime, p_option={}, transaction=False):
    from monitor.models import Performance
    if isinstance(instance, Performance):
        return general_warn_scanner(instance, database, warn, realtime, p_option, transaction)
    else:
        return object_warn_scanner(instance, database, warn, realtime, p_option)
# okay decompiling ./restful/hawkeye/api/v1/alarm/services/warnService.pyc
