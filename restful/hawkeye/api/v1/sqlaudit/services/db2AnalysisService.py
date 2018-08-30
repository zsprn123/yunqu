# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/sqlaudit/services/db2AnalysisService.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 9527 bytes
from celery.utils.log import get_task_logger
from django.db.models import Q, Count
from monitor.models import DB2_ASH
from api.v1.monitor.services.runsqlService import run_batch_sql, get_sql_plan
from api.v1.sqlaudit.services.buildqueryService import build_total_query, build_rule_query
from api.v1.sqlaudit.services.buildresultService import build_audit_result
from sqlaudit.enum.db2_detail_template_enum import DetailTemplateJson
from sqlaudit.enum.db2_problem_template_enum import ProblemTemplateJSON
from sqlaudit.enum.total_template_enum import TotalTemplateJSON
import sqlparse
from sqlaudit.models import Audit_Rule, Audit_Schema, Audit_SQL_Result
from collections import defaultdict
from common.util import build_exception_from_java, gen_sql_id, get_10s_time_str
from api.v1.monitor.services.sqldetail.common import get_default_sql_detail_format
from api.enum.sql_audit_enum import get_db2_single_sql_plan_audit, get_db2_single_sql_text_audit, get_db2_sql_audit
from datetime import datetime, timedelta
from api.v1.sqlaudit.services.buildresultService import build_static_result
logger = get_task_logger(__name__)
MAX_SQL_LIMIT = 1000

def db2_analysis(audit_job):
    try:
        schema, max_rows, order_by_pred, time_span = (
         audit_job.schema, audit_job.max_rows, audit_job.order_by, audit_job.time_span)
        if time_span:
            begin_time, end_time = datetime.now(), datetime.now() - (timedelta(hours=1))
        else:
            begin_time, end_time = audit_job.snapshot_begin_time, audit_job.snapshot_end_time
        rule_list = []
        database = audit_job.database
        strategy_dict = audit_job.strategy
        audit_rule_queryset = (Audit_Rule.objects.filter(database=database)).filter(enabled=True)
        for k, v in strategy_dict.items():
            rule_list += list((audit_rule_queryset.filter(audit_type=k)).filter(target__in=v))

        logger.error('sql_audit_analysis begin build query')
        query_total_json = build_total_query(TotalTemplateJSON.get(database.db_type), database, schema)
        query_detail_json = {}
        query_problem_json = {}
        object_rules_list = [rule for rule in rule_list if rule.audit_type == '']
        for rule in set(object_rules_list):
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
        sql_list = ((((DB2_ASH.objects.filter(database=database)).filter(created_at__range=(begin_time, end_time))).filter(db_name__in=schema.split(','))).values('sql_id', 'sql_text', 'db_name').annotate(total=Count('sql_id'))).order_by('-total')[:MAX_SQL_LIMIT]
        sql_count = sql_list.count()
        sql_rules_list = [rule for rule in rule_list if rule.audit_type == 'SQL']
        for rule in sql_rules_list:
            total_result[rule.target] = [
             {'COUNT': sql_count}]
            problem_result[rule.name] = [{'COUNT': 0}]

        for x in sql_list:
            sql_id = x.get('sql_id')
            sql_text = x.get('sql_text')
            sql_schema = x.get('db_name')
            if sql_id:
                if sql_text:
                    flag, json_data = get_sql_plan(database, sql_text, sql_schema)
                    if not flag:
                        print(sql_text)
                        print(str(build_exception_from_java(json_data)))
            if json_data:
                try:
                    plan_audit_data = get_db2_single_sql_plan_audit(database, sql_text, json_data)
                    text_audit_data = get_db2_single_sql_text_audit(database, sql_text, json_data)
                    audit_data = {**plan_audit_data, **text_audit_data}
                    for k, v in plan_audit_data.items():
                        if not detail_result.get(k):
                            detail_result[k] = []
                        detail_result[k].append({'SQL_ID':sql_id,  'SQL_TEXT':sql_text,  'SCHEMA':sql_schema})
                        current_problem_count = problem_result[k][0].get('COUNT')
                        problem_result[k] = [{'COUNT': current_problem_count + 1}]

                except Exception as e:
                    print(e)

        return build_audit_result(database, rule_list, total_result, problem_result, detail_result, audit_job)
    except Exception as e:
        logger.error(str(e))


def db2_static_analysis(audit_job):
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
        plan_keys = 'plans'
        rule_list = Audit_Rule.objects.filter((Q(database=database)) & (Q(enabled=True)))
        static_result = []
        error_statements = []
        for sql_text in sql_list:
            flag, json_data = get_sql_plan(database, sql_text, schema)
            audit_data = {}
            if not flag:
                print(sql_text)
                print(str(build_exception_from_java(json_data)))
                if not flag:
                    error_statements.append({'sql_text':sql_text,  'detail_id':gen_sql_id(sql_text), 
                     'detail_name':gen_sql_id(sql_text), 
                     'MESSAGE':str(build_exception_from_java(json_data))})
                    continue
            if json_data:
                try:
                    audit_data = get_db2_sql_audit(database, None, sql_text, json_data)
                except Exception as e:
                    print(e)

                audit_sql_result = Audit_SQL_Result()
                audit_sql_result.sql_id = gen_sql_id(sql_text)
                time_str = get_10s_time_str()
                sql_detail = get_default_sql_detail_format(database.db_type)
                sql_detail['sql_text'] = sql_text
                plan_dic = {}
                plan_dic[time_str] = json_data
                sql_detail[plan_keys]['data'] = plan_dic
                sql_detail['audit'] = audit_data
                audit_sql_result.detail = sql_detail
                audit_sql_result.job = audit_job
                audit_sql_result.save()
                detail_id = str(audit_sql_result.id)
                detail_name = detail_id
                static_result.append({'sql_text':sql_text, 
                 'detail_id':detail_id, 
                 'detail_name':detail_name, 
                 'data':audit_data})

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
    print(db2_static_analysis(ora, schema, sql1))
# okay decompiling ./restful/hawkeye/api/v1/sqlaudit/services/db2AnalysisService.pyc
