# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/sqlaudit/services/oracleAnalysisService.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 8925 bytes
from celery.utils.log import get_task_logger
from django.db.models import Q
from api.v1.monitor.services.runsqlService import run_batch_sql
from api.v1.sqlaudit.services.buildqueryService import build_total_query, build_rule_query
from api.v1.sqlaudit.services.buildresultService import collect_sql_text, build_audit_result
from sqlaudit.enum.oracle_detail_template_enum import DetailTemplateJson
from sqlaudit.enum.oracle_problem_template_enum import ProblemTemplateJSON
from sqlaudit.enum.total_template_enum import TotalTemplateJSON
from sqlaudit.enum.static_oracle_function_enum import *
import sqlparse
from sqlaudit.models import Audit_Rule, Audit_Schema, Audit_SQL_Result
from collections import defaultdict
from api.v1.sqlaudit.services.buildresultService import build_static_result
from api.v1.sqlaudit.services.buildqueryService import build_static_rule_query
from sqlaudit.enum.static_sql_enum import StaticSQLJson
from api.v1.monitor.services.runsqlService import run_rule_sql
from common.util import build_exception_from_java, gen_sql_id, get_10s_time_str
from api.v1.monitor.services.sqldetail.common import get_default_sql_detail_format
logger = get_task_logger(__name__)

def oracle_analysis(audit_job):
    try:
        schema, max_rows, order_by_pred = audit_job.schema, audit_job.max_rows, audit_job.order_by
        rule_list = []
        database = audit_job.database
        strategy_dict = audit_job.strategy
        audit_rule_queryset = ((Audit_Rule.objects.filter(database=database)).filter(enabled=True)).filter(is_static_rule=False)
        for k, v in strategy_dict.items():
            rule_list += list((audit_rule_queryset.filter(audit_type=k)).filter(target__in=v))

        logger.error('sql_audit_analysis begin build query')
        query_total_json = build_total_query(TotalTemplateJSON.get(database.db_type), database, schema)
        query_detail_json = {}
        query_problem_json = {}
        for rule in set(rule_list):
            query_detail_json[rule.name] = build_rule_query(DetailTemplateJson, database, rule, schema, max_rows, order_by_pred)
            query_problem_json[rule.name] = build_rule_query(ProblemTemplateJSON, database, rule, schema, max_rows, order_by_pred)

        logger.error('sql_audit_analysis begin run total')
        flag, total_result = run_batch_sql(database, query_total_json)
        if not flag:
            logger.error(total_result)
            raise build_exception_from_java(total_result)
        logger.error('sql_audit_analysis begin run detail')
        flag, detail_result = run_batch_sql(database, query_detail_json)
        if not flag:
            logger.error(detail_result)
            raise build_exception_from_java(detail_result)
        logger.error('sql_audit_analysis begin run problem')
        flag, problem_result = run_batch_sql(database, query_problem_json)
        if not flag:
            logger.error(problem_result)
            raise build_exception_from_java(problem_result)
        logger.error('sql_audit_analysis begin build result')
        return build_audit_result(database, rule_list, total_result, problem_result, detail_result, audit_job)
    except Exception as e:
        logger.error(str(e))


def oracle_static_analysis(audit_job):
    try:
        database = audit_job.database
        schema_object = ((Audit_Schema.objects.filter(database=database)).filter(username=audit_job.schema)).first()
        schema = schema_object.username
        password = schema_object.get_password()
        content_object = audit_job.audit_static_content_set.all()
        if content_object:
            content_object = content_object[0]
            sql_string = content_object.content
        else:
            logger.error('content is not exist')
            return
        sql_list = sqlparse.split(sql_string)
        audit_result = {}
        rule_detail_result = defaultdict(list)
        total = len(sql_list)
        new_sql_list = [preprocess_sqltext(sql) for sql in sql_list]
        print(sql_list)
        print(new_sql_list)
        rule_list = Audit_Rule.objects.filter((Q(database=database)) & (Q(enabled=True)) & (Q(is_static_rule=True)))
        for idx, sql in enumerate(new_sql_list):
            sql_type, object_type = get_type(sql)
            target_rule_list = Audit_Rule.objects.none()
            if sql_type in ('CREATE', 'ALTER'):
                target_rule_list = ((rule_list.filter(audit_type__contains=sql_type)).filter(target__contains=object_type)).filter(database=database)
            else:
                if sql_type in ('TRUNCATE', 'DROP'):
                    target_rule_list = (rule_list.filter(audit_type__contains=sql_type)).filter(database=database)
            sqltext_rule_list = (rule_list.filter(audit_type='SQL')).filter(target='SQL')
            target_rule_list = target_rule_list | sqltext_rule_list
            for rule in target_rule_list:
                if 'NAMING' in rule.template:
                    rule.predicate = rule.predicate.replace('_', '\\_')
                predicate = rule.predicate
                template = rule.template
                if template == 'WITH_HINT':
                    sql = sql_list[idx]
                func_str = f'''{template}(sql, predicate, schema, database)'''
                flag, message = eval(func_str)
                if flag:
                    if message:
                        rule_detail_result[rule.name].append({'sql_text':sql,  'MESSAGE':message})
                    else:
                        rule_detail_result[rule.name].append({'sql_text': sql})

        plan_rule_list = ((((Audit_Rule.objects.filter(database=database)).filter(enabled=True)).filter(is_static_rule=True)).filter(audit_type='SQL')).filter(target='')
        static_plan_json = {}
        for rule in plan_rule_list:
            static_plan_json[rule.name] = build_static_rule_query(StaticSQLJson, rule)

        plan_keys = 'plans'
        static_plan_json[plan_keys] = StaticSQLJson.get(plan_keys).get('sql')
        static_result = []
        error_statements = []
        for sql in new_sql_list:
            flag, rule_json = run_rule_sql(database, schema, password, sql, static_plan_json)
            audit_sql_result = Audit_SQL_Result()
            audit_sql_result.sql_id = gen_sql_id(sql)
            if not flag:
                audit_sql_result.detail = {'sql_text':sql, 
                 'MESSAGE':str(build_exception_from_java(rule_json))}
            else:
                time_str = get_10s_time_str()
                sql_detail = get_default_sql_detail_format(database.db_type)
                sql_detail['sql_text'] = sql
                plan_dic = {}
                plan_dic[time_str] = rule_json.get(plan_keys)
                sql_detail[plan_keys]['data'] = plan_dic
                rule_json.pop(plan_keys)
                sql_detail['audit'] = {k:v for k, v in rule_json.items() if v}
                audit_sql_result.detail = sql_detail
            audit_sql_result.job = audit_job
            audit_sql_result.save()
            detail_id = str(audit_sql_result.id)
            detail_name = detail_id
            if not flag:
                error_statements.append({'sql_text':sql,  'detail_id':detail_id, 
                 'detail_name':detail_name, 
                 'MESSAGE':str(build_exception_from_java(rule_json))})
            else:
                static_result.append({'sql_text':sql, 
                 'detail_id':detail_id, 
                 'detail_name':detail_name, 
                 'data':rule_json})

        for x in static_result:
            sql_text = x.get('sql_text')
            data = x.get('data')
            detail_id = x.get('detail_id')
            detail_name = x.get('detail_name')
            for k, v in data.items():
                if v:
                    rule_detail_result[k].append({'sql_text':sql_text, 
                     'detail':v, 
                     'detail_id':detail_id, 
                     'detail_name':detail_name})

        rule_detail_result['SQL'] = error_statements
        audit_result = build_static_result(database, total, rule_detail_result, audit_job)
        return audit_result
    except Exception as e:
        print(str(e))
        logger.error(str(e))


if __name__ == '__main__':
    sql1 = 'create sequence s1 cache 20'
    from monitor.models import Database
    ora = Database.objects.get(pk='aa4beaf6-7bb0-4cd0-b38f-9b1a9e69cdcf')
    schema = 'sid'
    print(static_analysis(ora, schema, sql1))
# okay decompiling ./restful/hawkeye/api/v1/sqlaudit/services/oracleAnalysisService.pyc
