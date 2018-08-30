# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/sqlaudit/model_views.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 21616 bytes
from django.db import transaction
from django.db.models import Q, Avg
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework_bulk import BulkModelViewSet
from api.tasks import sql_audit_analysis
from api.v1.monitor.serializers import DatabaseSerializer
from api.v1.sqlaudit.filtersets import default_filterset, Audit_JobFilterSet, Optimization_JobFilterSet, Audit_SQL_ResultFilterSet, SQL_Perf_DiffFilterSet
from api.v1.sqlaudit.serializers import default_serializer, Audit_JobSerializer, Audit_ResultSerializer, Audit_RuleSerializer, Audit_SQL_ResultSerializer, Optimization_JobSerializer, Audit_SchemaSerializer, SQL_Perf_Diff_Serializer
from sqlaudit.models import Audit_Strategy, Audit_Rule, Optimization_Job, Audit_Job, Audit_Result, Audit_SQL_Result, Audit_Schema, SQL_Perf_Diff
import pdfkit, datetime
from api.v1.monitor.services.sqldetailService import get_sql_detail
from api.v1.monitor.services.schemaService import object_detail
import uuid
from api.v1.monitor.services.activityService import get_sql_perf

class Audit_StrategyViewSet(BulkModelViewSet):
    queryset = Audit_Strategy.objects.all()
    serializer_class = default_serializer(Audit_Strategy)
    filter_class = default_filterset(Audit_Strategy)

    @list_route(methods=[
     'get'],
      url_path='config')
    def config(self, request):
        database = request.query_params['database']
        strategy_list = Audit_Strategy.objects.filter((Q(database=database)) & (Q(enabled=True))).values_list('audit_type', 'target')
        result = {}
        for strategy in strategy_list:
            if strategy[0] in result:
                result[strategy[0]].append(strategy[1])
            else:
                result[strategy[0]] = [
                 strategy[1]]

        return Response(result, status=status.HTTP_200_OK)


class Audit_RuleViewSet(BulkModelViewSet):
    queryset = Audit_Rule.objects.all()
    serializer_class = Audit_RuleSerializer
    filter_class = default_filterset(Audit_Rule)


class Audit_JobViewSet(BulkModelViewSet):
    queryset = Audit_Job.objects.all()
    serializer_class = Audit_JobSerializer
    filter_class = Audit_JobFilterSet

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        task = instance.task
        self.perform_destroy(instance)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @list_route(methods=[
     'POST'],
      url_path='create-static-audit')
    def create_static_audit(self, request):
        content = request.data.get('content', None)
        request.data['is_static_job'] = True
        schema_name = (Audit_Schema.objects.get(pk=request.data.get('schema'))).username
        request.data['schema'] = schema_name
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        headers = self.get_success_headers(serializer.data)
        (instance.audit_static_content_set.create(content=content)).save()
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @detail_route(methods=[
     'POST'],
      url_path='disable')
    @transaction.atomic
    def cancel(self, request, *args, **kwargs):
        audit_job = self.get_object()
        task = audit_job.task
        task.enabled = False
        task.save()
        audit_job.status = 4
        audit_job.save()
        return Response(status=status.HTTP_200_OK)

    @detail_route(methods=[
     'POST'],
      url_path='enable')
    @transaction.atomic
    def enable(self, request, *args, **kwargs):
        audit_job = self.get_object()
        task = audit_job.task
        task.enabled = True
        task.save()
        audit_job.status = 1
        audit_job.save()
        return Response(status=status.HTTP_200_OK)

    @detail_route(methods=[
     'GET'],
      url_path='report')
    def get_audit_report(self, request, *args, **kwargs):
        audit_job = self.get_object()
        report_data = get_report_by_audit(audit_job)
        return Response(report_data, status=status.HTTP_200_OK)

    @detail_route(methods=[
     'GET'],
      url_path='download-report')
    def download_report(self, request, *args, **kwargs):
        audit_job = self.get_object()
        report_data = get_report_by_audit(audit_job)
        options = {'page-size':'A4', 
         'margin-top':'0.75in', 
         'margin-right':'0.75in', 
         'margin-bottom':'0.75in', 
         'margin-left':'0.75in', 
         'encoding':'UTF-8'}
        trs = ''
        details = ''
        conclusion = report_data.get('conclusion', '')
        data_list = report_data.get('data', '')
        for data in data_list:
            name = ''
            if data.get('result'):
                name = f'''href="#{(data.get('name'))}"'''
            trs += f'''
            
                    <tr>
                        <td style="text-align:center;">
                            {(data.get('audit_type', ''))}<br />
                        </td>
                        <td style="text-align:center;">
                            {(data.get('target', ''))}<br />
                        </td>
                        <td style="text-align:center;">
                            <a {name}>{(data.get('name', ''))}</a><br />
                        </td>
                        <td style="text-align:center;">
                            {(data.get('score', ''))}<br />
                        </td>
                        <td style="text-align:center;">
                            {(data.get('problem', ''))}<br />
                        </td>
                        <td style="text-align:center;">
                            {(data.get('total', ''))}<br />
                        </td>
                        <td style="text-align:center;">
                            {(data.get('problem_rate', ''))}%<br />
                        </td>
                    </tr>        
            '''
            detail_head = ''
            detail_tr = ''
            for result in data.get('result', []):
                detail_td = ''
                head_td = ''
                for k, v in result.items():
                    head_td += f'''
                            <td style="text-align:center;">
                            {k}<br />
                            </td>
                            '''
                    detail_head = f'''
                                <tr>
                                    {head_td}
                                </tr>
                            '''
                    detail_td += f'''
                            <td style="text-align:center;">
                            {v}
                            </td>
                            '''

                detail_tr += f'''
                            <tr>
                                {detail_td}
                            </tr>
                            '''

            if data.get('result'):
                details += f'''
                    <div id="{(data.get('name', ''))}">
                        <span style="font-size:18px;">{(data.get('name', ''))}:</span></br>
                        <table cellpadding="2" cellspacing="0" border="1" bordercolor="#000000">
                            <tbody>
                                {detail_head}
                                {detail_tr}
                            </tbody>
                        </table>
                        </br></br>
                    </div>
                    '''

        html = f'''
                    <p>
                        <span><br />
                        <h1 style="text-align:center;">
                            <span style="color:#000000;font-family:SimSun;">{(audit_job.name)}</span>
                        </h1>
                        <p>
                            <span style="color:#000000;font-family:SimSun;"><br />
                    </span>
                        </p>
                        <p>
                            <span style="color:#000000;font-family:SimSun;"><br />
                    </span>
                        </p>
                    </span><span><span style="font-size:18px;">:</span></span>
                    </p>
                    <p>
                        <span>
                    <pre>{conclusion}</pre>
                        <div class="ant-table-wrapper _3HTnYrvUcsaZCJOoIk5Wqr" style="margin:1rem 0px 0px;padding:0px;color:rgba(0, 0, 0, 0.65);font-family:&quot;background-color:#FFFFFF;">
                            <div class="ant-spin-nested-loading" style="margin:0px;padding:0px;">
                                <div class="ant-spin-container" style="margin:0px;padding:0px;">
                                    <div class="ant-table ant-table-small ant-table-bordered ant-table-scroll-position-left" style="margin:0px;padding:0px;">
                                        <div class="ant-table-content" style="margin:0px;padding:0px;">
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    <br />
                    <span style="font-size:18px;">:</span></span>
                    </p>
                    <p>
                        <br />
                    </p>
                    <p>
                        <table style="width:100%;" cellpadding="2" cellspacing="0" border="1" bordercolor="#000000" align="center">
                            <tbody>
                                <tr>
                                    <td style="text-align:center;">
                                        <span style="background-color:;"></span><br />
                                    </td>
                                    <td style="text-align:center;">
                                        <span style="color:rgba(0, 0, 0, 0.85);font-family:&quot;background-color:#FFFFFF;">target</span><br />
                                    </td>
                                    <td style="text-align:center;">
                                        
                                    </td>
                                    <td style="text-align:center;">
                                        
                                    </td>
                                    <td style="text-align:center;">
                                        
                                    </td>
                                    <td style="text-align:center;">
                                        
                                    </td>
                                    <td style="text-align:center;">
                                        
                                    </td>
                                </tr>
                                {trs}
                            </tbody>
                        </table>
                    </p>
                    <br />
                    <br />  
                    {details}
      '''
        pdf = pdfkit.from_string(html, False, options=options)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="yunquReport.pdf"'
        response.write(pdf)
        return response

    @detail_route(methods=[
     'GET'],
      url_path='analysis')
    def analysis_from_post(self, request, *args, **kwargs):
        audit_job = self.get_object()
        if audit_job.status == 3:
            return Response({'message': ','}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if not audit_job.strategy:
                if not audit_job.is_static_job:
                    return Response({'message': ''}, status=status.HTTP_400_BAD_REQUEST)
                sql_audit_analysis.delay(audit_job.id)
            return Response(status=status.HTTP_200_OK)

    @detail_route(methods=[
     'GET'],
      url_path='problem-sql-list')
    def get_problem_sql(self, request, *args, **kwargs):
        audit_job = self.get_object()
        query_set = Audit_SQL_Result.objects.filter(audit_job=audit_job)
        serializer = Audit_SQL_ResultSerializer(query_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def get_report_by_audit(audit_job):
    queryset = Audit_Result.objects.filter(job=audit_job)
    serializer = Audit_ResultSerializer(queryset, many=True)
    score_list = queryset.values_list('score', 'target')
    strategy = audit_job.strategy if audit_job.strategy else {}
    rule_list = []
    for k, v in strategy.items():
        rule_list += v

    problem_str = ''
    for target in set(rule_list):
        num = sum((queryset.filter(target=target)).values_list('problem', flat=True))
        problem_str += f'''{num}{target},'''

    if not score_list:
        score = None
        conclusion = None
    else:
        score_list = calculate_target_avg_score(queryset)
        score = calculate_report_score(queryset)
        begin_time = audit_job.begin_time.strftime('%Y-%m-%d:%H:%M:%S')
        conclusion = f'''{(audit_job.database.db_name)},{begin_time},{score},{(len(queryset))},:{problem_str}'''
    report_data = {'database':DatabaseSerializer(audit_job.database).data,  'total_score':score, 
     'score_list':score_list, 
     'conclusion':conclusion, 
     'data':serializer.data}
    return report_data


def calculate_report_score(queryset):
    score_weight_set = queryset.values_list('score', 'rule_weight')
    if not score_weight_set:
        return 0
    else:
        score_sum = 0
        weight_sum = 0
        for score_weight in score_weight_set:
            score_sum += score_weight[0] * score_weight[1]
            weight_sum += score_weight[1]

        return round(score_sum / weight_sum, 2)


def calculate_target_avg_score(queryset):
    target_score_list = queryset.values('target').annotate(Avg('score')).values_list('score__avg', 'target')
    return list(target_score_list)


class Optimization_JobViewSet(BulkModelViewSet):
    queryset = Optimization_Job.objects.all()
    serializer_class = Optimization_JobSerializer
    filter_class = Optimization_JobFilterSet

    @list_route(methods=[
     'POST'],
      url_path='bulk-create')
    def bulk_create(self, request, *args, **kwargs):
        problem_set = request.data.get('problem_set')
        name = request.data.get('name')
        deadline = request.data.get('deadline')
        owner = request.data.get('owner')
        audit_job = request.data.get('audit_job')
        job = Audit_Job.objects.get(pk=audit_job)
        database = job.database
        schema = job.schema
        job_list = []
        for problem_id in problem_set:
            sql_id = problem_id.get('SQL_ID', None)
            detail_id = problem_id.get('detail_id', None)
            sql_detail = (Audit_SQL_Result.objects.get(pk=detail_id)).detail
            if sql_detail.get('sql_text') != None:
                is_sql_detail = True if sql_detail.get('audit') != None else False
                target = 'object'
                if sql_id or is_sql_detail:
                    target = 'sql'
                optimization_job = Optimization_Job(detail_name=problem_id.get('detail_name', None),
                  detail_id=detail_id,
                  name=name,
                  status=1,
                  audit_job_id=audit_job,
                  database=database,
                  owner_id=owner,
                  deadline=deadline,
                  schema=schema,
                  target=target)
                job_list.append(optimization_job)

        Optimization_Job.objects.bulk_create(job_list)
        return Response(status=status.HTTP_200_OK)

    @list_route(methods=[
     'POST'],
      url_path='bulk-finish')
    def bulk_finish(self, request, *args, **kwargs):
        job_list = request.data.get('job_list', [])
        optimize_description = request.data.get('optimize_description', '')
        (Optimization_Job.objects.filter(id__in=job_list)).update(status=2, optimize_description=optimize_description, closed_at=datetime.datetime.now())
        return Response(status=status.HTTP_200_OK)

    @detail_route(methods=[
     'GET'],
      url_path='cancel')
    def cancel(self, request, *args, **kwargs):
        optimization_job = self.get_object()
        optimization_job.status = 3
        optimization_job.save()
        return Response(status=status.HTTP_200_OK)

    @detail_route(methods=[
     'POST'],
      url_path='finish')
    def finish(self, request, *args, **kwargs):
        optimization_job = self.get_object()
        optimize_description = request.data.get('optimize_description', '')
        optimized_sql_text = request.data.get('optimized_sql_text', '')
        optimized_sql_id = request.data.get('optimized_sql_id', '')
        schema = request.data.get('schema', '')
        object_name = request.data.get('object', '')
        detail_name = ''
        detail_data = {}
        if optimized_sql_id:
            detail_data = get_sql_detail(str(optimization_job.database.id), optimized_sql_id, time_span='realtime', cache=False)
            detail_name = optimized_sql_id
        else:
            if optimized_sql_text:
                detail_data = {'sql_text': optimized_sql_text}
            else:
                detail_data = object_detail(str(optimization_job.database.id), schema, object_name)
                detail_name = ('{}.{}').format(schema, object_name)
            audit_sql_result = Audit_SQL_Result()
            audit_sql_result.sql_id = detail_name
            audit_sql_result.detail = detail_data
            audit_sql_result.job = optimization_job.audit_job
            audit_sql_result.save()
            detail_id = str(audit_sql_result.id)
            closed_at = datetime.datetime.now()
            optimization_job.optimize_description = optimize_description
            optimization_job.optimized_detail_id = detail_id
            optimization_job.optimized_detail_name = detail_name
            optimization_job.closed_at = closed_at
            optimization_job.status = 2
            optimization_job.save()
            return Response(status=status.HTTP_200_OK)


class Audit_SQL_ResultViewSet(BulkModelViewSet):
    queryset = Audit_SQL_Result.objects.all()
    serializer_class = default_serializer(Audit_SQL_Result)
    filter_class = Audit_SQL_ResultFilterSet

    @list_route(methods=[
     'GET'],
      url_path='detail')
    def detail(self, request, *args, **kwargs):
        detail_id = request.query_params.get('detail_id')
        job = request.query_params.get('job')
        audit_sql_result_set = Audit_SQL_Result.objects.filter((Q(id=detail_id)) & (Q(job_id=job)))
        audit_sql_result = audit_sql_result_set[0] if audit_sql_result_set else {}
        data = audit_sql_result.detail if hasattr(audit_sql_result, 'detail') else {}
        return Response(data, status=status.HTTP_200_OK)


class Audit_SchemaViewSet(BulkModelViewSet):
    queryset = Audit_Schema.objects.all()
    serializer_class = Audit_SchemaSerializer
    filter_class = default_filterset(Audit_Schema)


class SQL_Perf_Diff_ViewSet(BulkModelViewSet):
    queryset = SQL_Perf_Diff.objects.all()
    serializer_class = SQL_Perf_Diff_Serializer
    filter_class = SQL_Perf_DiffFilterSet

    @detail_route(methods=[
     'POST'],
      url_path='capture-sql-perf')
    @transaction.atomic
    def capture_sql_perf(self, request, *args, **kwargs):
        sql_perf_diff = self.get_object()
        db = sql_perf_diff.database
        pk = db.pk
        sql_id_list = sql_perf_diff.sql_id_list
        sql_perf_diff.end_result = get_sql_perf(pk, sql_id_list)
        summary_result = {}
        begin_result = sql_perf_diff.begin_result
        end_result = sql_perf_diff.end_result
        for x in begin_result:
            sql_id = x.get('sql_id')
            begin_elapse_time = x.get('()')
            end_elapse_time = None
            for y in end_result:
                if sql_id == y.get('sql_id'):
                    end_elapse_time = y.get('()')

            if end_elapse_time:
                summary_result[sql_id] = begin_elapse_time and (begin_elapse_time - end_elapse_time) / begin_elapse_time

        sql_perf_diff.summary_result = summary_result
        sql_perf_diff.snapshot_end_time = datetime.datetime.now()
        sql_perf_diff.save()
        return Response(status=status.HTTP_200_OK)

    @detail_route(methods=[
     'GET'],
      url_path='report')
    def get_sql_perf_diff_report(self, request, *args, **kwargs):
        audit_job = self.get_object()
        report_data = {}
        return Response({}, status=status.HTTP_200_OK)
# okay decompiling ./restful/hawkeye/api/v1/sqlaudit/model_views.pyc
