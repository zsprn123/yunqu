# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/sqlaudit/services/buildresultService.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 7323 bytes
from api.v1.monitor.services.sqldetailService import get_sql_detail
from api.v1.monitor.services.schemaService import object_detail
from collections import defaultdict
from sqlaudit.enum.table_stats_enum import format_table_stats
from sqlaudit.models import Audit_Result, Audit_SQL_Result
from api.v1.monitor.services.runsqlService import run_sql
from sqlaudit.enum.sql_text_emum import COLLECT_SQL_TEXT
from common.util import build_exception_from_java
from sqlaudit.models import Audit_SQL_Text
from sqlaudit.models import Audit_Rule
Object_Name = {u'\u5206\u533a':'PARTITION_NAME', 
 u'\u5b57\u6bb5':'COLUMN_NAME', 
 u'\u8868':'TABLE_NAME', 
 u'\u4e34\u65f6\u8868':'TABLE_NAME', 
 u'\u5e8f\u5217':'SEQUENCE_NAME', 
 u'\u7d22\u5f15':'INDEX_NAME', 
 u'\u5bf9\u8c61':'OBJECT_NAME', 
 u'\u5916\u952e\u7ea6\u675f':'TABLE_NAME'}
Owner_Name = {u'\u5206\u533a':'OWNER', 
 u'\u5b57\u6bb5':'OWNER', 
 u'\u8868':'OWNER', 
 u'\u4e34\u65f6\u8868':'OWNER', 
 u'\u5e8f\u5217':'SEQUENCE_OWNER', 
 u'\u7d22\u5f15':'OWNER', 
 u'\u5bf9\u8c61':'OBJECT_OWNER', 
 u'\u5916\u952e\u7ea6\u675f':'OWNER'}
Subobject_List = [
 '', '']

def build_audit_result(database, rule_list, total_result, problem_result, detail_result, audit_job):
    summary = defaultdict(lambda : defaultdict(dict))
    import sys, pprint
    sys.displayhook = pprint.pprint
    locals()
    result_list = []
    sql_list = []
    sql_id_map = {}
    object_map = defaultdict(dict)
    object_name_map = defaultdict(dict)
    for rule in rule_list:
        try:
            total = total_result.get(rule.target)[0].get('COUNT') if total_result.get(rule.target) else 0
            problem = problem_result.get(rule.name)[0].get('COUNT') if problem_result.get(rule.name) else 0
            problem_rate = round(problem / (total if total != 0 else 1) * 100)
            rule_detail_result = detail_result.get(rule.name)
            if rule.audit_type == '':
                result = format_table_stats(rule.template, rule_detail_result)
            else:
                result = rule_detail_result
            if result and rule.audit_type == 'SQL':
                for x in result:
                    sql_id = x.get('SQL_ID')
                    detail_id = sql_id_map.get(sql_id)
                    if not detail_id:
                        audit_sql_result = Audit_SQL_Result()
                        audit_sql_result.sql_id = sql_id
                        audit_sql_result.detail = get_sql_detail(database.id, sql_id, time_span='realtime', cache=False, activity=False, sql_audit=True)
                        audit_sql_result.job = audit_job
                        audit_sql_result.save()
                        detail_id = str(audit_sql_result.id)
                        sql_id_map[sql_id] = detail_id
                    x['detail_id'] = detail_id
                    x['detail_name'] = sql_id

            else:
                for x in result:
                    target = rule.target
                    name_key = Object_Name.get(target)
                    owner_key = Owner_Name.get(target)
                    owner = x.get(owner_key)
                    name = x.get(name_key)
                    detail = {}
                    key = name if target not in Subobject_List else ('{}.{}').format(x.get('TABLE_NAME'), name)
                    detail_id = object_map.get(target).get(key) if object_map.get(target) else None
                    detail_name = object_name_map.get(target).get(key) if object_name_map.get(target) else None
                    if detail_id:
                        x['detail_id'] = detail_id
                        x['detail_name'] = detail_name
                    else:
                        if target not in Subobject_List:
                            detail = object_detail(str(database.id), owner, name)
                        else:
                            table_name = x.get('TABLE_NAME')
                            detail = object_detail(str(database.id), owner, table_name, target, name)
                        audit_sql_result = Audit_SQL_Result()
                        audit_sql_result.sql_id = ('{}: {}').format(rule.name, key)
                        audit_sql_result.detail = detail
                        audit_sql_result.job = audit_job
                        audit_sql_result.save()
                        detail_id = str(audit_sql_result.id)
                        object_map[target][key] = detail_id
                        object_name_map[target][key] = audit_sql_result.sql_id
                        x['detail_id'] = detail_id
                        x['detail_name'] = audit_sql_result.sql_id

            rule_result = {'rule_weight':rule.weight,  'audit_type':rule.audit_type, 
             'name':rule.name, 
             'target':rule.target, 
             'total':total, 
             'problem':problem, 
             'problem_rate':problem_rate, 
             'score':100 - problem_rate, 
             'result':result, 
             'job':audit_job}
            summary[rule.audit_type][rule.target][rule.name] = rule_result
            result_list.append(Audit_Result(**rule_result))
        except:
            pass

    Audit_Result.objects.bulk_create(result_list)
    return summary


def collect_sql_text(database, schema):
    schema_name = COLLECT_SQL_TEXT.get('schema_name')
    instance_id_list = database.instance_id_list
    data = {'schema_pred':f'''{schema_name} in ('{schema}')''', 
     'inst_id_pred':f'''inst_id in ({instance_id_list})'''}
    query = COLLECT_SQL_TEXT.get('sql').format(**data)
    flag, result = run_sql(database, query)
    if not flag:
        raise build_exception_from_java(result)
    for x in result:
        a = Audit_SQL_Text()
        a.sql_id = x.get('SQL_ID')
        a.force_matching_signature = x.get('FORCE_MATCHING_SIGNATURE')
        a.sql_text = x.get('SQL_TEXT')
        a.save()


def build_static_result(database, total_result, detail_result, audit_job):
    audit_result = defaultdict(list)
    result_list = []
    for rule_name, result in detail_result.items():
        rule = (((Audit_Rule.objects.filter(database=database)).filter(enabled=True)).filter(name=rule_name)).first()
        if rule:
            total = total_result
            problem = len(result)
            problem_rate = round(problem / (total if total != 0 else 1) * 100)
            result = format_table_stats(rule.template, result)
            audit_result[rule_name] = result
            rule_result = {'rule_weight':rule.weight, 
             'audit_type':rule.audit_type, 
             'name':rule.name, 
             'target':rule.target, 
             'total':total, 
             'problem':problem, 
             'problem_rate':problem_rate, 
             'score':100 - problem_rate, 
             'result':result, 
             'job':audit_job}
            result_list.append(Audit_Result(**rule_result))

    Audit_Result.objects.bulk_create(result_list)
    return audit_result
# okay decompiling ./restful/hawkeye/api/v1/sqlaudit/services/buildresultService.pyc
