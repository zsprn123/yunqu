# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./alarm/enum/alarm_warn_enum.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 564 bytes
from enum import Enum
from alarm.enum.db2_warn_enum import DB2WarnCategory
from alarm.enum.host_warn_enum import HostWarnCategory
from alarm.enum.mysql_warn_enum import MySQLWarnCategory
from alarm.enum.oracle_warn_enum import OracleWarnCategory
from alarm.enum.sqlserver_warn_enum import SQLServerWarnCategory
History_Timestamp_GAP_Minute = 60
History_Timestamp_GAP_Hour = 3600
WARN_ENUM = {'oracle':OracleWarnCategory, 
 'mysql':MySQLWarnCategory, 
 'db2':DB2WarnCategory, 
 'sqlserver':SQLServerWarnCategory, 
 'host':HostWarnCategory}
# okay decompiling ./restful/hawkeye/alarm/enum/alarm_warn_enum.pyc
