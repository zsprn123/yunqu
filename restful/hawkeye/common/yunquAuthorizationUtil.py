# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./common/yunquAuthorizationUtil.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 2399 bytes
from common.storages import redis
from monitor.models import Database
from .yunquAuthorization import verify_sign, LICENSE_FILE
from django.conf import settings
import os, json
from datetime import datetime
import hashlib
from django.core.cache import cache

def get_lisence_info():
    license_info = {}
    license_info['certificated'] = verify_sign()
    current_total = get_current_total()
    LICENSE_FILE = os.path.join(settings.BASE_DIR, '.license.info')
    license_file = LICENSE_FILE
    if os.path.exists(license_file):
        with open(license_file) as (data_file):
            data = json.load(data_file)
    else:
        data = {}
    licensed_targets = data.get('targets', None)
    expiry_date = data.get('expiry_date', None)
    if licensed_targets:
        available_count = int(licensed_targets) - current_total
    else:
        available_count = None
    license_info['licensed_targets'] = licensed_targets
    license_info['current_total'] = current_total
    license_info['available_count'] = available_count
    license_info['expiry_date'] = expiry_date
    license_info['issue_date'] = data.get('issue_date', None)
    days = None
    if expiry_date:
        days = (datetime.strptime(data['expiry_date'], '%Y%m%d') - datetime.now()).days
    license_info['days'] = days
    license_info['client_name'] = data.get('client_name', '')
    license_info['product_key'] = ''
    if license_info['client_name'] != '':
        s = hashlib.sha256(('yunqu_hawkeye').encode('utf-8') + license_info['client_name'].encode('utf-8')).hexdigest()[:16].upper()
        license_info['product_key'] = ('-').join(map(('').join, zip(*[iter(s)] * 4)))
    license_info['service_expire_date'] = data.get('service_expire_date', license_info['expiry_date'])
    return license_info


def current_target_available():
    if verify_sign():
        current_total = get_current_total()
        license_file = LICENSE_FILE
        with open(license_file) as (data_file):
            data = json.load(data_file)
        licensed_targets = data['targets']
        if not licensed_targets:
            return False
        available_count = int(licensed_targets) - current_total
        return available_count
    else:
        return False


def get_current_total():
    return sum(list((Database.objects.all().exclude(is_switch_off=True)).values_list('instance_count', flat=True)))
# okay decompiling ./restful/hawkeye/common/yunquAuthorizationUtil.pyc
