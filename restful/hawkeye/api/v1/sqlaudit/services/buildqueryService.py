# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/sqlaudit/services/buildqueryService.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 4590 bytes
from sqlaudit.enum.sql_stats_enum import SQL_STAT

def build_rule_query(template, database, rule, schema, max_rows, order_by_pred):
    template = template.get(rule.template)
    schema_name = template.get('schema_name')
    instance_id_list = database.instance_id_list
    schema = (',').join([("'{}'").format(x) for x in schema.split(',')])
    if 'NAMING' in rule.template:
        rule.predicate = rule.predicate.replace('_', '=_')
    data = {'schema_pred':{schema_name}, 
     'sql_text_pred':f''' in ({schema})''',  'topn':f'''not regexp_like(translate(sql_text,chr(10)||chr(11)||chr(13), ' '),' (SYS.)?(CDB_|DBA_|ALL_|USER_|v\$|gv\$)', 'i')where rownum <={max_rows}''',  'pred':rule.predicate_templaterule.predicaterule.predicate_template.format(rule.predicate), 
     'order_by_pred':SQL_STAT.get(order_by_pred), 
     'inst_id_pred':f'''inst_id in ({instance_id_list})'''}
    query = template.get('sql').format(**data)
    return query


def build_total_query(template, database, schema):
    formatted_template = {}
    instance_id_list = database.instance_id_list
    schema = (',').join([("'{}'").format(x) for x in schema.split(',')])
    for k, v in template.items():
        schema_name = v.get('schema_name')
        data = {'sql_text_pred':"not regexp_like(translate(sql_text,chr(10)||chr(11)||chr(13), ' '),' (SYS.)?(CDB_|DBA_|ALL_|USER_|v\\$|gv\\$)', 'i')", 
         'schema_pred':f'''{schema_name} in ({schema})''', 
         'inst_id_pred':f'''inst_id in ({instance_id_list})'''}
        formatted_template[k] = v.get('sql').format(**data)

    return formatted_template


def build_rule_single_query(template, database, rule, sql_id, schema_list_str):
    template = template.get(rule.template)
    if not template:
        return
    else:
        schema_name = template.get('schema_name')
        instance_id_list = database.instance_id_list
        sql_id_pred = f'''sql_id = '{sql_id}''''
        inst_id_pred = f'''inst_id in ({instance_id_list})'''
        table_pred = ''
        if schema_name:
            table_pred = f'''({schema_name}) in ({schema_list_str})'''
        if 'NAMING' in rule.template:
            rule.predicate = rule.predicate.replace('_', '=_')
        data = {'table_pred':table_pred, 
         'sql_id_pred':sql_id_pred, 
         'pred':rule.predicate_templaterule.predicaterule.predicate_template.format(rule.predicate), 
         'inst_id_pred':inst_id_pred}
        query = None
        if template:
            query = template.get('sql').format(**data)
        return query


def build_db2_rule_single_query(template, database, rule, schema_list_str):
    template = template.get(rule.template)
    if not template:
        return
    else:
        schema_name = template.get('schema_name')
        table_pred = ''
        if schema_name:
            table_pred = f'''({schema_name}) in (values{schema_list_str})'''
        data = {'table_pred':table_pred,  'pred':rule.predicate_templaterule.predicaterule.predicate_template.format(rule.predicate)}
        query = None
        if template:
            query = template.get('sql').format(**data)
        return query


def build_tables_query(database, sql_id):
    instance_id_list = database.instance_id_list
    sql_id_pred = f'''sql_id = '{sql_id}''''
    inst_id_pred = f'''inst_id in ({instance_id_list})'''
    query_tables = f'''
        select object_owner, object_name
        from
            (SELECT object_owner, object_type, object_name from gv$sql_plan where {inst_id_pred} and {sql_id_pred}) where object_type like 'TABLE%'
        union
        select table_owner, table_name from
        dba_indexes where (owner, index_name) in
        (select object_owner, object_name from (SELECT object_owner, object_type, object_name from gv$sql_plan where {inst_id_pred} and {sql_id_pred}) where object_type like 'INDEX%')'''
    return query_tables


def build_static_query(template, schema, table_name, pred):
    schema_name = template.get('schema_name')
    table_pred = ''
    if schema_name:
        table_pred = f'''({schema_name}) in (('{schema}','{table_name}'))'''
    data = {'table_pred':table_pred,  'pred':pred}
    query = None
    if template:
        query = template.get('sql').format(**data)
    return query


def build_static_rule_query(template, rule):
    template = template.get(rule.template)
    data = {'pred': rule.predicate_templaterule.predicaterule.predicate_template.format(rule.predicate)}
    query = template.get('sql').format(**data)
    return query
# okay decompiling ./restful/hawkeye/api/v1/sqlaudit/services/buildqueryService.pyc
