# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/monitor/services/runsqlService.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 7496 bytes
import paramiko
from django.core.exceptions import ObjectDoesNotExist
from api.enum.database_enum import Driver
from api.enum.performance_enum import OraclePerformanceType
from api.models import graph_object_json
from common.aes import aes_decode
from common.util import get_java_response, is_response_error, get_performance_name_id
from monitor.models import type2jdbcurl, Database
import io, logging
logger = logging.getLogger('api')

def run_sql(database, sql_text, db_name=None):
    if database.is_switch_off:
        return (
         False, {'exception':'',  'message':''})
    url = type2jdbcurl(database.db_type, database.hostname, database.port, db_name=database.db_name, encoding=database.get_encoding())
    jsonobj = {'user':database.username, 
     'password':database.get_password(), 
     'jdbc_url':url, 
     'driver':Driver[database.db_type].value, 
     'sql':sql_text, 
     'db_name':db_name}
    r = get_java_response('exec/', jsonobj)
    if is_response_error(r):
        return (False, r.json())
    else:
        return (
         True, r.json())


def run_batch_sql(database, sql_text, db_name=None):
    if database.is_switch_off:
        return (
         False, {'exception':'',  'message':''})
    url = type2jdbcurl(database.db_type, database.hostname, database.port, db_name=database.db_name, encoding=database.get_encoding())
    jsonobj = {'user':database.username, 
     'password':database.get_password(), 
     'jdbc_url':url, 
     'driver':Driver[database.db_type].value, 
     'sql':sql_text, 
     'db_name':db_name}
    r = get_java_response('batch_exec/', jsonobj)
    if is_response_error(r):
        return (False, r.json())
    else:
        return (
         True, r.json())


def run_rule_sql(database, username, password, sql_text, rule_json):
    if database.is_switch_off:
        return (
         False, {'exception':'',  'message':''})
    url = type2jdbcurl(database.db_type, database.hostname, database.port, db_name=database.db_name, encoding=database.get_encoding())
    jsonobj = {'user':username, 
     'password':password, 
     'jdbc_url':url, 
     'driver':Driver[database.db_type].value, 
     'sql_text':sql_text, 
     'sql':rule_json}
    r = get_java_response('batch_rule_exec/', jsonobj)
    if is_response_error(r):
        return (False, r.json())
    else:
        return (
         True, r.json())


def run_plsql(database, sql_text):
    if database.is_switch_off:
        return (
         False, {'exception':'',  'message':''})
    url = type2jdbcurl(database.db_type, database.hostname, database.port, db_name=database.db_name, encoding=database.get_encoding())
    jsonobj = {'user':database.username, 
     'password':database.get_password(), 
     'jdbc_url':url, 
     'driver':Driver[database.db_type].value, 
     'sql':sql_text}
    r = get_java_response('exec_plsql/', jsonobj)
    if is_response_error(r):
        return (False, r.json())
    else:
        return (
         True, r.json())


def get_sql_plan(database, sql_text, schema):
    if database.is_switch_off:
        return (
         False, {'exception':'',  'message':''})
    url = type2jdbcurl(database.db_type, database.hostname, database.port, db_name=database.db_name, encoding=database.get_encoding())
    jsonobj = {'user':database.username, 
     'password':database.get_password(), 
     'jdbc_url':url, 
     'driver':Driver[database.db_type].value, 
     'sql_text':sql_text, 
     'schema':schema, 
     'db_type':database.db_type}
    r = get_java_response('get_sql_plan/', jsonobj)
    if is_response_error(r):
        return (False, r.json())
    else:
        return (
         True, r.json())


def run_sql_with_dict(data, sql_text):
    url = type2jdbcurl(data.get('db_type'), data.get('hostname'), data.get('port'), db_name=data.get('db_name'), encoding=data.get('encoding'))
    jsonobj = {'user':data.get('username'), 
     'password':data.get('password'), 
     'jdbc_url':url, 
     'driver':Driver[data.get('db_type')].value, 
     'sql':sql_text}
    r = get_java_response('exec/', jsonobj)
    if is_response_error(r):
        return (False, r.json())
    else:
        return (
         True, r.json())


def data2result(data, enumType, is_open=True, is_realtime=False):
    """
     enum data
    
    """
    result = []
    for e in enumType:
        json = graph_object_json(str(e), e.name, {})
        for k, v in data.items():
            name_id = get_performance_name_id(k.upper())
            if str(name_id) in e.value.split(','):
                if is_open or is_realtime:
                    json.data[k] = v
                else:
                    json.data[k] = [
                     v]

        result.append(json.__dict__)

    return result


def data2result_oracle(data, enumType, is_open=True, is_realtime=False):
    """
     enum  inst_id data
     CPU 
    
    """
    result = []
    for e in enumType:
        json = graph_object_json(str(e), e.name, {})
        if e == OraclePerformanceType.CPU:
            for k, v in data.items():
                name_id = get_performance_name_id(k.upper())
                if str(name_id) in e.value.split(','):
                    for _k, _v in v.items():
                        if is_open or is_realtime:
                            json.data[_k] = _v
                        else:
                            json.data[_k] = [
                             _v]

        else:
            for k, v in data.items():
                name_id = get_performance_name_id(k.upper())
                if str(name_id) in e.value.split(','):
                    if is_open or is_realtime:
                        json.data[k] = v
                    else:
                        json.data[k] = [
                         v]

        result.append(json.__dict__)

    return result


def data2result_json(data, enumType):
    """
     enum  inst_id data
     {inst_id:data,}
    """
    result = {}
    for e in enumType:
        json = graph_object_json(str(e), e.name, {})
        for k, v in data.items():
            if k.upper() in e.value:
                json.data[k] = v

        result.update(json.__dict__)

    return result


def get_index_data(pk):
    try:
        database = Database.objects.get(pk=pk)
    except ObjectDoesNotExist as e:
        return {'error_message': e}


def run_cmd(host, cmd):
    try:
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(host.hostname, host.port, host.username, aes_decode(host.password))
        stdin, stdout, stderr = s.exec_command(cmd)
        result = stdout.readlines()
        return result
    except paramiko.ssh_exception.SSHException as e:
        logger.error('is not support telnet now!')
    except Exception as e:
        logger.error(str(e))
# okay decompiling ./restful/hawkeye/api/v1/monitor/services/runsqlService.pyc
