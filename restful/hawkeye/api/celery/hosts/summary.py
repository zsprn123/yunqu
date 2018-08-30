# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/celery/hosts/summary.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 9029 bytes
import io, paramiko
from common.aes import aes_decode
from django.core.cache import cache

def hosts_summary(host):
    summary_data = cache.get('host-data' + str(host.id))
    if summary_data:
        return summary_data
    else:
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if host.ssh_key:
            private_key_file = io.StringIO()
            private_key_file.write(host.ssh_key)
            private_key_file.seek(0)
            private_key = paramiko.RSAKey.from_private_key(private_key_file)
            host_config = {'pkey':private_key, 
             'hostname':host.address, 
             'username':host.username, 
             'timeout':60, 
             'port':host.port}
            s.connect(**host_config)
        else:
            s.connect(host.address, host.port, host.username, aes_decode(host.password))
        cpu_model, cpu_num, core_num = get_cpu_info(s)
        memory_max_size, memory_speed, memory_model, memory_size = get_memory_info(s)
        network_info_list = get_network_info(s)
        directory_info_list = get_directory_info(s)
        hostname, lsb = get_host_info(s)
        summary_data = {'host_info':{'lsb':lsb, 
          'hostname':hostname}, 
         'memory':{'memory_max_size':memory_max_size, 
          'memory_speed':memory_speed, 
          'memory_model':memory_model, 
          'memory_size':memory_size}, 
         'processor':{'ansible_processor':cpu_model, 
          'ansible_processor_count':cpu_num, 
          'ansible_processor_core_count':core_num}, 
         'disk_mount':directory_info_list, 
         'network_info':network_info_list}
        cache.set('host-data' + str(host.id), summary_data, timeout=360)
        return summary_data


def get_cpu_info(connect):
    cpu_model = ''
    cpu_num = None
    core_num = None
    stdin, stdout, stderr = connect.exec_command('cat /proc/cpuinfo | grep name | cut -f2 -d: | uniq -c;cat /proc/cpuinfo| grep "processor"| wc -l;cat /proc/cpuinfo| grep "cpu cores"| uniq;cat /proc/cpuinfo| grep "physical id"| sort| uniq| wc -l')
    all_lines = stdout.read().decode('ASCII', 'ignore').splitlines()
    line_num = 0
    for line in all_lines:
        if line_num == 0:
            cpu_model = line.split('  ')[-1]
        else:
            if line_num == 1:
                cpu_num = int(line.strip())
            else:
                if line_num == 2:
                    try:
                        c = int(line.split(':')[1].strip())
                    except Exception as e:
                        c = 1

                else:
                    if line_num == 3:
                        pcore = int(line.strip())
                        core_num = c * pcore
                line_num += 1

    return (
     cpu_model, cpu_num, core_num)


def get_memory_info(connect):
    memory_max_size = ''
    memory_speed = ''
    memory_model = ''
    memory_size = ''
    stdin, stdout, stderr = connect.exec_command('dmidecode -t memory|grep -E "Type:|Speed|Maximum Capacity:|Type:" |head -5;cat /proc/meminfo |grep "MemTotal"')
    all_lines = stdout.read().decode('ASCII', 'ignore').splitlines()
    for line in all_lines:
        if 'Maximum Capacity' in line:
            memory_max_size = line.split(':')[1].strip()
        elif 'Speed' in line:
            memory_speed = line.split(':')[1].strip()
        elif 'Type:' in line:
            memory_model = line.split(':')[1].strip()
        elif 'MemTotal' in line:
            memory_size = int(line.split(':')[1].strip().split()[0]) / 1024 / 1024

    return (
     memory_max_size, memory_speed, memory_model, memory_size)


def get_network_info(connect):
    network_info_list = []
    net_device_ip = None
    net_device_name = None
    net_device_status = None
    net_device_mtu = None
    stdin, stdout, stderr = connect.exec_command('ip a l |grep -E "inet |stat"')
    all_lines = stdout.read().decode('ASCII', 'ignore').splitlines()
    new_interface = True
    for line in all_lines:
        if ' lo' in line:
            continue
        if 'inet' in line:
            if new_interface:
                ip = line.split('/')[0].split(' ')[5]
                net_device_ip = ip
                new_interface = False
                network_info_list.append({'net_device_ip':net_device_ip, 
                 'net_device_name':net_device_name,  'net_device_status':net_device_status, 
                 'net_device_mtu':net_device_mtu})
                net_device_ip = None
                net_device_name = None
                net_device_status = None
                net_device_mtu = None
            else:
                if 'state DOWN' not in line:
                    new_interface = True
                    splited = line.split(':')
                    dname = splited[1].strip()
                    s2 = splited[2].split(' ')
                    status = s2[1][1:-1]
                    mtu = s2[3]
                    net_device_name = dname
                    net_device_status = status
                    net_device_mtu = mtu

    return network_info_list


def get_directory_info(connect):
    directory_info_list = []
    stdin, stdout, stderr = connect.exec_command('df -k;date  "+%F %T"')
    all_lines = stdout.read().decode('ASCII', 'ignore').splitlines()
    line_tag = 1
    is_one_record = False
    directory, used_percent, avail, used, size = (None, None, None, None, None)
    for line in all_lines[:-1]:
        r = line.split()
        r = r[:6]
        if line_tag != 1:
            if len(r) != 1:
                if is_one_record:
                    is_one_record = False
                else:
                    filesystem = r[0]
                filesystem = filesystem
                directory = r[-1]
                used_percent = r[-2]
                avail = str(round(int(r[-3]) / 1024.0 / 1024, 1)) + 'G'
                used = str(round(int(r[-4]) / 1024.0 / 1024, 1)) + 'G'
                size = str(round(int(r[-5]) / 1024.0 / 1024, 1)) + 'G'
                directory_info_list.append({'directory':directory, 
                 'used_percent':used_percent, 
                 'avail':avail, 
                 'used':used, 
                 'size':size})
                directory, used_percent, avail, used, size = (None, None, None, None,
                                                              None)
            else:
                filesystem = r[0]
                is_one_record = True
            line_tag = line_tag + 1

    return directory_info_list


def get_host_info(connect):
    stdin, stdout1, stderr = connect.exec_command('cat /proc/sys/kernel/hostname')
    hostname = stdout1.readline() or ''
    stdin, stdout2, stderr = connect.exec_command('cat /etc/redhat-release')
    lsb = stdout2.readline() or ''
    return (
     hostname, lsb)
# okay decompiling ./restful/hawkeye/api/celery/hosts/summary.pyc
