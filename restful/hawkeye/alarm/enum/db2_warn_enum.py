# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./alarm/enum/db2_warn_enum.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 4061 bytes
from enum import Enum

class DB2WarnCategory(Enum):
    Connection_Warn = {'description':'DB2 ', 
     'warn_threshold':'100',  'critical_threshold':'200',  'alarm_attr':'value', 
     'alarm_name':'APPLS_CUR_CONS', 
     'message_template':'{warn_level} !! :{message} :{created_at} :{alias}', 
     'link':{'url':'performance', 
      'type':'database',  'json':{}}}
    Blocking_Session_Warn = {'description':'DB2 ', 
     'warn_threshold':'5',  'critical_threshold':'20',  'alarm_attr':'value', 
     'alarm_name':'Blocking_Session_Warn', 
     'message_template':'{warn_level} !! :{message} :{created_at} :{alias}', 
     'link':{'url':'lock', 
      'type':'database',  'json':{}}}
    Database_Access_Warn = {'description':'DB2 ', 
     'warn_threshold':'0', 
     'critical_threshold':'0',  'message_template':'{warn_level} !! :{alias} :{created_at}'}
    Active_Session_Warn = {'description':'DB2 ', 
     'warn_threshold':'50',  'critical_threshold':'100',  'alarm_attr':'value', 
     'alarm_name':'Active_Session_Warn', 
     'message_template':'{warn_level} !! :{message} :{created_at} :{alias}', 
     'link':{'url':'top-activity', 
      'type':'database',  'json':{}}}
    Tablespace_Warn = {'description':'DB2 ', 
     'warn_threshold':'80', 
     'critical_threshold':'90', 
     'optional':{'exclude': []}, 
     'alarm_attr':'used_pct', 
     'alarm_name':'Tablespace_Warn', 
     'message_template':'{warn_level} !! :{name} :{total}(MB) :{used}(MB) {used_pct}% :{created_at} :{alias}', 
     'link':{'url':'space-detail', 
      'type':'database',  'json':{}}}
    Long_Transaction_Warn = {'description':'DB2 ()', 
     'warn_threshold':'60',  'critical_threshold':'300',  'alarm_attr':'value', 
     'alarm_name':'Long_Transaction_Warn', 
     'message_template':'{warn_level} !! :{message}() ID:{SESSION_ID} :{MACHINE} :{TRX_STARTED} :{created_at} :{alias}', 
     'link':{'url':'lock', 
      'type':'database',  'json':{}}}
    Transaction_Warn = {'description':'DB2 ', 
     'warn_threshold':'50',  'critical_threshold':'200',  'alarm_attr':'value', 
     'alarm_name':'Transaction_Warn', 
     'message_template':'{warn_level} !! :{message} :{created_at} :{alias}', 
     'link':{'url':'lock', 
      'type':'database',  'json':{}}}
    Big_Transaction_Warn = {'description':'DB2 ()', 
     'warn_threshold':'1048576',  'critical_threshold':'1048576100',  'alarm_attr':'value', 
     'alarm_name':'Big_Transaction_Warn', 
     'message_template':'{warn_level} !! :{session_id} , :{start_time} :{message} :{created_at} :{alias}', 
     'link':{'url':'lock', 
      'type':'database',  'json':{}}}
# okay decompiling ./restful/hawkeye/alarm/enum/db2_warn_enum.pyc
