# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./sqlaudit/enum/db2_audit_rule_enum.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 19749 bytes
from enum import Enum

class DB2SqlRuleEnum(Enum):
    rule1 = {'audit_type':'SQL', 
     'target':'',  'name':'',  'risky':'',  'single':True,  'description':', , 10000', 
     'modifiable':True,  'template':'FULL_SCAN', 
     'predicate':'10000'}
    rule2 = {'audit_type':'SQL', 
     'target':'',  'name':'',  'risky':'',  'single':True,  'description':', 1000', 
     'modifiable':True,  'template':'INDEX_ROWS', 
     'predicate':'1000'}
    rule21 = {'audit_type':'', 
     'target':'',  'name':'',  'risky':'',  'single':True,  'description':'', 
     'modifiable':True,  'template':'TABLE_OLD_STATS', 
     'predicate':'90'}
    rule22 = {'audit_type':'',  'target':'',  'name':'',  'risky':'',  'single':True,  'description':'', 
     'modifiable':True,  'template':'INDEX_OLD_STATS', 
     'predicate':'90'}
    rule23 = {'audit_type':'', 
     'target':'',  'name':'',  'risky':'',  'single':True,  'description':'', 
     'modifiable':False,  'template':'INDEX_MISSING_STATS', 
     'predicate':'7'}
    rule24 = {'audit_type':'', 
     'target':'',  'name':'',  'risky':'',  'single':True,  'description':'', 
     'modifiable':False,  'template':'TABLE_MISSING_STATS', 
     'predicate':'7'}
    rule25 = {'audit_type':'', 
     'target':'',  'name':'(NPAGES > 0), (card = 0)',  'risky':'',  'single':True,  'description':', , 1280(10MB)', 
     'modifiable':True,  'template':'TABLE_INCONSISTENT_STATS', 
     'predicate':'1280'}
    rule26 = {'audit_type':'', 
     'target':'',  'name':'(NPAGES = 0, card = 0)',  'risky':'',  'single':True,  'description':', ', 
     'modifiable':False,  'template':'TABLE_EMPTY_STATS', 
     'predicate':'1280'}
    rule27 = {'audit_type':'', 
     'target':'',  'name':'',  'risky':'',  'single':True,  'description':', 10000', 
     'modifiable':True,  'template':'INDEX_EMPTY_LEAFS', 
     'predicate':'10000'}
    rule28 = {'audit_type':'', 
     'target':'',  'name':'',  'risky':'',  'single':True,  'description':', 10000', 
     'modifiable':True,  'template':'INDEX_RIDS_DELETED', 
     'predicate':'10000'}
    rule29 = {'audit_type':'', 
     'target':'',  'name':'',  'risky':'',  'single':True,  'description':'NLEVELS, 3', 
     'modifiable':True,  'template':'INDEX_NLEVELS', 
     'predicate':'3'}
    rule30 = {'audit_type':'', 
     'target':'',  'name':'',  'risky':'',  'single':True,  'description':', , , 10000', 
     'modifiable':False,  'template':'TABLE_EMPTY_PAGES', 
     'predicate':'10000'}
    rule31 = {'audit_type':'', 
     'target':'',  'name':'',  'risky':'',  'single':True,  'description':', , 5', 
     'modifiable':True,  'template':'INDEX_COLUMNS', 
     'predicate':'5'}
    rule32 = {'audit_type':'', 
     'target':'',  'name':'',  'risky':'',  'single':True,  'description':', update/delete, , DML', 
     'modifiable':False,  'template':'UNINDEXED_FK', 
     'predicate':'1'}
    rule33 = {'audit_type':'', 
     'target':'',  'name':'',  'risky':'',  'single':True,  'description':', ', 
     'modifiable':False,  'template':'REDUNDANT_INDEX', 
     'predicate':'1'}
    rule34 = {'audit_type':'', 
     'target':'',  'name':'',  'risky':'',  'single':True,  'description':', , 8', 
     'modifiable':True,  'template':'SINGLE_TABLE_INDEXES', 
     'predicate':'8'}
    rule74 = {'audit_type':'SQL', 
     'target':'SQL',  'name':'',  'risky':'',  'single':True,  'description':", Like '%ABC', ", 
     'modifiable':False,  'template':'LEFT_WILDCARD', 
     'predicate':'1'}
    rule75 = {'audit_type':'SQL', 
     'target':'SQL',  'name':'Insert ',  'risky':'',  'single':True,  'description':'Insert into t values(...), ', 
     'modifiable':False,  'template':'INSERT_VALUE', 
     'predicate':'1'}
    rule67 = {'audit_type':'SQL', 
     'target':'SQL',  'name':'SELECT *',  'risky':'',  'single':True,  'description':', ', 
     'modifiable':False,  'template':'SELECT_STAR', 
     'predicate':'1'}
    rule68 = {'audit_type':'SQL', 
     'target':'SQL',  'name':'SQL',  'risky':'',  'single':False,  'description':'SQL', 
     'modifiable':False,  'template':'ERROR_STATMENT', 
     'predicate':'10'}
# okay decompiling ./restful/hawkeye/sqlaudit/enum/db2_audit_rule_enum.pyc
