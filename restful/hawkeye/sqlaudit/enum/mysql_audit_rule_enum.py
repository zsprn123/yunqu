# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./sqlaudit/enum/mysql_audit_rule_enum.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 20266 bytes
from enum import Enum

class MySQLSqlRuleEnum(Enum):
    rule1 = {'audit_type':'', 
     'target':'',  'name':'',  'risky':'',  'single':True,  'description':'', 
     'modifiable':False,  'template':'NO_INDEX', 
     'predicate':'90'}
# okay decompiling ./restful/hawkeye/sqlaudit/enum/mysql_audit_rule_enum.pyc
