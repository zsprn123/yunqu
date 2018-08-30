# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./sqlaudit/enum/static_oracle_function_enum.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 9457 bytes
import re, sqlparse
from api.v1.sqlaudit.services.buildqueryService import build_static_query
from sqlaudit.enum.static_sql_enum import StaticSQLJson
from api.v1.monitor.services.runsqlService import run_sql
from sqlparse.sql import Where

def get_type(sqltext):
    parsed = sqlparse.parse(sqltext)[0]
    sql_type = parsed.get_type()
    object_type = None
    if sql_type == 'UNKNOWN':
        keyword = ''
        try:
            keyword = next((str(t) for t in parsed.tokens if t.match(sqlparse.tokens.Keyword, 'truncate', True)))
        except:
            pass

        if keyword.upper() == 'TRUNCATE':
            sql_type = 'TRUNCATE'
    try:
        object_type = next((str(t) for t in parsed.tokens if t.match(sqlparse.tokens.Keyword, '\\w+', True)))
    except:
        pass

    return (
     sql_type.upper(), object_type.upper() if object_type else None)


def preprocess_sqltext(sqltext):
    sqltext_without_comment = sqlparse.format(sqltext, strip_comments=True)
    return (' ').join(sqltext_without_comment.split()).rstrip(';')


def get_name(sqltext):
    prog = re.compile('^(?:\\S+\\s){2}(\\S+)', re.IGNORECASE)
    m = prog.search(sqltext)
    if m:
        name = m.group(1)
        prog2 = re.compile('[^\\(]+', re.IGNORECASE)
        m2 = prog2.search(name)
        if m2:
            return m2.group(0)


def SEQUENCE_CACHE(sqltext, pred=0, schema=None, database=None):
    prog = re.compile('cache', re.IGNORECASE)
    result = prog.search(sqltext)
    found = '20'
    m = re.search('cache (\\d+)', sqltext, re.IGNORECASE)
    if m:
        found = m.group(1)
    if not result or int(found) < int(pred):
        return (True, found)
    else:
        return (False, None)


def SEQUENCE_ORDER(sqltext, pred=0, schema=None, database=None):
    prog = re.compile('noorder', re.IGNORECASE)
    result = prog.search(sqltext)
    if not result:
        return (True, None)
    else:
        return (False, None)


def SEQUENCE_INCREMENT_BY(sqltext, pred=0, schema=None, database=None):
    found = '1'
    m = re.search('INCREMENT BY (\\d+)', sqltext, re.IGNORECASE)
    if m:
        found = m.group(1)
    if int(found) > int(pred):
        return (True, found)
    else:
        return (False, None)


def SEQUENCE_NAMING(sqltext, pred=0, schema=None, database=None):
    prog = re.compile(('SEQUENCE {}').format(pred), re.IGNORECASE)
    result = prog.search(sqltext)
    if not result:
        return (True, None)
    else:
        return (False, None)


def HAS_RAW(sqltext, pred=0, schema=None, database=None):
    prog = re.compile('( LONG| RAW| LONG RAW)', re.IGNORECASE)
    result = prog.search(sqltext)
    if result:
        return (True, None)
    else:
        return (False, None)


def BASEFILE_LOB(sqltext, pred=0, schema=None, database=None):
    prog = re.compile('( CLOB| BLOB)', re.IGNORECASE)
    result = prog.search(sqltext)
    prog2 = re.compile('STORE AS SECUREFILE', re.IGNORECASE)
    result2 = prog2.search(sqltext)
    if result:
        if not result2:
            return (True, None)
        return (False, None)


def TABLE_TABLESPACE(sqltext, pred=0, schema=None, database=None):
    prog = re.compile('tablespace', re.IGNORECASE)
    result = prog.search(sqltext)
    if not result:
        return (True, None)
    else:
        return (False, None)


def INDEX_TABLESPACE(sqltext, pred=0, schema=None, database=None):
    prog = re.compile('tablespace', re.IGNORECASE)
    result = prog.search(sqltext)
    if not result:
        return (True, None)
    else:
        return (False, None)


def INDEX_NAMING(sqltext, pred=0, schema=None, database=None):
    prog = re.compile(('INDEX {}').format(pred), re.IGNORECASE)
    result = prog.search(sqltext)
    if not result:
        return (True, None)
    else:
        return (False, None)


def CREATE_INDEX_PARALLEL(sqltext, pred=0, schema=None, database=None):
    prog = re.compile(' PARALLEL', re.IGNORECASE)
    result = prog.search(sqltext)
    if not result:
        return (True, None)
    else:
        return (False, None)


def CREATE_INDEX_ONLINE(sqltext, pred=0, schema=None, database=None):
    prog = re.compile(' ONLINE', re.IGNORECASE)
    result = prog.search(sqltext)
    if not result:
        return (True, None)
    else:
        return (False, None)


def INDEX_NAMING(sqltext, pred=0, schema=None, database=None):
    prog = re.compile('INDEX IDX\\_', re.IGNORECASE)
    result = prog.search(sqltext)
    if not result:
        return (True, None)
    else:
        return (False, None)


def INDEX_COLUMNS(sqltext, pred=0, schema=None, database=None):
    prog = re.compile('ON [\\w$]+ ?\\(([^)]+)\\)', re.IGNORECASE)
    m = prog.search(sqltext)
    if m:
        columns = m.group(1)
        columns = columns.replace(' ', '')
        columns_list = columns.split(',')
        if len(columns_list) > int(pred):
            return (True, str(len(columns_list)))
        return (False, None)


def REDUNDANT_INDEX(sqltext, pred=0, schema=None, database=None):
    prog = re.compile('ON ([\\w$]+) ?\\(([^)]+)\\)', re.IGNORECASE)
    m = prog.search(sqltext)
    if m:
        table_name = m.group(1).upper()
        columns = m.group(2).upper()
        columns = columns.replace(' ', '')
        columns = (':').join(columns.split(','))
        query = build_static_query(StaticSQLJson.get('REDUNDANT_INDEX'), schema, table_name, columns)
        flag, result = run_sql(database, query)
        if flag:
            if result:
                return (True, None)
            return (False, None)


def OBJECT_NAMING(sqltext, pred=0, schema=None, database=None):
    object_name = get_name(sqltext)
    prog = re.compile('[0-9$]', re.IGNORECASE)
    m = prog.search(object_name)
    if m:
        return (True, None)
    else:
        return (False, None)


def WRONG_OBJECT(sqltext, pred=0, schema=None, database=None):
    sql_type, object_type = get_type(sqltext)
    if object_type in ('TRIGGER', 'DATABASE', 'PUBLIC'):
        return (True, None)
    else:
        return (False, None)


def PARTITION_INDEX(sqltext, pred=0, schema=None, database=None):
    prog = re.compile('(ADD|COALESCEDROP|EXCHANGE|MERGE|MOVE|SPLIT|TRUNCATE) (SUB)?PARTITION', re.IGNORECASE)
    m = prog.search(sqltext)
    if m:
        prog2 = re.compile('UPDATE (GLOBAL )?INDEX', re.IGNORECASE)
        m2 = prog2.search(sqltext)
        if not m2:
            return (True, None)
        return (False, None)


def UPDATE_WHERE(sqltext, pred=0, schema=None, database=None):
    parsed = sqlparse.parse(sqltext)[0]
    where = [token for token in parsed.tokens if isinstance(token, Where)]
    if not where:
        return (True, None)
    else:
        return (False, None)


def DROP_OBJECT(sqltext, pred=0, schema=None, database=None):
    return (True, None)


def TRUNCATE(sqltext, pred=0, schema=None, database=None):
    return (True, None)


def ALTER_INDEX_PARALLEL(sqltext, pred=0, schema=None, database=None):
    prog = re.compile(' PARALLEL', re.IGNORECASE)
    result = prog.search(sqltext)
    prog2 = re.compile(' REBUILD', re.IGNORECASE)
    result2 = prog2.search(sqltext)
    if not result:
        if result2:
            return (True, None)
        return (False, None)


def ALTER_INDEX_ONLINE(sqltext, pred=0, schema=None, database=None):
    prog = re.compile(' ONLINE', re.IGNORECASE)
    result = prog.search(sqltext)
    prog2 = re.compile(' REBUILD', re.IGNORECASE)
    result2 = prog2.search(sqltext)
    if not result:
        if result2:
            return (True, None)
        return (False, None)


def OVER_BIND_VARIABLE(sqltext, pred=0, schema=None, database=None):
    prog = re.compile('(:[\\w]+ IS NULL|NVL\\(:[\\w]+)', re.IGNORECASE)
    result = prog.search(sqltext)
    if result:
        return (True, None)
    else:
        return (False, None)


def LEFT_WILDCARD(sqltext, pred=0, schema=None, database=None):
    prog = re.compile(" like '%", re.IGNORECASE)
    result = prog.search(sqltext)
    if result:
        return (True, None)
    else:
        return (False, None)


def INSERT_VALUE(sqltext, pred=0, schema=None, database=None):
    prog = re.compile('insert into[^(]+values', re.IGNORECASE)
    result = prog.search(sqltext)
    if result:
        return (True, None)
    else:
        return (False, None)


def MANY_BINDS(sqltext, pred=0, schema=None, database=None):
    prog = re.compile('in *\\(:[\\w]+( *, *:[\\w]+){%s}' % pred, re.IGNORECASE)
    result = prog.search(sqltext)
    if result:
        return (True, None)
    else:
        return (False, None)


def WITH_HINT(sqltext, pred=0, schema=None, database=None):
    prog = re.compile('(--\\+|/\\*\\+.*\\*/)', re.IGNORECASE)
    result = prog.search(sqltext)
    if result:
        return (True, None)
    else:
        return (False, None)


def SELECT_STAR(sqltext, pred=0, schema=None, database=None):
    prog = re.compile('select \\*', re.IGNORECASE)
    result = prog.search(sqltext)
    if result:
        return (True, None)
    else:
        return (False, None)


if __name__ == '__main__':
    sql1 = 'create table t1 (id number)'
    sql2 = 'create sequence s1 cache 20'
    sql3 = 'create index idx_t1 on t1(id)'
    sql4 = 'alter index idx_t1 rebuild'
    sql5 = 'alter table t1 add partition p1(values less than 100)'
    sql6 = 'update t1 set id=2 where 2>1'
    print(get_type(sql1))
    print(get_type(sql2))
    print(get_type(sql3))
    print(get_type(sql4))
    print(get_type(sql5))
    print(get_type(sql6))
# okay decompiling ./restful/hawkeye/sqlaudit/enum/static_oracle_function_enum.pyc
