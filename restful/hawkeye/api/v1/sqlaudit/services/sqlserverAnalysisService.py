# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/sqlaudit/services/sqlserverAnalysisService.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 3994 bytes
from celery.utils.log import get_task_logger
from django.db.models import Q, Count
from monitor.models import DB2_ASH
from api.v1.monitor.services.runsqlService import run_batch_sql, get_sql_plan
from api.v1.sqlaudit.services.buildqueryService import build_total_query, build_rule_query
from api.v1.sqlaudit.services.buildresultService import build_audit_result
from sqlaudit.enum.sqlserver_detail_template_enum import DetailTemplateJson
from sqlaudit.enum.sqlserver_problem_template_enum import ProblemTemplateJSON
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

def sqlserver_analysis(audit_job):
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
        flag, total_result = run_batch_sql(database, query_total_json, schema)
        if not flag:
            logger.error(total_result)
            raise build_exception_from_java(total_result)
        logger.error('sql_audit_analysis begin run detail')
        flag, detail_result = run_batch_sql(database, query_detail_json, schema)
        if not flag:
            logger.error(detail_result)
            raise build_exception_from_java(detail_result)
        logger.error('sql_audit_analysis begin run problem')
        flag, problem_result = run_batch_sql(database, query_problem_json, schema)
        if not flag:
            logger.error(problem_result)
            raise build_exception_from_java(problem_result)
        logger.error('sql_audit_analysis begin build result')
        return build_audit_result(database, rule_list, total_result, problem_result, detail_result, audit_job)
    except Exception as e:
        logger.error(str(e))


if __name__ == '__main__':
    sql1 = 'create sequence s1 cache 20'
    from monitor.models import Database
    ora = Database.objects.get(pk='aa4beaf6-7bb0-4cd0-b38f-9b1a9e69cdcf')
    schema = 'sid'
    print(db2_static_analysis(ora, schema, sql1))
# okay decompiling ./restful/hawkeye/api/v1/sqlaudit/services/sqlserverAnalysisService.pyc
