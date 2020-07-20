# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/sqlaudit/services/initialService.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 5099 bytes
from api.v1.monitor.services.runsqlService import run_sql
from sqlaudit.enum.audit_rule_enum import AUDIT_RULE_ENUM
from sqlaudit.enum.static_audit_rule_enum import STATIC_AUDIT_RULE_ENUM
from sqlaudit.enum.audit_strategy_enum import StrategyEnum
from sqlaudit.models import Audit_Rule, Audit_Strategy
from django.db.models import Q

def sqlaudit_init(database):
    all_rules = (Audit_Rule.objects.filter(is_static_rule=False)).filter(database=database)
    none_static_rule_predicate = {rule.name:rule.predicate for rule in all_rules}
    none_static_rule_enabled = {rule.name:rule.enabled for rule in all_rules}
    none_static_rule_single = {rule.name:rule.single for rule in all_rules}
    all_rules = (Audit_Rule.objects.filter(is_static_rule=True)).filter(database=database)
    static_rule_predicate = {rule.name:rule.predicate for rule in all_rules}
    static_rule_enabled = {rule.name:rule.enabled for rule in all_rules}
    static_rule_single = {rule.name:rule.single for rule in all_rules}
    (Audit_Rule.objects.filter(database=database)).delete()
    (Audit_Strategy.objects.filter(database=database)).delete()
    init_audit_strategy(database)
    init_sql_rule(database, none_static_rule_predicate, static_rule_predicate, none_static_rule_enabled, static_rule_enabled, none_static_rule_single, static_rule_single)


def init_sql_rule(database, none_static_rule_predicate={}, static_rule_predicate={}, none_static_rule_enabled={}, static_rule_enabled={}, none_static_rule_single={}, static_rule_single={}):
    audit_rule_list = []
    SqlRuleEnum = AUDIT_RULE_ENUM.get(database.db_type) if AUDIT_RULE_ENUM.get(database.db_type) else []
    for default_sql_rule in SqlRuleEnum:
        name = default_sql_rule.value.get('name')
        predicate = none_static_rule_predicate.get(name)
        enabled = none_static_rule_enabled.get(name)
        single = none_static_rule_single.get(name)
        if predicate:
            default_sql_rule.value['predicate'] = predicate
        if enabled != None:
            default_sql_rule.value['enabled'] = enabled
        if single != None:
            default_sql_rule.value['single'] = single
        objs = Audit_Strategy.objects.filter((Q(audit_type=default_sql_rule.value.get('audit_type'))) & (Q(database=database)))
        audit_rule = Audit_Rule(remarks=default_sql_rule.name, 
         database=database, 
         audit_strategy=objs[0] if objs else None, **default_sql_rule.value)
        audit_rule_list.append(audit_rule)

    StaticRuleEnum = STATIC_AUDIT_RULE_ENUM.get(database.db_type) if STATIC_AUDIT_RULE_ENUM.get(database.db_type) else []
    for static_sql_rule in StaticRuleEnum:
        name = static_sql_rule.value.get('name')
        predicate = static_rule_predicate.get(name)
        enabled = static_rule_enabled.get(name)
        single = static_rule_single.get(name)
        if predicate:
            static_sql_rule.value['predicate'] = predicate
        if enabled != None:
            static_sql_rule.value['enabled'] = enabled
        if single != None:
            static_sql_rule.value['single'] = single
        objs = Audit_Strategy.objects.filter((Q(audit_type=static_sql_rule.value.get('audit_type'))) & (Q(database=database)))
        audit_rule = Audit_Rule(remarks=static_sql_rule.name, 
         database=database, 
         audit_strategy=objs[0] if objs else None, **static_sql_rule.value)
        audit_rule_list.append(audit_rule)

    Audit_Rule.objects.bulk_create(audit_rule_list)


def init_audit_strategy(database):
    strategy_list = []
    for default_audit_strategy in StrategyEnum:
        audit_strategy = Audit_Strategy(database=database, **default_audit_strategy.value)
        strategy_list.append(audit_strategy)

    Audit_Strategy.objects.bulk_create(strategy_list)


def get_database_schema_list(database):
    schema_query = {'oracle':"select\n                                username\n                            from\n                                dba_users\n                            where\n                                username not in ('MGMT_VIEW','MDDATA','MDSYS','SI_INFORMTN_SCHEMA','ORDPLUGINS','ORDSYS','OLAPSYS','SYSMAN','ANONYMOUS','XDB','CTXSYS','EXFSYS','WMSYS','ORACLE_OCM','DBSNMP','TSMSYS','DMSYS','DIP','OUTLN','SYSTEM','SYS','APPQOSSYS', 'FLOWS_FILES', 'JWT', 'ORDDATA', 'OWBSYS', 'OWBSYS_AUDIT', 'SCOTT', 'SPATIAL_CSW_ADMIN_USR', 'SPATIAL_WFS_ADMIN_USR', 'XS$NULL', 'YUNQU') and username not like 'APEX%'\n                            order by username", 
     'db2':'\n        select rtrim(schemaname) username from syscat.schemata order by schemaname', 
     'sqlserver':'\n        SELECT NAME [USERNAME] FROM main.dbo.sysdatabases'}
    flag, result = run_sql(database, schema_query.get(database.db_type))
    if not flag:
        return []
    else:
        schema_list = []
        for schema in result:
            schema_list.append(schema['USERNAME'])

        return schema_list
# okay decompiling ./restful/hawkeye/api/v1/sqlaudit/services/initialService.pyc
