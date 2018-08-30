# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/monitor/services/sqldetail/common.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 3646 bytes
from monitor.models import Oracle_ASH, DB2_ASH, MySQL_ASH, MSSQL_ASH
from api.v1.monitor.services.runsqlService import run_sql, run_batch_sql
from common.util import build_exception_from_java
ASH_DICT = {'oracle':Oracle_ASH, 
 'mysql':MySQL_ASH, 
 'sqlserver':MSSQL_ASH, 
 'db2':DB2_ASH}
PLAN_HEADER = {'oracle':[
  'ID', 'PLAN_STEP', 'OBJECT_OWNER', 'OBJECT_NAME', 'CARDINALITY', 'COST',
  'ACCESS_PREDICATES', 'FILTER_PREDICATES'], 
 'db2':[
  'ID', 'PLAN_STEP', 'OBJECT_OWNER', 'OBJECT_NAME', 'CARDINALITY', 'COST',
  'ACCESS_PREDICATES', 'FILTER_PREDICATES'], 
 'mysql':[
  'id', 'key', 'ref', 'rows', 'type', 'Extra', 'table', 'key_len', 'filtered', 'partitions', 'select_type', 'possible_keys']}

def get_default_sql_detail_format(db_type):
    sql_detail = {}
    sql_detail['sql_text'] = ''
    sql_detail['stats'] = {}
    sql_detail['tune'] = {}
    sql_detail['audit'] = {}
    sql_detail['plans'] = {'header':PLAN_HEADER.get(db_type), 
     'data':[]}
    sql_detail['sqlmon'] = {'header':[
      'STATUS', 'SQL_ID', 'ELAPSED_TIME', 'DB_TIME', 'DB_CPU', 'SQL_EXEC_ID', 'SQL_EXEC_START',
      'SQL_PLAN_HASH_VALUE', 'INST_ID', 'USERNAME'], 
     'data':[]}
    sql_detail['binds'] = {'header':[
      'CHILD_NUMBER', 'NAME', 'POSITION', 'DATATYPE_STRING', 'VALUE_STRING', 'LAST_CAPTURED'], 
     'data':[]}
    sql_detail['top_activity'] = {}
    sql_detail['sql_id'] = ''
    sql_detail['dim'] = 11
    return sql_detail


def get_sql_text(database, sql_id):
    sql_text = ''
    db_type = database.db_type
    model = ASH_DICT.get(db_type)
    obj = (((model.objects.filter(database=database)).filter(sql_id=sql_id)).filter(sql_text__isnull=False)).order_by('-created_at').first()
    if obj:
        return (obj.sql_text, obj.db_name)
    if sql_id != 'null':
        if db_type == 'oracle':
            instance_id_list = database.instance_id_list
            query_sqltext_realtime = f'''select sql_fulltext SQL_TEXT from gv$sql where inst_id in ({instance_id_list}) and sql_id= '{sql_id}' and rownum=1'''
            query_sqltext_hist = f'''select SQL_TEXT from DBA_HIST_SQLTEXT where sql_id='{sql_id}' and rownum=1'''
            flag, sql_text = run_sql(database, query_sqltext_realtime)
            if not flag:
                raise build_exception_from_java(sql_text)
            else:
                if not sql_text:
                    flag, sql_text = run_sql(database, query_sqltext_hist)
                    if not flag:
                        raise build_exception_from_java(sql_text)
            return (
             sql_text[0].get('SQL_TEXT') if sql_text else '', None)
        if db_type == 'sqlserver':
            query = f'''
        select top 1 TEXT as SQL_TEXT from sys.dm_exec_sql_text(cast('' as xml).value('xs:hexBinary("{sql_id}")', 'varbinary(max)'))'''
            flag, sql_text = run_sql(database, query)
            if not flag:
                raise build_exception_from_java(sql_text)
            return (
             sql_text[0].get('SQL_TEXT') if sql_text else database.db_name, None)
        if db_type == 'db2':
            query = f'''
        select
        stmt_text SQL_TEXT
        from
        TABLE(MON_GET_PKG_CACHE_STMT(null,
                                     null,
                                     null,
                                     -2))
        cache
    where
    EXECUTABLE_ID = x'{sql_id}'
    fetch first 1 rows only
    '''
            flag, sql_text = run_sql(database, query)
            if not flag:
                raise build_exception_from_java(sql_text)
            return (
             sql_text[0].get('SQL_TEXT') if sql_text else database.db_name, None)
        return ('', None)
# okay decompiling ./restful/hawkeye/api/v1/monitor/services/sqldetail/common.pyc
