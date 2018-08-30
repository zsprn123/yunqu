# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./alarm/enum/oracle_warn_enum.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 11611 bytes
from enum import Enum

class OracleWarnCategory(Enum):
    Tablespace_Warn = {'description':'Oracle ', 
     'warn_threshold':'80',  'critical_threshold':'90',  'alarm_attr':'used_pct', 
     'alarm_name':'Tablespace_Warn', 
     'message_template':'{warn_level} !! :{name} :{total}(MB) :{used}(MB) {used_pct}% :{created_at} :{alias}', 
     'link':{'url':'space-detail', 
      'type':'database',  'json':{}}}
    DiskGroup_Offline_Disks_Warn = {'description':'Oracle ASM Offline', 
     'warn_threshold':'1',  'critical_threshold':'2', 
     'alarm_attr':'value', 
     'alarm_name':'DiskGroup_Offline_Disks_Warn', 
     'message_template':'{warn_level} !! :{name} {message}OFFLINE :{created_at} :{alias}', 
     'link':{'url':'space', 
      'type':'database',  'json':{}}}
    DiskGroup_Used_Percent_Warn = {'description':'Oracle ASM', 
     'warn_threshold':'80',  'critical_threshold':'90', 
     'alarm_attr':'value', 
     'alarm_name':'DiskGroup_Used_Percent_Warn', 
     'message_template':'{warn_level} !! :{name} :{total}(GB) :{used}(GB) {used_pct}% :{created_at} :{alias}', 
     'link':{'url':'space', 
      'type':'database',  'json':{}}}
    DiskGroup_Status_Warn = {'description':'Oracle ASM', 
     'warn_threshold':'DISMOUNTED',  'critical_threshold':'BROKEN', 
     'alarm_attr':'value', 
     'alarm_name':'DiskGroup_Status_Warn', 
     'message_template':'{warn_level} !! :{name} :{message} :{created_at} :{alias}', 
     'link':{'url':'space', 
      'type':'database',  'json':{}}}
    Big_Transaction_Warn = {'description':'Oracle (UNDO)', 
     'warn_threshold':'1000',  'critical_threshold':'10000',  'alarm_attr':'value', 
     'alarm_name':'Big_Transaction_Warn', 
     'message_template':'{warn_level} !! :{session_id} , :{start_time} UNDO:{message} :{created_at} :{alias}', 
     'link':{'url':'lock', 
      'type':'database',  'json':{}}}
    Blocking_Session_Warn = {'description':'Oracle ', 
     'warn_threshold':'3',  'critical_threshold':'10',  'alarm_attr':'value', 
     'alarm_name':'Blocking_Session_Warn', 
     'message_template':'{warn_level} !! :{message} :{created_at} :{alias}', 
     'link':{'url':'lock', 
      'type':'database',  'json':{}}}
    IO_Latency_Warn = {'description':'Oracle IO()', 
     'warn_threshold':'50',  'critical_threshold':'100',  'alarm_attr':'value', 
     'alarm_name':'LOG FILE SYNC,LOG FILE PARALLEL WRITE,DB FILE PARALLEL WRITE,DB FILE SEQUENTIAL READ,DB FILE SCATTERED READ,DB FILE SCATTERED READ,DIRECT PATH READ TEMP', 
     'message_template':'{warn_level} !! :{name} :{message} :{created_at} :{alias} :{inst_id}', 
     'link':{'url':'performance', 
      'type':'database',  'json':{}}}
    Parse_Failure_Warn = {'description':'Oracle ', 
     'warn_threshold':'10',  'critical_threshold':'50',  'alarm_attr':'value', 
     'alarm_name':'PARSE FAILURE COUNT PER SEC', 
     'message_template':'{warn_level} !! :{message} :{created_at} :{alias} :{inst_id}', 
     'link':{'url':'performance', 
      'type':'database',  'json':{}}}
    Session_Count_Warn = {'description':'Oracle ', 
     'warn_threshold':'1000',  'critical_threshold':'2000',  'alarm_attr':'value', 
     'alarm_name':'SESSION COUNT', 
     'message_template':'{warn_level} !! :{message} :{created_at} :{alias} :{inst_id}', 
     'link':{'url':'performance', 
      'type':'database',  'json':{}}}
    Hard_Parse_Warn = {'description':'Oracle ', 
     'warn_threshold':'500',  'critical_threshold':'1000',  'alarm_attr':'value', 
     'alarm_name':'HARD PARSE COUNT PER SEC', 
     'message_template':'{warn_level} !! :{message} :{created_at} :{alias} :{inst_id}', 
     'link':{'url':'performance', 
      'type':'database',  'json':{}}}
    Host_CPU_Warn = {'description':'Oracle CPU', 
     'warn_threshold':'80',  'critical_threshold':'90',  'alarm_attr':'value', 
     'alarm_name':'HOST CPU UTILIZATION (%)', 
     'message_template':'{warn_level} !! CPU:{message} :{created_at} :{alias} :{inst_id}', 
     'link':{'url':'performance', 
      'type':'database',  'json':{}}}
    RAC_Interconnect_Warn = {'description':'Oracle ()', 
     'warn_threshold':'10',  'critical_threshold':'20',  'alarm_attr':'value', 
     'alarm_name':'GLOBAL CACHE AVERAGE CR GET TIME,GLOBAL CACHE AVERAGE CURRENT GET TIME', 
     'message_template':'{warn_level} !! RAC:{message} :{created_at} :{alias} :{inst_id}', 
     'link':{'url':'performance', 
      'type':'database',  'json':{}}}
    Standby_Gap_Warn = {'description':'Oracle ()', 
     'warn_threshold':'120',  'critical_threshold':'300',  'alarm_attr':'value', 
     'alarm_name':'APPLY LAG,TRANSPORT LAG', 
     'message_template':'{warn_level} !! :{name} :{message}() :{created_at} :{alias} :{inst_id}', 
     'link':{'url':'performance', 
      'type':'database',  'json':{}}}
    Active_Session_Warn = {'description':'Oracle ', 
     'warn_threshold':'100',  'critical_threshold':'200',  'alarm_attr':'value', 
     'alarm_name':'Active_Session_Warn', 
     'message_template':'{warn_level} !! :{message} :{created_at} :{alias}', 
     'link':{'url':'top-activity', 
      'type':'database',  'json':{}}}
    Transaction_Warn = {'description':'Oracle ', 
     'warn_threshold':'50',  'critical_threshold':'200',  'alarm_attr':'value', 
     'alarm_name':'Transaction_Warn', 
     'message_template':'{warn_level} !! :{message} :{created_at} :{alias}', 
     'link':{'url':'lock', 
      'type':'database',  'json':{}}}
    Plan_Change_Warn = {'description':'Oracle SQL', 
     'warn_threshold':'100',  'critical_threshold':'100000',  'alarm_attr':'value', 
     'alarm_name':'Plan_Change_Warn', 
     'message_template':'{warn_level} !! sql_id:{sql_id}  :{message} :{created_at} :{alias}', 
     'link':{'url':'sql-detail', 
      'type':'database',  'json':{}}}
    Job_Warn = {'description':'Oracle Job ', 
     'warn_threshold':'2',  'critical_threshold':'10',  'alarm_attr':'value', 
     'alarm_name':'Job_Warn', 
     'message_template':'{warn_level} !! job:{name} :{message} :{created_at} :{alias}', 
     'link':{'url':'schema', 
      'type':'database',  'json':{}}}
    DB_Object_Change_Warn = {'description':'Oracle ', 
     'warn_threshold':'0',  'critical_threshold':'0',  'alarm_attr':'value', 
     'alarm_name':'DB_Object_Change_Warn', 
     'message_template':'{warn_level} !! :{schema}.{object_name} DDL:{last_ddl_time} :{created_at} :{alias}', 
     'link':{'url':'schema', 
      'type':'database',  'json':{}}}
    Database_Access_Warn = {'description':'Oracle ', 
     'warn_threshold':'0', 
     'critical_threshold':'0',  'message_template':'{warn_level} !! :{alias}  :{created_at}'}
    Long_Transaction_Warn = {'description':'Oracle ()', 
     'warn_threshold':'60',  'critical_threshold':'300',  'alarm_attr':'value', 
     'alarm_name':'Long_Transaction_Warn', 
     'message_template':'{warn_level} !! :{message}() ID:{SESSION_ID} :{MACHINE} :{TRX_STARTED} :{created_at} :{alias}', 
     'link':{'url':'lock', 
      'type':'database',  'json':{}}}
    READ_IOPS_Warn = {'description':'Oracle IOPS', 
     'warn_threshold':'10000',  'critical_threshold':'20000',  'alarm_attr':'value', 
     'alarm_name':'PHYSICAL READ IO REQUESTS PER SEC', 
     'message_template':'{warn_level} !! IOPS:{message} :{created_at} :{alias} :{inst_id}', 
     'link':{'url':'performance', 
      'type':'database',  'json':{}}}
    WRITE_IOPS_Warn = {'description':'Oracle IOPS', 
     'warn_threshold':'5000',  'critical_threshold':'10000',  'alarm_attr':'value', 
     'alarm_name':'PHYSICAL WRITE IO REQUESTS PER SEC', 
     'message_template':'{warn_level} !! IOPS:{message} :{created_at} :{alias} :{inst_id}', 
     'link':{'url':'performance', 
      'type':'database',  'json':{}}}
# okay decompiling ./restful/hawkeye/alarm/enum/oracle_warn_enum.pyc
