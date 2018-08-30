# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./sqlaudit/enum/static_oracle_audit_rule_enum.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 16988 bytes
from enum import Enum

class StaticOracleRuleEnum(Enum):
    rule1 = {'audit_type':'CREATE', 
     'target':'SEQUENCE',  'name':'',  'risky':'',  'is_static_rule':True,  'description':', , , Library Cache, DFS LOCK HANDLE, 100', 
     'modifiable':True,  'template':'SEQUENCE_CACHE', 
     'predicate':'100'}
    rule2 = {'audit_type':'CREATE', 
     'target':'SEQUENCE',  'name':' ORDER ',  'risky':'',  'is_static_rule':True,  'description':' ORDER , RAC', 
     'modifiable':False,  'template':'SEQUENCE_ORDER', 
     'predicate':'100'}
    rule3 = {'audit_type':'CREATE', 
     'target':'SEQUENCE',  'name':'1',  'risky':'',  'is_static_rule':True,  'description':', 1', 
     'modifiable':True,  'template':'SEQUENCE_INCREMENT_BY', 
     'predicate':'1'}
    rule4 = {'audit_type':'CREATE', 
     'target':'SEQUENCE',  'name':' SEQ_ ',  'risky':'',  'is_static_rule':True,  'description':'', 
     'modifiable':True,  'template':'SEQUENCE_NAMING', 
     'predicate':'SEQ_'}
    rule5 = {'audit_type':'CREATE', 
     'target':'TABLE',  'name':', LONG, RAW, LONG RAW',  'risky':'',  'is_static_rule':True,  'description':', LONG, RAW, LONG RAW', 
     'modifiable':False,  'template':'HAS_RAW', 
     'predicate':'1'}
    rule6 = {'audit_type':'CREATE', 
     'target':'TABLE',  'name':'Lob  BASEFILE ',  'risky':'',  'is_static_rule':True,  'description':'Lob  BASEFILE ', 
     'modifiable':False,  'template':'BASEFILE_LOB', 
     'predicate':'1'}
    rule7 = {'audit_type':'CREATE', 
     'target':'INDEX',  'name':'',  'risky':'',  'is_static_rule':True,  'description':'', 
     'modifiable':False,  'template':'INDEX_TABLESPACE', 
     'predicate':'1'}
    rule8 = {'audit_type':'CREATE', 
     'target':'TABLE',  'name':'',  'risky':'',  'is_static_rule':True,  'description':'', 
     'modifiable':False,  'template':'TABLE_TABLESPACE', 
     'predicate':'1'}
    rule9 = {'audit_type':'CREATE', 
     'target':'INDEX',  'name':' IDX_ ',  'risky':'',  'is_static_rule':True,  'description':'', 
     'modifiable':True,  'template':'INDEX_NAMING', 
     'predicate':'IDX_'}
    rule10 = {'audit_type':'CREATE', 
     'target':'INDEX',  'name':'',  'risky':'',  'is_static_rule':True,  'description':'', 
     'modifiable':False,  'template':'CREATE_INDEX_PARALLEL', 
     'predicate':'1'}
    rule11 = {'audit_type':'CREATE', 
     'target':'INDEX',  'name':' Online',  'risky':'',  'is_static_rule':True,  'description':' Online', 
     'modifiable':False,  'template':'CREATE_INDEX_ONLINE', 
     'predicate':'1'}
    rule12 = {'audit_type':'CREATE', 
     'target':'INDEX',  'name':'',  'risky':'',  'is_static_rule':True,  'description':', , 5', 
     'modifiable':True,  'template':'INDEX_COLUMNS', 
     'predicate':'5'}
    rule13 = {'audit_type':'CREATE', 
     'target':'INDEX',  'name':'',  'risky':'',  'is_static_rule':True,  'description':'', 
     'modifiable':False,  'template':'REDUNDANT_INDEX', 
     'predicate':'1'}
    rule14 = {'audit_type':'CREATE', 
     'target':'TABLE,INDEX,SEQUENCE,FUNCTION,PACKAGE,PROCEDURE,SYNONYM',  'name':'$', 
     'risky':'',  'is_static_rule':True,  'description':'$', 
     'modifiable':False,  'template':'OBJECT_NAMING', 
     'predicate':'1'}
    rule15 = {'audit_type':'CREATE', 
     'target':'TRIGGER,DATABASE,PUBLIC',  'name':',DB_LINK,Public ', 
     'risky':'',  'is_static_rule':True,  'description':',DB_LINK,Public ', 
     'modifiable':False,  'template':'WRONG_OBJECT', 
     'predicate':'1'}
    rule16 = {'audit_type':'ALTER', 
     'target':'TABLE',  'name':' Update Index',  'risky':'',  'is_static_rule':True,  'description':' Update Index', 
     'modifiable':False,  'template':'PARTITION_INDEX', 
     'predicate':'1'}
    rule18 = {'audit_type':'DROP', 
     'target':'TABLE',  'name':'',  'risky':'',  'is_static_rule':True,  'description':'', 
     'modifiable':False,  'template':'DROP_OBJECT', 
     'predicate':'1'}
    rule19 = {'audit_type':'TRUNCATE', 
     'target':'TABLE',  'name':'Truncate ',  'risky':'',  'is_static_rule':True,  'description':'Truncate ', 
     'modifiable':False,  'template':'TRUNCATE', 
     'predicate':'1'}
    rule20 = {'audit_type':'ALTER', 
     'target':'INDEX',  'name':'',  'risky':'',  'is_static_rule':True,  'description':'', 
     'modifiable':False,  'template':'ALTER_INDEX_PARALLEL', 
     'predicate':'1'}
    rule21 = {'audit_type':' ALTER', 
     'target':'INDEX',  'name':' Online',  'risky':'',  'is_static_rule':True,  'description':' Online', 
     'modifiable':False,  'template':'ALTER_INDEX_ONLINE', 
     'predicate':'1'}
    rule23 = {'audit_type':'SQL', 
     'target':'',  'name':'',  'risky':'',  'is_static_rule':True,  'description':', , 10', 
     'modifiable':True,  'template':'BAD_PLAN', 
     'predicate':'100', 
     'predicate_template':"(operation = 'TABLE ACCESS' and options in ('FULL','STORAGE FULL')) and cost > {}"}
    rule24 = {'audit_type':'SQL', 
     'target':'',  'name':'',  'risky':'',  'is_static_rule':True,  'description':', , 10', 
     'modifiable':True,  'template':'BAD_PLAN', 
     'predicate':'100', 
     'predicate_template':"(operation = 'INDEX' and options = 'FULL SCAN') and cost > {}"}
    rule25 = {'audit_type':'SQL', 
     'target':'',  'name':'',  'risky':'',  'description':',  SQL ', 
     'modifiable':False,  'is_static_rule':True,  'template':'BAD_PLAN', 
     'predicate':"(operation = 'MERGE JOIN' and options = 'CARTESIAN')"}
    rule26 = {'audit_type':'SQL', 
     'target':'',  'name':'',  'risky':'',  'is_static_rule':True,  'description':', , 10', 
     'modifiable':True,  'template':'BAD_PLAN', 
     'predicate':'100', 
     'predicate_template':"(operation = 'INDEX' and options = 'SKIP SCAN') and cost > {}"}
    rule27 = {'audit_type':'SQL', 
     'target':'',  'name':'',  'risky':'',  'is_static_rule':True,  'description':', , 10', 
     'modifiable':True,  'template':'BAD_PLAN', 
     'predicate':'100', 
     'predicate_template':"(operation = 'INDEX' and options = 'FAST FULL SCAN') and cost > {}"}
    rule28 = {'audit_type':'SQL', 
     'target':'',  'name':'',  'risky':'',  'is_static_rule':True,  'description':', ', 
     'modifiable':False,  'template':'BAD_PLAN', 
     'predicate':"(operation = 'PARTITION RANGE' and options = 'ALL')"}
    rule29 = {'audit_type':'SQL', 
     'target':'',  'name':': (INTERNAL_FUNCTION)',  'risky':'',  'is_static_rule':True,  'description':', DATETIMESTAMP, ', 
     'modifiable':False,  'template':'TYPE_CONVERSION', 
     'predicate':'(REGEXP_LIKE(filter_predicates, \'INTERNAL_FUNCTION\\("[^"]+"\\)\') and not REGEXP_LIKE(filter_predicates, \'(AND|OR) INTERNAL_FUNCTION\\("[^"]+"\\)\') and not REGEXP_LIKE(filter_predicates, \'INTERNAL_FUNCTION\\("[^"]+"\\) (AND|OR)\'))'}
    rule30 = {'audit_type':'SQL', 
     'target':'',  'name':'',  'risky':'',  'is_static_rule':True,  'description':', (AND,OR), ', 
     'modifiable':False,  'template':'TYPE_CONVERSION', 
     'predicate':'(REGEXP_LIKE(filter_predicates, \'(AND|OR) INTERNAL_FUNCTION\\("[^"]+"\\)\') or REGEXP_LIKE(filter_predicates, \'INTERNAL_FUNCTION\\("[^"]+"\\) (AND|OR)\'))'}
    rule31 = {'audit_type':'SQL', 
     'target':'',  'name':'',  'risky':'',  'description':', , , ', 
     'modifiable':False,  'is_static_rule':True,  'template':'TYPE_CONVERSION', 
     'predicate':'(REGEXP_LIKE(filter_predicates, \'\\("[^"]+"\\)\') and not REGEXP_LIKE(filter_predicates, \'INTERNAL_FUNCTION\\("[^"]+"\\)\')) and (operation = \'INDEX\' or operation like \'%TABLE%\')'}
    rule32 = {'audit_type':'SQL', 
     'target':'SQL',  'name':'',  'risky':'',  'is_static_rule':True,  'description':', , , SQL ', 
     'modifiable':False,  'template':'OVER_BIND_VARIABLE', 
     'predicate':'1'}
    rule42 = {'audit_type':'SQL', 
     'target':'SQL',  'name':'',  'risky':'',  'is_static_rule':True,  'description':", Like '%ABC', ", 
     'modifiable':False,  'template':'LEFT_WILDCARD', 
     'predicate':'1'}
    rule43 = {'audit_type':'SQL', 
     'target':'SQL',  'name':'Insert ',  'risky':'',  'single':False,  'is_static_rule':True, 
     'description':'Insert into t values(...), ', 
     'modifiable':False,  'template':'INSERT_VALUE', 
     'predicate':'1'}
    rule44 = {'audit_type':'SQL', 
     'target':'SQL',  'name':'In',  'risky':'',  'is_static_rule':True,  'description':'IN,,  join .  SQL .  In , 20', 
     'modifiable':True, 
     'template':'MANY_BINDS', 
     'predicate':'20'}
    rule45 = {'audit_type':'SQL',  'target':'SQL',  'name':'SQL  Hint',  'risky':'',  'single':False,  'is_static_rule':True,  'description':'SQL  Hint,  Hint , ', 
     'modifiable':False,  'template':'WITH_HINT', 
     'predicate':'1'}
    rule33 = {'audit_type':'SQL', 
     'target':'',  'name':'Update  Where ',  'risky':'',  'is_static_rule':True,  'description':'Update  Where , , ,undo,, , :10', 
     'modifiable':True,  'template':'UPDATE_WHERE', 
     'predicate':'10'}
    rule34 = {'audit_type':'SQL', 
     'target':'',  'name':'Delete  Where ',  'risky':'',  'is_static_rule':True,  'description':'Delete  Where , , ,undo,,  Truncate , , :10', 
     'modifiable':True,  'template':'DELETE_WHERE', 
     'predicate':'10'}
    rule35 = {'audit_type':'SQL', 
     'target':'',  'name':'Select  Where ',  'risky':'',  'is_static_rule':True,  'description':'Select  Where , , , :10', 
     'modifiable':True,  'template':'SELECT_WHERE', 
     'predicate':'10'}
    rule36 = {'audit_type':'SQL', 
     'target':'',  'name':' FILTER ',  'risky':'',  'is_static_rule':True,  'description':'Rownum, Group By, FILTER', 
     'modifiable':False,  'template':'PLAN_FILTER', 
     'predicate':'10'}
    rule37 = {'audit_type':'SQL', 
     'target':'',  'name':'',  'risky':'',  'is_static_rule':True,  'description':',  CPU, IO ,  OLTP ', 
     'modifiable':False,  'template':'PARALLEL_PLAN', 
     'predicate':'10'}
    rule38 = {'audit_type':'SQL', 
     'target':'SQL',  'name':'SELECT *',  'risky':'',  'single':False,  'is_static_rule':True,  'description':', ', 
     'modifiable':False,  'template':'SELECT_STAR', 
     'predicate':'1'}
    rule39 = {'audit_type':'SQL', 
     'target':'SQL',  'name':'SQL  Hint',  'risky':'',  'single':False,  'is_static_rule':True,  'description':'SQL  Hint,  Hint , ', 
     'modifiable':False,  'template':'WITH_HINT', 
     'predicate':'1'}
    rule40 = {'audit_type':'SQL', 
     'target':'',  'name':'SQL',  'risky':'',  'single':False,  'is_static_rule':True,  'description':'SQL, , , :5', 
     'modifiable':True,  'template':'NESTED_BLOCK', 
     'predicate':'5'}
    rule41 = {'audit_type':'SQL', 
     'target':'',  'name':'SQL',  'risky':'',  'single':False,  'is_static_rule':True,  'description':'BI, OLTP ,, SQL, :5', 
     'modifiable':True,  'template':'MANY_TABLE', 
     'predicate':'5'}
    rule46 = {'audit_type':'SQL', 
     'target':'',  'name':'Select ... For Update',  'risky':'',  'is_static_rule':True,  'description':', , ', 
     'modifiable':False,  'template':'FOR_UPDATE', 
     'predicate':'10'}
    rule47 = {'audit_type':'SQL', 
     'target':'SQL',  'name':'SQL',  'risky':'',  'is_static_rule':True,  'description':'SQL', 
     'modifiable':False,  'template':'ERROR_STATMENT', 
     'predicate':'10'}
# okay decompiling ./restful/hawkeye/sqlaudit/enum/static_oracle_audit_rule_enum.pyc
