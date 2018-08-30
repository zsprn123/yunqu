# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/heathcheck/views.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 17345 bytes
import json
from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from api.v1.heathcheck.filtersets import Heathcheck_ReportFilterSet
from api.v1.heathcheck.rules.db2_rule import DB2_Config_Rule, DB2_Performance_Rule, DB2_Secure_Rule, DB2_Management_Rule, DB2_Backup_Rule
from api.v1.heathcheck.rules.oracle_rule import Oracle_Config_Rule, Oracle_Performance_Rule, Oracle_Secure_Rule, Oracle_Management_Rule, Oracle_Backup_Rule
from api.v1.heathcheck.rules.sqlserver_rule import SQLServer_Config_Rule, SQLServer_Performance_Rule, SQLServer_Secure_Rule, SQLServer_Management_Rule, SQLServer_Backup_Rule
from api.v1.heathcheck.serializers import Heathcheck_ReportSerializer
from common.yunquAuthorizationUtil import get_lisence_info
from heathcheck.models import Heathcheck_Report
from monitor.models import Database
from django.core.cache import cache
logger = get_task_logger(__name__)

class Heathcheck_ReportViewSet(ModelViewSet):
    queryset = Heathcheck_Report.objects.all()
    serializer_class = Heathcheck_ReportSerializer
    filter_class = Heathcheck_ReportFilterSet


@api_view(['POST'])
def gen_report(request):
    database_id = request.data.get('database_id', None)
    if not database_id:
        return Response({'message': ' database_id'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        generate_healthcheck_report(database_id)
        return Response({'message': ''}, status=status.HTTP_200_OK)


@api_view(['POST'])
def merge_healthcheck_report(request):
    database_id_list = request.data.get('database_id_list', None)
    if not database_id_list:
        return Response({'message': ''}, status=status.HTTP_400_BAD_REQUEST)
    else:
        generate_merge_report.delay(database_id_list)
        return Response({'message': ''}, status=status.HTTP_200_OK)


@shared_task(bind=True)
def generate_merge_report(self, database_id_list):
    database_list = Database.objects.filter(id__in=database_id_list)
    if not database_list:
        report = Heathcheck_Report(status_message=',:', status=3)
        report.save()
        return
    logger.info('start generate merge healthcheck report')
    merge_result = {}
    lisence_info = get_lisence_info()
    merge_summary = {'title':lisence_info.get('client_name', '') + '', 
     'summary':{'database_score_list':[],  'overview':'', 
      'score':{}}, 
     'report_list':{}}
    oracle_count = (database_list.filter(db_type='oracle')).count()
    db2_count = (database_list.filter(db_type='db2')).count()
    oracle_rules_filter = cache.get('oraclefilter_data', '')
    db2_rules_filter = cache.get('db2filter_data', '')
    oracle_filterList = oracle_rules_filter.split(';')
    db2_filterList = db2_rules_filter.split(';')
    count_str = ''
    if oracle_count != 0:
        count_str += f''' oracle {oracle_count},{(list((database_list.filter(db_type='oracle')).values_list('alias', flat=True)))} '''
    if db2_count != 0:
        count_str += f''' db2 {db2_count},{(list((database_list.filter(db_type='db2')).values_list('alias', flat=True)))} '''
    rules_count_str = ',,,,5,'
    if oracle_filterList:
        rules_count_str += f'''oracle {(sum((len(y) for y in get_rules('oracle')[1].values())) - len(oracle_filterList))},{((',').join([x for x in list(get_rules('oracle')[1].values())][0:5]))} '''
    if db2_filterList:
        rules_count_str += f'''db2 {(sum((len(y) for y in get_rules('db2')[1].values())) - len(db2_filterList))},{((',').join([x for x in list(get_rules('db2')[1].values())][0:5]))}'''
    overview = f'''{(len(database_list))},{count_str}{rules_count_str}'''
    merge_summary['summary']['overview'] = overview
    report = Heathcheck_Report(status_message='', status=2)
    report.save()
    for database in database_list:
        rules_filter = cache.get(database.db_type + 'filter_data', '')
        filterList = rules_filter.split(';')
        if database.db_type == 'oracle':
            R1, R2, R3, R4, R5 = (
             Oracle_Config_Rule, Oracle_Performance_Rule, Oracle_Secure_Rule, Oracle_Management_Rule, Oracle_Backup_Rule)
        else:
            if database.db_type == 'db2':
                R1, R2, R3, R4, R5 = (
                 DB2_Config_Rule, DB2_Performance_Rule, DB2_Secure_Rule, DB2_Management_Rule, DB2_Backup_Rule)
            else:
                if database.db_type == 'sqlserver':
                    R1, R2, R3, R4, R5 = (
                     SQLServer_Config_Rule, SQLServer_Performance_Rule, SQLServer_Secure_Rule, SQLServer_Management_Rule, SQLServer_Backup_Rule)
            config_rules = {'category':'', 
             'data':[classname(database.id, database.alias).check(database, database.version) for classname in R1.__subclasses__() if classname(database.id, database.alias).title not in filterList]}
            peformance_rules = {'category':'', 
             'data':[classname(database.id, database.alias).check(database, database.version) for classname in R2.__subclasses__() if classname(database.id, database.alias).title not in filterList]}
            secure_rules = {'category':'',  'data':[classname(database.id, database.alias).check(database, database.version) for classname in R3.__subclasses__() if classname(database.id, database.alias).title not in filterList]}
            management_rules = {'category':'',  'data':[classname(database.id, database.alias).check(database, database.version) for classname in R4.__subclasses__() if classname(database.id, database.alias).title not in filterList]}
            backup_rules = {'category':'',  'data':[classname(database.id, database.alias).check(database, database.version) for classname in R5.__subclasses__() if classname(database.id, database.alias).title not in filterList]}
            all_rules = [config_rules, peformance_rules, secure_rules, management_rules, backup_rules]
            score_sum = sum([_data.get('score') for _data in all_rules])
            total_score_sum = sum([_data.get('total_score') for _data in all_rules])
            final_score = round(score_sum / total_score_sum, 2)
            low_level_sum = 0
            mid_level_sum = 0
            high_level_sum = 0
            for rules in all_rules:
                for _data in rules.get('data'):
                    if float(_data.get('score')) < float(_data.get('total_score')):
                        if _data.get('priority') == '':
                            mid_level_sum += 1
                        else:
                            if _data.get('priority') == '':
                                low_level_sum += 1
                            else:
                                high_level_sum += 1

            old_list = merge_summary['summary']['database_score_list'] or []
            old_list.append([database.db_type, database.alias, final_score, high_level_sum, mid_level_sum])
            merge_summary['summary']['database_score_list'] = old_list
            merge_summary['report_list'][database.alias] = all_rules
            old_score = merge_summary['summary']['score']
            old_score.update({database.alias: final_score})
        merge_summary['summary']['score'] = old_score

    report.status = 4
    report.status_message = ''
    report.report_detail = merge_summary
    report.save()


@shared_task(bind=True)
def generate_healthcheck_report(self, database_id):
    report = None
    try:
        database = Database.objects.get(pk=database_id)
        rules_filter = cache.get(database.db_type + 'filter_data', '')
        filterList = rules_filter.split(';')
        if database.db_type == 'oracle':
            R1, R2, R3, R4, R5 = (
             Oracle_Config_Rule, Oracle_Performance_Rule, Oracle_Secure_Rule, Oracle_Management_Rule, Oracle_Backup_Rule)
        else:
            if database.db_type == 'db2':
                R1, R2, R3, R4, R5 = (
                 DB2_Config_Rule, DB2_Performance_Rule, DB2_Secure_Rule, DB2_Management_Rule, DB2_Backup_Rule)
            else:
                if database.db_type == 'sqlserver':
                    R1, R2, R3, R4, R5 = (
                     SQLServer_Config_Rule, SQLServer_Performance_Rule, SQLServer_Secure_Rule, SQLServer_Management_Rule, SQLServer_Backup_Rule)
            logger.info('start generate healthcheck report')
            report = Heathcheck_Report(database=database, status_message='', status=2)
            report.save()
            config_rules = {'category':'',  'data':[classname(database.id, database.alias).check(database, database.version) for classname in R1.__subclasses__() if classname(database.id, database.alias).title not in filterList]}
            peformance_rules = {'category':'', 
             'data':[classname(database.id, database.alias).check(database, database.version) for classname in R2.__subclasses__() if classname(database.id, database.alias).title not in filterList]}
            secure_rules = {'category':'',  'data':[classname(database.id, database.alias).check(database, database.version) for classname in R3.__subclasses__() if classname(database.id, database.alias).title not in filterList]}
            management_rules = {'category':'',  'data':[classname(database.id, database.alias).check(database, database.version) for classname in R4.__subclasses__() if classname(database.id, database.alias).title not in filterList]}
            backup_rules = {'category':'',  'data':[classname(database.id, database.alias).check(database, database.version) for classname in R5.__subclasses__() if classname(database.id, database.alias).title not in filterList]}
            all_rules = [config_rules, peformance_rules, secure_rules, management_rules, backup_rules]
            score_sum = sum([_data.get('score') for _data in all_rules])
            total_score_sum = sum([_data.get('total_score') for _data in all_rules])
            final_score = round(score_sum / total_score_sum, 2)
            total_level = ''
            if final_score < 60:
                total_level = ''
            else:
                if final_score < 80:
                    total_level = ''
                else:
                    total_level = ''
                low_level_sum = 0
                mid_level_sum = 0
                high_level_sum = 0
                for rules in all_rules:
                    for _data in rules.get('data'):
                        if _data.get('score') < _data.get('total_score'):
                            if _data.get('priority') == '':
                                mid_level_sum += 1
                            else:
                                if _data.get('priority') == '':
                                    low_level_sum += 1
                                else:
                                    high_level_sum += 1

                summary_message = f'''
        {total_level},{(low_level_sum + mid_level_sum + high_level_sum)}:

            {high_level_sum},, ,{high_level_sum}
            {mid_level_sum}, ,,SQL
            {low_level_sum},,,

        '''
                summary = {'score':final_score, 
                 'summary_message':summary_message}
                report_detail = {'summary':summary, 
                 'all_rules':all_rules}
                report.status = 1
                report.status_message = ''
                report.report_detail = report_detail
                report.save()
    except ObjectDoesNotExist as ex:
        logger.error(str(ex))
        report = Heathcheck_Report(status_message=',', status=3)
        report.save()
        return
    except Exception as ex:
        logger.error(str(ex))
        if not report:
            report = Heathcheck_Report(database_id=database_id, status_message=',:' + str(ex), status=3)
            report.save()
        else:
            report.status = 3
            report.status_message = ',:' + str(ex)
            report.save()


@api_view(['POST'])
def save_filter(request):
    if request.data.get('filter'):
        if request.data.get('db_type') == 'oracle':
            cache.set('oraclefilter_data', request.data.get('filter'), timeout=None)
        else:
            if request.data.get('db_type') == 'db2':
                cache.set('db2filter_data', request.data.get('filter'), timeout=None)
            else:
                if request.data.get('db_type') == 'sqlserver':
                    cache.set('sqlserverfilter_data', request.data.get('filter'), timeout=None)
            return Response({'message': ''})


@api_view(['POST'])
def get_report_filter(request):
    db_type = request.data.get('db_type')
    rules_filter, rules_title_map = get_rules(db_type)
    return Response({'rules_title_map':rules_title_map,  'rules_filter':rules_filter})


def get_rules(type):
    if not type:
        return
    else:
        if type == 'oracle':
            rules_title_map = {u'\u914d\u7f6e':[classname('', '').title for classname in Oracle_Config_Rule.__subclasses__()], 
             u'\u6027\u80fd':[classname('', '').title for classname in Oracle_Performance_Rule.__subclasses__()], 
             u'\u5b89\u5168':[classname('', '').title for classname in Oracle_Secure_Rule.__subclasses__()], 
             u'\u7ba1\u7406':[classname('', '').title for classname in Oracle_Management_Rule.__subclasses__()], 
             u'\u5907\u4efd':[classname('', '').title for classname in Oracle_Backup_Rule.__subclasses__()]}
        else:
            if type == 'db2':
                rules_title_map = {u'\u914d\u7f6e':[classname('', '').title for classname in DB2_Config_Rule.__subclasses__()],  u'\u5b89\u5168':[classname('', '').title for classname in DB2_Secure_Rule.__subclasses__()], 
                 u'\u6027\u80fd':[classname('', '').title for classname in DB2_Performance_Rule.__subclasses__()], 
                 u'\u5907\u4efd':[classname('', '').title for classname in DB2_Backup_Rule.__subclasses__()], 
                 u'\u7ba1\u7406':[classname('', '').title for classname in DB2_Management_Rule.__subclasses__()]}
            else:
                if type == 'sqlserver':
                    rules_title_map = {u'\u914d\u7f6e':[classname('', '').title for classname in SQLServer_Config_Rule.__subclasses__()],  u'\u5b89\u5168':[classname('', '').title for classname in SQLServer_Secure_Rule.__subclasses__()], 
                     u'\u6027\u80fd':[classname('', '').title for classname in SQLServer_Performance_Rule.__subclasses__()], 
                     u'\u5907\u4efd':[classname('', '').title for classname in SQLServer_Backup_Rule.__subclasses__()], 
                     u'\u7ba1\u7406':[classname('', '').title for classname in SQLServer_Management_Rule.__subclasses__()]}
                else:
                    rules_title_map = {u'\u914d\u7f6e':[classname('', '').title for classname in Oracle_Config_Rule.__subclasses__()], 
                     u'\u6027\u80fd':[classname('', '').title for classname in Oracle_Performance_Rule.__subclasses__()], 
                     u'\u5b89\u5168':[classname('', '').title for classname in Oracle_Secure_Rule.__subclasses__()], 
                     u'\u7ba1\u7406':[classname('', '').title for classname in Oracle_Management_Rule.__subclasses__()], 
                     u'\u5907\u4efd':[classname('', '').title for classname in Oracle_Backup_Rule.__subclasses__()]}
                rules_filter = cache.get(type + 'filter_data', '')
        return (
         rules_filter, rules_title_map)
# okay decompiling ./restful/hawkeye/api/v1/heathcheck/views.pyc
