# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./inventory.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 962 bytes
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hawkeye.settings.dev')
import django
django.setup()
import json, sys
from hosts.models import Host
import socket

def group():
    host_list = Host.objects.all().values_list('address', flat=True)
    host1 = list(host_list)
    group1 = 'test-group'
    hostdata = {group1: {'hosts': host1}}
    print(json.dumps(hostdata, indent=4))


def host(ip):
    try:
        h = Host.objects.get(address=ip)
        info_dict = {'ansible_ssh_host':h.address, 
         'ansible_ssh_user':h.username, 
         'ansible_ssh_pass':h.get_password()}
        print(json.dumps(info_dict, indent=4))
    except:
        pass


if len(sys.argv) == 2:
    if sys.argv[1] == '--list':
        group()
    if len(sys.argv) == 3:
        if sys.argv[1] == '--host':
            host(sys.argv[2])
        print('Usage: %s --list' % sys.argv[0])
        sys.exit(1)
# okay decompiling ./restful/hawkeye/inventory.pyc
