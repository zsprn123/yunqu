# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/enum/sql_audit_enum.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 5001 bytes
from django.db.models import Q
from sqlaudit.models import Audit_Rule
from api.v1.monitor.services.runsqlService import run_sql, run_batch_sql
from api.v1.sqlaudit.services.buildqueryService import build_tables_query, build_rule_single_query, build_db2_rule_single_query
from sqlaudit.enum.single_sql_audit_enum import SingleTemplateJson
from sqlaudit.enum.table_stats_enum import format_table_stats
from collections import defaultdict

def build_single_audit_result(rule_list, detail_result):
    audit_result = {}
    for rule in rule_list:
        rule_detail_result = detail_result.get(rule.name)
        if rule_detail_result:
            result = []
            if rule.target in (u'\u8868', u'\u5206\u533a', u'\u7d22\u5f15', u'\u4e34\u65f6\u8868',
                               u'\u5e8f\u5217', u'\u5b57\u6bb5'):
                result = format_table_stats(rule.template, rule_detail_result)
            else:
                result = rule_detail_result
            audit_result[rule.name] = result

    return audit_result


def get_oracle_sql_audit(database, sql_id, only_tune=False):
    audit_rule_queryset = []
    if only_tune:
        audit_rule_queryset = Audit_Rule.objects.filter((Q(database=database)) & (Q(enabled=True)) & (Q(single=True)) & (Q(is_static_rule=False)) & (Q(name__in=['', '', ''])))
    else:
        audit_rule_queryset = Audit_Rule.objects.filter((Q(database=database)) & (Q(enabled=True)) & (Q(single=True)) & (Q(is_static_rule=False)))
    tables_query = build_tables_query(database, sql_id)
    flag, tables = run_sql(database, tables_query)
    if not flag:
        return tables
    else:
        schema_list = [("('{}','{}')").format(x.get('OBJECT_OWNER'), x.get('OBJECT_NAME')) for x in tables]
        schema_list_str = (',').join(schema_list) if schema_list else "('','')"
        query_detail_json = {}
        for rule in audit_rule_queryset:
            query = build_rule_single_query(SingleTemplateJson.get(database.db_type), database, rule, sql_id, schema_list_str)
            if query:
                query_detail_json[rule.name] = query

        flag, audit_data = run_batch_sql(database, query_detail_json)
        audit_result = build_single_audit_result(audit_rule_queryset, audit_data)
        return audit_result


def get_db2_single_sql_plan_audit(database, sql_text, plans=[]):
    from sqlaudit.enum.db2_function_enum import FULL_SCAN, INDEX_ROWS
    audit_result = {}
    audit_sql_rule_queryset = Audit_Rule.objects.filter((Q(database=database)) & (Q(enabled=True)) & (Q(audit_type='SQL')) & (Q(target='')) & (Q(single=True)))
    for rule in audit_sql_rule_queryset:
        template = rule.template
        func_str = f'''{template}(rule, sql_text, plans)'''
        result = eval(func_str)
        if result:
            audit_result[rule.name] = result

    return audit_result


def get_db2_single_sql_text_audit(database, sql_text, plans=[]):
    from sqlaudit.enum.static_oracle_function_enum import preprocess_sqltext, LEFT_WILDCARD, INSERT_VALUE, SELECT_STAR
    audit_result = defaultdict(list)
    audit_sql_rule_queryset = Audit_Rule.objects.filter((Q(database=database)) & (Q(enabled=True)) & (Q(audit_type='SQL')) & (Q(target='SQL')) & (Q(single=True)))
    sql = preprocess_sqltext(sql_text)
    for rule in audit_sql_rule_queryset:
        template = rule.template
        func_str = f'''{template}(sql)'''
        flag, message = eval(func_str)
        if flag:
            audit_result[rule.name].append({'sql_text': sql})

    return audit_result


def get_db2_sql_audit(database, sql_id, sql_text=None, plans=[]):
    schema_list = [("('{}','{}')").format(x.get('OBJECT_OWNER'), x.get('OBJECT_NAME')) for x in plans if x.get('OBJECT_NAME')]
    schema_list_str = (',').join(schema_list) if schema_list else "('','')"
    audit_rule_queryset = Audit_Rule.objects.filter((Q(database=database)) & (Q(enabled=True)) & (Q(audit_type='')) & (Q(single=True)))
    query_detail_json = {}
    for rule in audit_rule_queryset:
        query = build_db2_rule_single_query(SingleTemplateJson.get(database.db_type), database, rule, schema_list_str)
        if query:
            query_detail_json[rule.name] = query

    flag, audit_data = run_batch_sql(database, query_detail_json)
    audit_result = build_single_audit_result(audit_rule_queryset, audit_data)
    sql_audit_plan_result = get_db2_single_sql_plan_audit(database, sql_text, plans)
    sql_audit_text_result = get_db2_single_sql_text_audit(database, sql_text, plans)
    audit_result = {**audit_result, **sql_audit_plan_result, **sql_audit_text_result}
    print(audit_result)
    return audit_result
# okay decompiling ./restful/hawkeye/api/enum/sql_audit_enum.pyc
