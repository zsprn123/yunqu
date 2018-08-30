# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./sqlaudit/enum/oracle_audit_rule_enum.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 27963 bytes
from enum import Enum

class OracleSqlRuleEnum(Enum):
    rule1 = {'audit_type':'SQL', 
     'target':'',  'name':'',  'risky':'',  'description':', , 10', 
     'modifiable':True,  'template':'MULTI_PLAN', 
     'predicate':'10'}
    rule2 = {'audit_type':'SQL',  'target':'',  'name':'',  'risky':'',  'description':', , 10', 
     'modifiable':True,  'template':'BAD_PLAN', 
     'predicate':'100', 
     'predicate_template':"(operation = 'TABLE ACCESS' and options in ('FULL','STORAGE FULL')) and cost > {}"}
    rule3 = {'audit_type':'SQL', 
     'target':'',  'name':'',  'risky':'',  'description':', , 10', 
     'modifiable':True,  'template':'BAD_PLAN', 
     'predicate':'100', 
     'predicate_template':"(operation = 'INDEX' and options = 'FULL SCAN') and cost > {}"}
    rule4 = {'audit_type':'SQL', 
     'target':'',  'name':'',  'risky':'',  'description':',  SQL ', 
     'modifiable':False,  'template':'BAD_PLAN', 
     'predicate':"(operation = 'MERGE JOIN' and options = 'CARTESIAN')"}
    rule5 = {'audit_type':'SQL', 
     'target':'',  'name':'',  'risky':'',  'description':', , 10', 
     'modifiable':True,  'template':'BAD_PLAN', 
     'predicate':'100', 
     'predicate_template':"(operation = 'INDEX' and options = 'SKIP SCAN') and cost > {}"}
    rule6 = {'audit_type':'SQL', 
     'target':'',  'name':'',  'risky':'',  'description':', , 10', 
     'modifiable':True,  'template':'BAD_PLAN', 
     'predicate':'100', 
     'predicate_template':"(operation = 'INDEX' and options = 'FAST FULL SCAN') and cost > {}"}
    rule7 = {'audit_type':'SQL', 
     'target':'',  'name':'',  'risky':'',  'description':', ', 
     'modifiable':False,  'template':'BAD_PLAN', 
     'predicate':"(operation = 'PARTITION RANGE' and options = 'ALL')"}
    rule12 = {'audit_type':'SQL', 
     'target':'',  'name':': (INTERNAL_FUNCTION)',  'risky':'',  'description':', DATETIMESTAMP, ', 
     'modifiable':False,  'template':'TYPE_CONVERSION', 
     'predicate':'(REGEXP_LIKE(filter_predicates, \'INTERNAL_FUNCTION\\("[^"]+"\\)\') and not REGEXP_LIKE(filter_predicates, \'(AND|OR) INTERNAL_FUNCTION\\("[^"]+"\\)\') and not REGEXP_LIKE(filter_predicates, \'INTERNAL_FUNCTION\\("[^"]+"\\) (AND|OR)\'))'}
    rule13 = {'audit_type':'SQL', 
     'target':'',  'name':'',  'risky':'',  'description':', (AND,OR), ', 
     'modifiable':False,  'template':'TYPE_CONVERSION', 
     'predicate':'(REGEXP_LIKE(filter_predicates, \'(AND|OR) INTERNAL_FUNCTION\\("[^"]+"\\)\') or REGEXP_LIKE(filter_predicates, \'INTERNAL_FUNCTION\\("[^"]+"\\) (AND|OR)\'))'}
    rule14 = {'audit_type':'SQL', 
     'target':'',  'name':'',  'risky':'',  'description':', , , ', 
     'modifiable':False,  'template':'TYPE_CONVERSION', 
     'predicate':'(REGEXP_LIKE(filter_predicates, \'\\("[^"]+"\\)\') and not REGEXP_LIKE(filter_predicates, \'INTERNAL_FUNCTION\\("[^"]+"\\)\')) and (operation = \'INDEX\' or operation like \'%TABLE%\')'}
    rule17 = {'audit_type':'SQL', 
     'target':'SQL',  'name':'',  'risky':'',  'description':'', 
     'modifiable':True,  'template':'CARDINALITY_GAP', 
     'predicate':'1000'}
    rule18 = {'audit_type':'SQL', 
     'target':'SQL',  'name':'',  'risky':'',  'description':'', 
     'modifiable':True,  'template':'DATAFLOW_GAP', 
     'predicate':'1000'}
    rule19 = {'audit_type':'SQL', 
     'target':'SQL',  'name':'',  'risky':'',  'description':'', 
     'modifiable':True,  'template':'INDEX_ROWS', 
     'predicate':'10000'}
    rule20 = {'audit_type':'SQL', 
     'target':'SQL',  'name':'',  'risky':'',  'description':'', 
     'modifiable':True,  'template':'OPERATION_STARTS', 
     'predicate':'100000'}
    rule21 = {'audit_type':'', 
     'target':'',  'name':'',  'risky':'',  'description':'', 
     'modifiable':True,  'template':'TABLE_OLD_STATS', 
     'predicate':'30'}
    rule22 = {'audit_type':'', 
     'target':'',  'name':'(stale)',  'risky':'',  'description':'(10%), (stale)', 
     'modifiable':False,  'template':'TABLE_STALE_STATS', 
     'predicate':'10'}
    rule23 = {'audit_type':'', 
     'target':'',  'name':'',  'risky':'',  'description':', ', 
     'modifiable':False,  'template':'TABLE_LOCKED_STATS', 
     'predicate':'10'}
    rule24 = {'audit_type':'', 
     'target':'',  'name':'',  'risky':'',  'description':', , 7', 
     'modifiable':True,  'template':'TABLE_MISSING_STATS', 
     'predicate':'7'}
    rule25 = {'audit_type':'', 
     'target':'',  'name':'(blocks > 0), (num_rows = 0)',  'risky':'',  'description':', , 1280(10MB)', 
     'modifiable':True,  'template':'TABLE_INCONSISTENT_STATS', 
     'predicate':'1280'}
    rule26 = {'audit_type':'', 
     'target':'',  'name':'(blocks = 0, num_rows = 0)',  'risky':'',  'description':', ', 
     'modifiable':False,  'template':'TABLE_EMPTY_STATS', 
     'predicate':'1280'}
    rule27 = {'audit_type':'', 
     'target':'',  'name':'',  'risky':'',  'description':', , DDL, ', 
     'modifiable':True,  'template':'TABLE_PARTITIONS', 
     'predicate':'100'}
    rule28 = {'audit_type':'', 
     'target':'',  'name':'',  'risky':'',  'description':', , DDL, ', 
     'modifiable':True,  'template':'TABLE_SUBPARTITIONS', 
     'predicate':'100'}
    rule29 = {'audit_type':'', 
     'target':'',  'name':'',  'risky':'',  'description':'', 
     'modifiable':False,  'template':'TMP_TABLE_STATS', 
     'predicate':'1'}
    rule30 = {'audit_type':'', 
     'target':'',  'name':'',  'risky':'',  'description':'', 
     'modifiable':False,  'template':'TABLE_DEGREE', 
     'predicate':'1'}
    rule31 = {'audit_type':'', 
     'target':'',  'name':'',  'risky':'',  'description':', , (GB)', 
     'modifiable':True,  'template':'TABLE_SMALL_DEGREE', 
     'predicate':'1'}
    rule32 = {'audit_type':'', 
     'target':'',  'name':'',  'risky':'',  'description':'', 
     'modifiable':False,  'template':'TABLE_INDEX_INCONSISTENT_DEGREE', 
     'predicate':'1'}
    rule33 = {'audit_type':'', 
     'target':'',  'name':'(stale)',  'risky':'',  'single':False,  'description':'(stale)', 
     'modifiable':False,  'template':'PARTITION_STALE_STATS', 
     'predicate':'1'}
    rule34 = {'audit_type':'', 
     'target':'',  'name':'',  'risky':'',  'single':False,  'description':'', 
     'modifiable':False,  'template':'PARTITION_LOCKED_STATS', 
     'predicate':'1'}
    rule35 = {'audit_type':'', 
     'target':'',  'name':'',  'risky':'',  'single':False,  'description':', , 7', 
     'modifiable':False,  'template':'PARTITION_MISSING_STATS', 
     'predicate':'1'}
    rule36 = {'audit_type':'', 
     'target':'',  'name':'(blocks > 0)  num_rows = 0',  'risky':'',  'single':False,  'description':', , 1280(10MB)', 
     'modifiable':False,  'template':'PARTITION_INCONSISTENT_STATS', 
     'predicate':'1280'}
    rule37 = {'audit_type':'', 
     'target':'',  'name':' (0 rows 0 blocks)',  'risky':'',  'single':False,  'description':' (0 rows 0 blocks)', 
     'modifiable':False,  'template':'PARTITION_EMPTY_STATS', 
     'predicate':'1280'}
    rule38 = {'audit_type':'', 
     'target':'',  'name':', LONG, RAW, LONG RAW',  'risky':'',  'single':False,  'description':', LONG, RAW, LONG RAW', 
     'modifiable':False,  'template':'HAS_RAW', 
     'predicate':'1'}
    rule39 = {'audit_type':'', 
     'target':'',  'name':'Lob  BASEFILE ',  'risky':'',  'single':False,  'description':'Lob  BASEFILE ,  11g , Oracle  SECUREFILE ', 
     'modifiable':False,  'template':'BASEFILE_LOB', 
     'predicate':'1'}
    rule40 = {'audit_type':'', 
     'target':'',  'name':'',  'risky':'',  'single':False,  'description':', ', 
     'modifiable':False,  'template':'MISSING_PK', 
     'predicate':'1'}
    rule41 = {'audit_type':'', 
     'target':'',  'name':'',  'risky':'',  'description':', ', 
     'modifiable':False,  'template':'REDUNDANT_INDEX', 
     'predicate':'1'}
    rule42 = {'audit_type':'', 
     'target':'',  'name':'',  'risky':'',  'description':', update/delete, (TM), DML', 
     'modifiable':False,  'template':'UNINDEXED_FK', 
     'predicate':'1'}
    rule43 = {'audit_type':'', 
     'target':'',  'name':'SQL',  'risky':'',  'single':False,  'description':'', 
     'modifiable':False,  'template':'UNUSED_INDEX', 
     'predicate':'1'}
    rule44 = {'audit_type':'', 
     'target':'',  'name':'',  'risky':'',  'single':False,  'description':', , 8', 
     'modifiable':True,  'template':'SINGLE_TABLE_INDEXES', 
     'predicate':'8'}
    rule45 = {'audit_type':'', 
     'target':'',  'name':'',  'risky':'',  'single':False,  'description':', , 5', 
     'modifiable':True,  'template':'INDEX_COLUMNS', 
     'predicate':'5'}
    rule46 = {'audit_type':'', 
     'target':'',  'name':'',  'risky':'',  'single':False,  'description':'UNUSABLE', 
     'modifiable':False,  'template':'UNUSABLE_INDEX', 
     'predicate':'1'}
    rule47 = {'audit_type':'', 
     'target':'',  'name':' IDX_ ',  'risky':'',  'single':False,  'description':' IDX_ ', 
     'modifiable':True,  'template':'INDEX_NAMING', 
     'predicate':'IDX_'}
    rule48 = {'audit_type':'', 
     'target':'',  'name':'',  'risky':'',  'description':', , 7', 
     'modifiable':True,  'template':'INDEX_MISSING_STATS', 
     'predicate':'7'}
    rule49 = {'audit_type':'', 
     'target':'',  'name':'',  'risky':'',  'single':False,  'description':', , , Library Cache, DFS LOCK HANDLE, 100', 
     'modifiable':True,  'template':'SEQUENCE_CACHE', 
     'predicate':'100'}
    rule50 = {'audit_type':'', 
     'target':'',  'name':'RAC ORDER ',  'risky':'',  'single':False,  'description':' ORDER , ', 
     'modifiable':False,  'template':'SEQUENCE_ORDER', 
     'predicate':'1'}
    rule51 = {'audit_type':'', 
     'target':'',  'name':'1',  'risky':'',  'single':False,  'description':', 1', 
     'modifiable':True,  'template':'SEQUENCE_INCREMENT_BY', 
     'predicate':'1'}
    rule52 = {'audit_type':'', 
     'target':'',  'name':' SEQ_ ',  'risky':'',  'single':False,  'description':'', 
     'modifiable':True,  'template':'SEQUENCE_NAMING', 
     'predicate':'SEQ_'}
    rule53 = {'audit_type':'SQL', 
     'target':'SQL',  'name':'',  'risky':'',  'description':' SQL , ,  SQL ,  SQL ', 
     'modifiable':True,  'template':'BIND_VARIABLE', 
     'predicate':'10'}
    rule54 = {'audit_type':'SQL', 
     'target':'SQL',  'name':'',  'risky':'',  'description':', , , SQL ', 
     'modifiable':False,  'template':'OVER_BIND_VARIABLE', 
     'predicate':'1'}
    rule55 = {'audit_type':'SQL', 
     'target':'',  'name':'Update  Where ',  'risky':'',  'description':'Update  Where , , ,undo,, , :10', 
     'modifiable':True,  'template':'UPDATE_WHERE', 
     'predicate':'10'}
    rule56 = {'audit_type':'SQL', 
     'target':'',  'name':'Delete  Where ',  'risky':'',  'description':'Delete  Where , , ,undo,,  Truncate , , :10', 
     'modifiable':True,  'template':'DELETE_WHERE', 
     'predicate':'10'}
    rule57 = {'audit_type':'', 
     'target':'',  'name':'',  'risky':'',  'single':False,  'description':'OLTP , ; , HASH Join ', 
     'modifiable':False,  'template':'BITMAP_INDEX', 
     'predicate':'10'}
    rule58 = {'audit_type':'SQL', 
     'target':'SQL',  'name':'',  'risky':'',  'description':', , 5', 
     'modifiable':True,  'template':'TABLE_FILTER', 
     'predicate':'5'}
    rule59 = {'audit_type':'SQL', 
     'target':'',  'name':'Select  Where ',  'risky':'',  'description':'Select  Where , , , :10', 
     'modifiable':True,  'template':'SELECT_WHERE', 
     'predicate':'10'}
    rule60 = {'audit_type':'SQL', 
     'target':'',  'name':' FILTER ',  'risky':'',  'description':'Rownum, Group By, FILTER', 
     'modifiable':False,  'template':'PLAN_FILTER', 
     'predicate':'10'}
    rule61 = {'audit_type':'SQL', 
     'target':'',  'name':'',  'risky':'',  'description':',  CPU, IO ,  OLTP ', 
     'modifiable':False,  'template':'PARALLEL_PLAN', 
     'predicate':'10'}
    rule62 = {'audit_type':'', 
     'target':'',  'name':' not null ',  'risky':'',  'description':' not null ,  is null ', 
     'modifiable':False,  'template':'INDEX_NULL', 
     'predicate':'10'}
    rule63 = {'audit_type':'', 
     'target':'',  'name':'',  'risky':'',  'single':False,  'description':', (GB), 10GB', 
     'modifiable':True,  'template':'TABLE_NOPARTITION', 
     'predicate':'10'}
    rule64 = {'audit_type':'', 
     'target':'',  'name':'',  'risky':'',  'description':', , ', 
     'modifiable':False,  'template':'MULTI_RANGE_KEY', 
     'predicate':'10'}
    rule65 = {'audit_type':'', 
     'target':'',  'name':'',  'risky':'',  'description':', , 10', 
     'modifiable':True,  'template':'SKEW_PARTITION', 
     'predicate':'10'}
    rule66 = {'audit_type':'', 
     'target':'',  'name':'unique',  'risky':'',  'description':'unique', 
     'modifiable':False,  'template':'GLOBAL_INDEX', 
     'predicate':'10'}
    rule67 = {'audit_type':'SQL', 
     'target':'SQL',  'name':'SELECT *',  'risky':'',  'single':False,  'description':', ', 
     'modifiable':False,  'template':'SELECT_STAR', 
     'predicate':'1'}
    rule68 = {'audit_type':'SQL', 
     'target':'SQL',  'name':'SQL  Hint',  'risky':'',  'single':False,  'description':'SQL  Hint,  Hint , ', 
     'modifiable':False,  'template':'WITH_HINT', 
     'predicate':'1'}
    rule69 = {'audit_type':'SQL', 
     'target':'',  'name':'SQL  SQL Profile SQL PLAN Baseline',  'risky':'',  'description':' SQL Profile SQL PLAN Baseline, ', 
     'modifiable':False,  'template':'SQL_PROFILE', 
     'predicate':'1'}
    rule70 = {'audit_type':'', 
     'target':'',  'name':'',  'risky':'',  'single':False,  'description':', , 30', 
     'modifiable':True,  'template':'SKEW_COLUMN', 
     'predicate':'30'}
    rule71 = {'audit_type':'', 
     'target':'',  'name':'',  'risky':'',  'description':'1,  bucket , , ', 
     'modifiable':False,  'template':'WRONG_HISTOGRAM', 
     'predicate':'1'}
    rule74 = {'audit_type':'SQL', 
     'target':'SQL',  'name':'',  'risky':'',  'description':", Like '%ABC', ", 
     'modifiable':False,  'template':'LEFT_WILDCARD', 
     'predicate':'1'}
    rule75 = {'audit_type':'SQL', 
     'target':'SQL',  'name':'Insert ',  'risky':'',  'single':False,  'description':'Insert into t values(...), ', 
     'modifiable':False,  'template':'INSERT_VALUE', 
     'predicate':'1'}
    rule76 = {'audit_type':'SQL', 
     'target':'SQL',  'name':'In',  'risky':'',  'description':'IN,,  join .  SQL .  In , 20', 
     'modifiable':True,  'template':'MANY_BINDS', 
     'predicate':'20'}
    rule77 = {'audit_type':'', 
     'target':'',  'name':'',  'risky':'',  'description':', , 7', 
     'modifiable':True,  'template':'OBJECT_CREATED', 
     'predicate':'7'}
    rule78 = {'audit_type':'', 
     'target':'',  'name':'',  'risky':'',  'description':', , 7', 
     'modifiable':True,  'template':'OBJECT_DDL', 
     'predicate':'7'}
    rule79 = {'audit_type':'', 
     'target':'',  'name':'',  'risky':'',  'description':', , , 10', 
     'modifiable':True,  'template':'JOIN_NULL', 
     'predicate':'10'}
    rule80 = {'audit_type':'SQL', 
     'target':'',  'name':'Select ... For Update',  'risky':'',  'description':', , ', 
     'modifiable':False,  'template':'FOR_UPDATE', 
     'predicate':'10'}
    rule81 = {'audit_type':'',  'target':'',  'name':'CHAR',  'risky':'',  'single':False,  'description':'CHAR, , trim', 
     'modifiable':False,  'template':'CHAR_COL', 
     'predicate':'1'}
# okay decompiling ./restful/hawkeye/sqlaudit/enum/oracle_audit_rule_enum.pyc
