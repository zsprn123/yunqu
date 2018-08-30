# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./alarm/enum/mysql_warn_enum.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 4448 bytes
from enum import Enum

class MySQLWarnCategory(Enum):
    Standby_Latency_Warn = {'description':'Mysql ()', 
     'warn_threshold':'60',  'critical_threshold':'300',  'alarm_attr':'value', 
     'alarm_name':'Standby_Latency_Warn', 
     'message_template':'{warn_level} !! :{message}() (:{master_host} :{master_port} :{master_user}) :{created_at} :{alias}', 
     'link':{'url':'performance', 
      'type':'database',  'json':{}}}
    Connection_Warn = {'description':'Mysql ', 
     'warn_threshold':'100',  'critical_threshold':'200',  'alarm_attr':'value', 
     'alarm_name':'Thread_connected', 
     'message_template':'{warn_level} !! :{message} :{created_at} :{alias}', 
     'link':{'url':'performance', 
      'type':'database',  'json':{}}}
    Locked_Table_Warn = {'description':'Mysql ', 
     'warn_threshold':'0',  'critical_threshold':'5',  'alarm_attr':'value', 
     'alarm_name':'Locked_Table_Warn', 
     'message_template':'{warn_level} !! :{message} :{table_list} :{created_at} :{alias}', 
     'link':{'url':'lock', 
      'type':'database',  'json':{}}}
    Blocking_Session_Warn = {'description':'Mysql ', 
     'warn_threshold':'5',  'critical_threshold':'20',  'alarm_attr':'value', 
     'alarm_name':'Blocking_Session_Warn', 
     'message_template':'{warn_level} !! :{message} :{created_at} :{alias}', 
     'link':{'url':'lock', 
      'type':'database',  'json':{}}}
    Database_Access_Warn = {'description':'Mysql ', 
     'warn_threshold':'0', 
     'critical_threshold':'0',  'message_template':'{warn_level} !! :{alias} :{created_at}'}
    Active_Session_Warn = {'description':'Mysql ', 
     'warn_threshold':'20',  'critical_threshold':'100',  'alarm_attr':'value', 
     'alarm_name':'Active_Session_Warn', 
     'message_template':'{warn_level} !! :{message} :{created_at} :{alias}', 
     'link':{'url':'top-activity', 
      'type':'database',  'json':{}}}
    Long_Transaction_Warn = {'description':'Mysql ()', 
     'warn_threshold':'60',  'critical_threshold':'300',  'alarm_attr':'value', 
     'alarm_name':'Long_Transaction_Warn', 
     'message_template':'{warn_level} !! :{message}() ID:{SESSION_ID} :{MACHINE} :{TRX_STARTED} :{created_at} :{alias}', 
     'link':{'url':'lock', 
      'type':'database',  'json':{}}}
    Transaction_Warn = {'description':'Mysql ', 
     'warn_threshold':'50',  'critical_threshold':'200',  'alarm_attr':'value', 
     'alarm_name':'Transaction_Warn', 
     'message_template':'{warn_level} !! :{message} :{created_at} :{alias}', 
     'link':{'url':'lock', 
      'type':'database',  'json':{}}}
    Big_Transaction_Warn = {'description':'Mysql ()', 
     'warn_threshold':'1000',  'critical_threshold':'10000',  'alarm_attr':'value', 
     'alarm_name':'Big_Transaction_Warn', 
     'message_template':'{warn_level} !! ID:{session_id} , :{start_time} :{message} :{created_at} :{alias}', 
     'link':{'url':'lock', 
      'type':'database',  'json':{}}}
# okay decompiling ./restful/hawkeye/alarm/enum/mysql_warn_enum.pyc
