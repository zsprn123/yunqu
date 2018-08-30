# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./alarm/enum/host_warn_enum.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 1537 bytes
from enum import Enum

class HostWarnCategory(Enum):
    Host_CPU_Warn = {'description':'CPU', 
     'warn_threshold':'80',  'critical_threshold':'90',  'alarm_attr':'value', 
     'alarm_name':'HOST CPU', 
     'message_template':'', 
     'optional':{'summary':'{{ $labels.instance }}CPU', 
      'description':'{{ $labels.instance }}CPU{{ $value }}'}, 
     'link':{'url':'host', 
      'type':'performace',  'json':{}}}
    Host_Disk_Warn = {'description':'', 
     'warn_threshold':'80',  'critical_threshold':'90',  'alarm_attr':'value', 
     'alarm_name':'disk', 
     'message_template':'', 
     'optional':{'summary':'{{ $labels.instance }}', 
      'description':'{{ $labels.instance }}{{ $value }}'}, 
     'link':{'url':'host', 
      'type':'performace',  'json':{}}}
    Log_Warn = {'description':'', 
     'warn_threshold':'0',  'critical_threshold':'5',  'alarm_attr':'value', 
     'alarm_name':'disk', 
     'message_template':'', 
     'optional':{'log_config':[],  'summary':'{{ $labels.instance }}',  'description':''},  'link':{'url':'host', 
      'type':'log',  'json':{}}}
# okay decompiling ./restful/hawkeye/alarm/enum/host_warn_enum.pyc
