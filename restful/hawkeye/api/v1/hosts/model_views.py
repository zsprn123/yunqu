# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/hosts/model_views.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 9771 bytes
import io, paramiko, requests
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import detail_route, api_view
from rest_framework.response import Response
from rest_framework_bulk import BulkModelViewSet
from alarm.models import Warn_Config
from api.celery.hosts.summary import hosts_summary
from api.v1.alarm.serializers import Warn_ConfigSerializer
from api.v1.hosts.filtersets import HostFilterSet, HostDetailFilterSet, LogMatchKeyFilterSet
from api.v1.hosts.serializers import HostSerializer, HostDetailSerializer, LogMatchKeySerializer, Warn_Config_promsSerializer, send_warnconfig_proms, update_proms_config
from api.v1.monitor.services.createdbService import init_global_warnconfig
from common.aes import aes_decode
from hosts.models import Host, HostDetail, LogMatchKey
import json, datetime
from django.conf import settings

class PromsQuery:

    def __init__(self, query, category, description):
        self.query = query
        self.category = category
        self.description = description


class HostViewSet(BulkModelViewSet):
    queryset = Host.objects.all()
    serializer_class = HostSerializer
    filter_class = HostFilterSet
    prom_url = settings.PROMS_URL + ':9090/api/v1/query_range?query={query_key}&start={start_time}&end={end_time}&step={step}'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        update_proms_config(instance, 'delete')
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @detail_route(methods=[
     'get'],
      url_path='summary')
    def get_host_summary_data(self, request, pk=None):
        host = self.get_object()
        summary_data = hosts_summary(host)
        return Response(summary_data, status=status.HTTP_200_OK)

    @detail_route(methods=[
     'get'],
      url_path='dynamic-data')
    def get_dynamic_data(self, request, pk=None):
        host = self.get_object()
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')
        step = request.query_params.get('step')
        now_timestamp = int(datetime.datetime.now().timestamp())
        d1 = int((datetime.datetime.now() - (datetime.timedelta(hours=1))).timestamp())
        data = []
        format_data = {'start_time':start_time or d1, 
         'end_time':end_time or now_timestamp, 
         'step':step or 75}
        memery_query = PromsQuery(f'''1-node_memory_MemAvailable{instance='{(host.address)}'}/node_memory_MemTotal{instance='{(host.address)}'}''', 'memery', '')
        cpu_query = PromsQuery(f'''1 - (avg by (instance) (irate(node_cpu{instance='{(host.address)}', mode='idle'}[5m])))''', 'cpu', 'cpu')
        disk_query = PromsQuery(f'''1 - node_filesystem_free{instance='{(host.address)}',fstype!~'rootfs|selinuxfs|autofs|rpc_pipefs|tmpfs|udev|none|devpts|sysfs|debugfs|fuse.*'} / node_filesystem_size{instance='{(host.address)}',fstype!~'rootfs|selinuxfs|autofs|rpc_pipefs|tmpfs|udev|none|devpts|sysfs|debugfs|fuse.*'}''', 'disk', '')
        network_io_update = PromsQuery(f'''sum by (instance) (irate(node_network_receive_bytes{instance='{(host.address)}',device!~'bond.*?|lo'}[5m])/128)''', 'network_io_update', ' IO()')
        network_io_download = PromsQuery(f'''sum by (instance) (irate(node_network_transmit_bytes{instance='{(host.address)}',device!~'bond.*?|lo'}[5m])/128)''', 'network_io_download', ' IO()')
        network_out_package = PromsQuery(f'''sum by (instance) (rate(node_network_receive_bytes{instance='{(host.address)}',device!='lo'}[5m]))''', 'network_out_package', '')
        network_in_package = PromsQuery(f'''sum by (instance) (rate(node_network_transmit_bytes{instance='{(host.address)}',device!='lo'}[5m]))''', 'network_in_package', '')
        query_list = [
         memery_query, cpu_query, network_io_update, network_io_download, network_in_package,
         network_out_package]
        for query in query_list:
            res = requests.get(self.prom_url.format(**format_data, **{'query_key': query.query}))
            if res.status_code == 200:
                if res.json().get('status', None):
                    _data = {}
                    for res_data in res.json().get('data', {}).get('result', []):
                        _data.update({query.category: [[data1[0] * 1000, float(data1[1])] for data1 in res_data.get('values', [])]})

                    data.append({'type':query.category, 
                     'name':query.description, 
                     'data':_data})

        return Response(data, status=status.HTTP_200_OK)

    @detail_route(methods=[
     'post'],
      url_path='save-log-config')
    def save_log_config(self, request, pk=None):
        config = request.data
        if type(config) == list:
            warnconfig_is_exists = Warn_Config.objects.filter((Q(host=self.get_object())) & (Q(category='Log_Warn'))).exists()
            if warnconfig_is_exists:
                warnconfig = Warn_Config.objects.filter((Q(host=self.get_object())) & (Q(category='Log_Warn')))[0]
                warnconfig.optional.update({'log_config': config})
                flag = send_log_config_proms(self.get_object(), config)
                if not flag:
                    return Response({'message': ',PROMS '}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                warnconfig.save()
                send_warnconfig_proms(self.get_object())
            else:
                return Response({'message': ','}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'message': ','}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': ''}, status=status.HTTP_200_OK)

    @detail_route(methods=[
     'get'],
      url_path='get-log-config')
    def get_log_config(self, request, pk=None):
        warnconfig_is_exists = Warn_Config.objects.filter((Q(host=self.get_object())) & (Q(category='Log_Warn'))).exists()
        if warnconfig_is_exists:
            warnconfig = Warn_Config.objects.filter((Q(host=self.get_object())) & (Q(category='Log_Warn')))[0]
            data = Warn_ConfigSerializer(warnconfig).data.get('optional', {}).get('log_config', [])
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'message': ''}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def send_log_config_proms(host, log_config):
    json_body = {'address':host.address, 
     'log':log_config or []}
    print(json.dumps(json_body))
    res = requests.post(settings.PROMS_URL + ':9091/v1/monitor/config/log', json=json_body)
    print(res.text)
    if res.status_code != 200:
        return False
    else:
        return True


class HostDetailViewSet(BulkModelViewSet):
    queryset = HostDetail.objects.all()
    serializer_class = HostDetailSerializer
    filter_class = HostDetailFilterSet


@api_view(['POST'])
def host_test_connection(request):
    address = request.data.get('address', '').strip() if request.data.get('address') else ''
    port = request.data.get('port', None)
    username = request.data.get('username', '').strip() if request.data.get('username') else ''
    password = request.data.get('password', '').strip() if request.data.get('password') else ''
    need_decode = request.data.get('need_decode', False)
    ssh_key = request.data.get('ssh_key')
    if not address:
        return Response({'message': 'hostname is required'}, status=status.HTTP_400_BAD_REQUEST)
    if ssh_key:
        private_key_file = io.StringIO()
        private_key_file.write(ssh_key)
        private_key_file.seek(0)
        private_key = paramiko.RSAKey.from_private_key(private_key_file)
        host_config = {'pkey':private_key, 
         'hostname':address, 
         'username':username, 
         'timeout':60}
    else:
        if need_decode:
            try:
                password = aes_decode(password)
            except Exception as e:
                print(str(e))

            host_config = {'hostname':address,  'username':username, 
             'password':password, 
             'timeout':60}
        if port:
            host_config.update({'port': port})
        try:
            s = paramiko.SSHClient()
            s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            s.connect(**host_config)
        except Exception as e:
            return Response({'message': ',:' + str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': ''}, status=status.HTTP_200_OK)


class LogMatchKeyViewSet(BulkModelViewSet):
    queryset = LogMatchKey.objects.all()
    serializer_class = LogMatchKeySerializer
    filter_class = LogMatchKeyFilterSet
# okay decompiling ./restful/hawkeye/api/v1/hosts/model_views.pyc
