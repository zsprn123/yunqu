# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/alarm/views.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 8671 bytes
import base64, json, zlib, requests
from django.conf import settings
from django.core.mail.backends.smtp import EmailBackend
from django.db.models import Q
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from guardian.shortcuts import get_objects_for_user
from rest_framework import status
from rest_framework.decorators import detail_route, api_view
from rest_framework.response import Response
from rest_framework_bulk import BulkCreateModelMixin
from rest_framework_bulk.generics import BulkModelViewSet
from alarm.models import Warn_Config, Warn_Config_Template, Receiver, Warn_Result, Mail_Config
from api.v1.alarm.filtersets import Warn_ConfigFilterSet, PeriodicTaskFilterSet, IntervalScheduleFilterSet, Warn_ResultFilterSet, Warn_Config_TemplateFilterSet, ReceiverFilterSet
from api.v1.alarm.serializers import Warn_ConfigSerializer, PeriodicTaskSerializer, IntervalScheduleSerializer, Warn_Config_TemplateSerializer, Warn_ResultSerializer, ReceiverSerializer, Mail_ConfigSerializer
from api.v1.alarm.services.warnConfigService import update_database_warn_config
from api.v1.hosts.serializers import send_warnconfig_proms
from api.v1.monitor.filtersets import default_filterset
from celery import current_app
from api.v1.monitor.services.createdbService import init_warnconfig
from common.util import send_alarm
from hosts.models import Host
from monitor.models import Database, Space
import logging
logger = logging.getLogger(__name__)

class WarnConfigViewSet(BulkModelViewSet):
    queryset = Warn_Config.objects.all()
    serializer_class = Warn_ConfigSerializer
    filter_class = Warn_ConfigFilterSet

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        if instance.host:
            send_warnconfig_proms(instance.host)
        return Response(serializer.data)


class Warn_Config_TemplateViewSet(BulkModelViewSet):
    queryset = Warn_Config_Template.objects.all()
    serializer_class = Warn_Config_TemplateSerializer
    filter_class = Warn_Config_TemplateFilterSet

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        update_database_warn_config(instance)
        return Response(serializer.data)


class Warn_ResultViewSet(BulkModelViewSet):
    queryset = Warn_Result.objects.all()
    serializer_class = Warn_ResultSerializer
    filter_class = Warn_ResultFilterSet

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Warn_Result.objects.all()
        else:
            database_list = get_objects_for_user(user, 'monitor.view_database')
            return Warn_Result.objects.filter((Q(database__in=database_list)) | (Q(database=None)))


class ReceiverViewSet(BulkModelViewSet):
    queryset = Receiver.objects.all()
    serializer_class = ReceiverSerializer
    filter_class = ReceiverFilterSet


class PeriodicTaskViewSet(BulkModelViewSet):
    queryset = PeriodicTask.objects.all()
    serializer_class = PeriodicTaskSerializer
    filter_class = PeriodicTaskFilterSet


class IntervalScheduleViewSet(BulkModelViewSet):
    queryset = IntervalSchedule.objects.all()
    serializer_class = IntervalScheduleSerializer
    filter_class = IntervalScheduleFilterSet


class Mail_ConfigViewSet(BulkModelViewSet):
    queryset = Mail_Config.objects.all()
    serializer_class = Mail_ConfigSerializer
    filter_class = default_filterset(Mail_Config)

    def create(self, request, *args, **kwargs):
        Mail_Config.objects.all().delete()
        return super(BulkCreateModelMixin, self).create(request, *args, **kwargs)


@api_view(['GET'])
def get_mail_config(request):
    config = {}
    config_list = Mail_Config.objects.all()
    if not config_list:
        return Response({'host':'smtp.qq.com', 
         'port':465, 
         'username':'example@qq.com', 
         'password':'', 
         'use_tls':False, 
         'use_ssl':True},
          status=status.HTTP_200_OK)
    else:
        config = config_list[0]
        return Response(Mail_ConfigSerializer(config).data, status=status.HTTP_200_OK)


@api_view(['POST'])
def test_mail_connection(request):
    host = request.data.get('host', '')
    port = request.data.get('port', '')
    username = request.data.get('username', '')
    password = request.data.get('password', '')
    use_ssl = request.data.get('use_ssl', True)
    use_tls = request.data.get('use_tls', False)
    try:
        backend = EmailBackend(host=host, port=port, username=username, password=password,
          use_ssl=use_ssl,
          use_tls=use_tls,
          fail_silently=False)
        backend.open()
    except Exception as e:
        return Response({'error_message': '' + str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': ''})


@api_view(['GET'])
def get_celery_tasks(request):
    tasks = list(sorted((name for name in current_app.tasks if not name.startswith('celery.'))))
    return Response({'tasks': tasks})


@api_view(['GET'])
def reset_warn_config(request):
    Warn_Config_Template.objects.all().delete()
    for database in Database.objects.all():
        init_warnconfig(database)

    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def get_space_table_name(request):
    name_list = []
    if request.data.get('db_type', None):
        name_list = (Space.objects.filter(database__db_type=request.data.get('db_type'))).values_list('name', flat=True)
    if request.data.get('database', None):
        name_list = (Space.objects.filter(database__id=request.data.get('database'))).values_list('name', flat=True)
    name_set = set(name_list)
    return Response(name_set, status=status.HTTP_200_OK)


@api_view(['POST'])
def handle_prom_alert(request):
    prom_alerts = request.data.get('alerts', [])
    logging.error(':' + json.dumps(prom_alerts))
    for alert in prom_alerts:
        severity = alert.get('labels', {}).get('severity', '')
        host = Host.objects.filter(address=alert.get('labels', {}).get('instance', ''))
        if host.exists():
            host = host[0]
            warn_config = Warn_Config.objects.filter(host=host)
            if warn_config.exists():
                warn_content = get_warn_content(host=host.address)
                logger.info(warn_content)
                warn_message = f'''{severity}!!,{(alert.get('annotations', {}).get('description', ''))},{warn_content}'''
                logger.info(warn_message)
                warn_result = Warn_Result(warn_message=warn_message, warn=warn_config[0])
                warn_result.save()
                warn_alert = {'warn_message':warn_message, 
                 'link':{}}
                send_alarm(host.id, json.dumps(warn_alert))

    return Response(status=status.HTTP_200_OK)


def get_warn_content(host):
    playload = {'query':'node_log_keywords', 
     'instance':host}
    logger.info(playload)
    res = requests.get(settings.PROMS_URL + ':9090/api/v1/query', params=playload)
    res_json = json.loads(res.text)
    result = res_json['data']['result']
    logger.info(result)
    content = ''
    if result:
        logger.info('get metric')
        metric = result[0]['metric']
        logger.info(metric)
        contents = metric['content']
        if contents:
            logger.info('get content')
            contents = bytes.decode(zlib.decompress(base64.standard_b64decode(contents)))
            contents = contents.splitlines()
            content = contents[0]
            logger.info(content)
    logger.info(content)
    return content
# okay decompiling ./restful/hawkeye/api/v1/alarm/views.pyc
