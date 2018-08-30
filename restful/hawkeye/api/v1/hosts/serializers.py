# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/hosts/serializers.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 7056 bytes
import json, requests
from django.db.models import Q
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta
from rest_framework_bulk import BulkListSerializer
from rest_framework_filters.compat import set_many
from rest_framework import serializers
from alarm.models import Warn_Config
from api.celery.hosts.summary import hosts_summary
from api.v1.monitor.services.createdbService import init_warnconfig
from common.aes import aes_encode
from common.serializers import DynamicFieldsModelSerializer
from hosts.models import Host, HostDetail, LogMatchKey
from django.conf import settings
import logging
logger = logging.getLogger('api')

class HostSerializer(DynamicFieldsModelSerializer):

    def create(self, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = aes_encode(validated_data['password'])
        item = Host.objects.create(**validated_data)
        item.save()
        try:
            update_proms_config(item, 'post')
            init_warnconfig(item)
            send_warnconfig_proms(item)
        except:
            return item

        return item

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = aes_encode(validated_data['password'])
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)
        for attr, value in validated_data.items():
            if attr in info.relations:
                if info.relations[attr].to_many:
                    set_many(instance, attr, value)
            else:
                setattr(instance, attr, value)

        send_warnconfig_proms(instance)
        update_proms_config(instance, 'patch')
        instance.save()
        return instance

    class Meta:
        model = Host
        list_serializer_class = BulkListSerializer
        fields = '__all__'


class HostDetailSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = HostDetail
        list_serializer_class = BulkListSerializer
        fields = '__all__'


class LogMatchKeySerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = LogMatchKey
        list_serializer_class = BulkListSerializer
        fields = '__all__'


class Warn_Config_promsSerializer(DynamicFieldsModelSerializer):
    name = serializers.SerializerMethodField()
    summary = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    metric = serializers.SerializerMethodField()

    class Meta:
        model = Warn_Config
        list_serializer_class = BulkListSerializer
        fields = ('warn_threshold', 'critical_threshold', 'warning_interval', 'name',
                  'summary', 'description', 'metric')

    def get_name(self, obj):
        return obj.category

    def get_summary(self, obj):
        optional = obj.optional
        return optional.get('summary', '')

    def get_description(self, obj):
        optional = obj.optional
        return optional.get('description', '')

    def get_metric(self, obj):
        if obj.category == 'Host_CPU_Warn':
            return f'''1 - (avg by (instance) (irate(node_cpu{instance="{(obj.host.address)}", mode="idle"}[5m])))'''
        elif obj.category == 'Host_Disk_Warn':
            return f'''1 - node_filesystem_free{instance="{(obj.host.address)}",fstype!~"rootfs|selinuxfs|autofs|rpc_pipefs|tmpfs|udev|none|devpts|sysfs|debugfs|fuse.*"} / node_filesystem_size{instance="{(obj.host.address)}",fstype!~"rootfs|selinuxfs|autofs|rpc_pipefs|tmpfs|udev|none|devpts|sysfs|debugfs|fuse.*"}'''
        else:
            return ''


class Host2PromsSerializer(DynamicFieldsModelSerializer):
    password = serializers.SerializerMethodField()
    port = serializers.SerializerMethodField()

    def get_password(self, obj):
        return obj.get_password()

    def get_port(self, obj):
        return str(obj.port)

    class Meta:
        model = Host
        list_serializer_class = BulkListSerializer
        exclude = ('disabled', 'created_at', 'updated_at')


def send_warnconfig_proms(host):
    warn_config_list = (Warn_Config.objects.filter(host=host)).exclude(category='Log_Warn')
    warn_config_json = (Warn_Config_promsSerializer(warn_config_list, many=True)).data
    warn_log_config = (Warn_Config.objects.filter(host=host)).filter(category='Log_Warn')
    log_config_json = []
    if warn_log_config.exists():
        log_configs = warn_log_config[0].optional.get('log_config', [])
        for log_config in log_configs:
            log_config_json.append({'name':log_config.get('filename', 'log_warn'), 
             'warn_threshold':warn_log_config[0].warn_threshold, 
             'critical_threshold':warn_log_config[0].critical_threshold, 
             'warning_interval':warn_log_config[0].warning_interval, 
             'summary':'', 
             'description':'', 
             'metric':f'''sum(node_log_keywords{file="{log_config.get('filename', '')}",keywords=~"{('|').join(log_config.get('keywords', []))}",instance="{host.address}"})'''})

    warn_config_json = warn_config_json + log_config_json
    print('')
    logger.warning('')
    print(json.dumps(warn_config_json))
    logger.warning(json.dumps(warn_config_json))
    json_body = {'address':host.address, 
     'alert':warn_config_json or []}
    print(json_body)
    res = requests.post(settings.PROMS_URL + ':9091/v1/monitor/config/alert', json=json_body)
    print(res.json())
    res2 = requests.post(settings.PROMS_URL + ':9090/-/reload', json={})
    logger.warning(' reload')
    print(str(res2.status_code))
    logger.warning(str(res2.status_code))


def update_proms_config(host, method):
    host_json = (Host2PromsSerializer(Host.objects.all(), many=True)).data
    json_body = {'hosts': host_json or []}
    if method == 'post':
        print(settings.PROMS_URL + ':9091/v1/monitor/config/host/' + '\n')
        print(json.dumps(Host2PromsSerializer(host).data))
        res = requests.post(settings.PROMS_URL + ':9091/v1/monitor/config/host', json=Host2PromsSerializer(host).data)
    else:
        if method == 'patch':
            print(settings.PROMS_URL + ':9091/v1/monitor/config/host/' + str(host.id) + '\n')
            print(json.dumps(Host2PromsSerializer(host).data))
            res = requests.put(settings.PROMS_URL + ':9091/v1/monitor/config/host/' + str(host.id), json=Host2PromsSerializer(host).data)
        else:
            if method == 'delete':
                print(settings.PROMS_URL + ':9091/v1/monitor/config/host/' + str(host.id) + '\n')
                print(json.dumps(Host2PromsSerializer(host).data))
                res = requests.delete(settings.PROMS_URL + ':9091/v1/monitor/config/host/' + str(host.id), json={})
        logger.warning(res.text)
        print(res.text)
# okay decompiling ./restful/hawkeye/api/v1/hosts/serializers.pyc
