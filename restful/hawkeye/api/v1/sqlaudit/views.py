# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/sqlaudit/views.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 7962 bytes
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from api.v1.monitor.services.runsqlService import run_batch_sql
from api.v1.sqlaudit.serializers import Optimization_JobSerializer
from api.v1.sqlaudit.services.initialService import get_database_schema_list
from monitor.models import Database
from sqlaudit.models import Audit_Rule, Audit_Job, Audit_Result, Optimization_Job
from api.v1.sqlaudit.services.buildqueryService import build_rule_query, build_total_query
from api.v1.sqlaudit.services.buildresultService import build_audit_result, collect_sql_text
from common.util import build_exception_from_java, execute_return_json
from sqlaudit.enum.total_template_enum import TotalTemplateJSON
from sqlaudit.enum.oracle_detail_template_enum import DetailTemplateJson
from sqlaudit.enum.oracle_problem_template_enum import ProblemTemplateJSON
import sqlparse, datetime

@api_view(['POST'])
def analysis_from_post(request):
    database_id = request.data.get('database_id')
    schema = request.data.get('schema', None)
    max_rows = request.data.get('max_rows', None)
    order_by_pred = request.data.get('order_by_pred', '')
    audit_result = {}
    try:
        database = Database.objects.get(pk=database_id)
        rule_list = ((Audit_Rule.objects.filter(database=database)).filter(enabled=True)).filter(is_static_rule=False)
        query_total_json = build_total_query(TotalTemplateJSON, database, schema)
        query_detail_json = {}
        query_problem_json = {}
        for rule in rule_list:
            query_detail_json[rule.name] = build_rule_query(DetailTemplateJson, database, rule, schema, max_rows, order_by_pred)
            query_problem_json[rule.name] = build_rule_query(ProblemTemplateJSON, database, rule, schema, max_rows, order_by_pred)

        flag, detail_result = run_batch_sql(database, query_detail_json)
        if not flag:
            raise build_exception_from_java(detail_result)
        flag, problem_result = run_batch_sql(database, query_problem_json)
        if not flag:
            raise build_exception_from_java(problem_result)
        flag, total_result = run_batch_sql(database, query_total_json)
        if not flag:
            raise build_exception_from_java(total_result)
        audit_result = build_audit_result(database, rule_list, total_result, problem_result, detail_result, None)
        collect_sql_text(database, schema)
        return Response(audit_result, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({'error_message': ''}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_schema_list(request):
    database_id = request.query_params['database']
    try:
        database = Database.objects.get(pk=database_id)
    except Exception as e:
        print(str(e))
        return Response(status=status.HTTP_400_BAD_REQUEST)

    schema_list = get_database_schema_list(database)
    return Response(schema_list, status=status.HTTP_200_OK)


@api_view(['POST'])
def sql_format(request):
    sql = request.data.get('sql', None)
    if not sql:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        formatted_sql = sqlparse.format(sql, reindent=True)
        return Response(formatted_sql, status=status.HTTP_200_OK)


@api_view(['get'])
def index(request):
    score_list = (Audit_Job.objects.filter(status=3)).order_by('created_at').values_list('database__alias', 'created_at', 'total_score', 'database__id')
    latest_exec = (Audit_Job.objects.filter(status=3)).latest('finish_at').finish_at if (Audit_Job.objects.filter(status=3)) else None
    latest_exec_time = latest_exec.strftime('%Y-%m-%d %H:%M:%S') if latest_exec else ''
    final_score_dict = {}
    count_list = []
    for score in score_list:
        score = list(score)
        if score[2]:
            score[2] = round(score[2], 2)
        if score[1]:
            if type(score[1]) == datetime.datetime:
                score[1] = int(score[1].timestamp())
        if score[0] in final_score_dict:
            final_score_dict[score[0]].append(score[1:3])
        else:
            final_score_dict[score[0]] = [
             score[1:3]]

    query_result = execute_return_json('SELECT database_id,(SELECT alias From monitor_database WHERE id = database_id),count(database_id) FROM sqlaudit_audit_job GROUP BY database_id;')
    for _result in query_result:
        count_list.append({'database_alias':_result.get('alias') or _result.get('ALIAS'), 
         'database_id':_result.get('database_id') or _result.get('DATABASE_ID'), 
         'count':_result.get('count') or _result.get('COUNT')})

    data = {'score_dict':final_score_dict, 
     'latest_exec_time':latest_exec_time, 
     'count_list':count_list}
    return Response(data, status=status.HTTP_200_OK)


@api_view(['get'])
def audit_compare_index(request):
    database_id = request.query_params['database'] or request.query_params['database_id']
    database = Database.objects.get(pk=database_id)
    score_list = list(Audit_Job.objects.filter((Q(status=3)) & (Q(database_id=database_id)) & (Q(is_static_job=False))).order_by('created_at').values_list('created_at', 'total_score'))
    final_score_list = []
    for score in score_list:
        score = list(score)
        if score[0]:
            if type(score[0]) == datetime.datetime:
                score[0] = int(score[0].timestamp())
                score[1] = round(score[1], 2)
        final_score_list.append(score)

    data = {'database_alias':database.alias,  'single_database_score':final_score_list}
    return Response(data, status=status.HTTP_200_OK)


@api_view(['post'])
def audit_compare(request):
    audit_1_id = request.data.get('audit_1_id', None)
    audit_2_id = request.data.get('audit_2_id', None)
    try:
        audit_1 = Audit_Job.objects.get(pk=audit_1_id)
        audit_2 = Audit_Job.objects.get(pk=audit_2_id)
    except ObjectDoesNotExist:
        return Response({'error_message': ''}, status=status.HTTP_400_BAD_REQUEST)

    data = compare_audit(audit_1, audit_2)
    return Response(data, status=status.HTTP_200_OK)


def compare_audit(audit_1, audit_2):
    if not audit_1 or not audit_2:
        return {}
    else:
        start_score = audit_1.total_score
        end_score = audit_2.total_score
        improvement_rate = round(end_score - start_score, 2)
        audit_1_result_set = Audit_Result.objects.filter(job=audit_1)
        audit_2_result_set = Audit_Result.objects.filter(job=audit_2)
        final_result_list = []
        final_result_detail_list = []
        for audit_1_result in audit_1_result_set:
            if audit_2_result_set.filter(name=audit_1_result.name):
                audit_2_result = (audit_2_result_set.filter(name=audit_1_result.name))[0]
            result_improvement_rate = round(audit_2_result.score - audit_1_result.score, 2)
            result = [
             audit_1_result.name, audit_1_result.score, audit_2_result.score, result_improvement_rate]
            final_result_list.append(result)

        opt_job_query_set = Optimization_Job.objects.filter(audit_job=audit_1)
        data = {'start_score':start_score, 
         'end_score':end_score, 
         'improvement_rate':improvement_rate, 
         'final_result_list':final_result_list, 
         'optimization_job':Optimization_JobSerializer(opt_job_query_set, many=True).data}
        return data
# okay decompiling ./restful/hawkeye/api/v1/sqlaudit/views.pyc
