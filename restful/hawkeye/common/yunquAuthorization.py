# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./common/yunquAuthorization.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 7212 bytes
import json, os.path, os.path, socket, struct
from base64 import b64decode
from collections import OrderedDict
from datetime import datetime
from uuid import getnode as get_mac
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_PSS
from django.conf import settings
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_PSS
from django.conf import settings
FCNTL_EXISTS = True
try:
    import fcntl
except ImportError:
    FCNTL_EXISTS = False

def _get_ip_address(ifname):
    if FCNTL_EXISTS:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 35093, struct.pack('256s', ifname[:15]))[20:24])
    else:
        return socket.gethostbyname(socket.gethostname())


def prepare_mac_str():
    mac = get_mac()
    mac_str = (':').join((('%012X' % mac)[i:i + 2] for i in range(0, 12, 2)))
    try:
        ip_str = _get_ip_address('eth0')
    except Exception as e:
        ip_str = ''

    return mac_str + ip_str


def _str_to_bytes(s):
    return bytes(s, encoding='utf-8')


def _bytes_to_str(b):
    return b.decode('utf-8')


LICENSE_FILE = os.path.join(settings.BASE_DIR, '.license.info')

def prepare_msg(client_name, targets, expiry_date_str, sql_audit, issue_date_str, service_expire_date_str):
    """
        return bytes
    """
    mac_str = prepare_mac_str()
    json_obj = OrderedDict((
     (
      'client_name', client_name),
     (
      'targets', targets),
     (
      'sql_audit', sql_audit),
     (
      'expiry_date', expiry_date_str),
     (
      'issue_date', issue_date_str),
     (
      'service_expire_date', service_expire_date_str)))
    json_str = json.dumps(json_obj)
    result = _str_to_bytes('%s%s' % (mac_str, json_str))
    return result


def verify(signature='', client_name='', targets='', expiry_date='', sql_audit='', issue_date='', service_expire_date='', **kwargs):
    """
        return True if the signature in b64encoded str can be verified by the public_key
    """
    msg = prepare_msg(client_name, targets, expiry_date, sql_audit, issue_date, service_expire_date)
    hash_obj = SHA.new(msg)
    try:
        sign = b64decode(signature)
    except Exception as e:
        print('signature decode error', e)
        return False

    public_key_str = '-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDAls3DZuunZwcytPp3kBCItO5W\n2tzzzzMUnt40PgacyfQ9ReuqdwVzt8n4b91CNeEQLgf69Rutjrtn8Y1FK53sOM4e\nyyp0dsDnVmNFNxlkyQTEdg1yOa0cdMXz3Rfq1HpdFHGX8DnQnoT2wyduwGHkayqO\n3h04jtxZm68y+3QqdwIDAQAB\n-----END PUBLIC KEY-----'
    public_key = RSA.importKey(public_key_str)
    public_cipher = PKCS1_PSS.new(public_key)
    return public_cipher.verify(hash_obj, sign)


def verify_sign():
    if not os.path.isfile(LICENSE_FILE):
        return False
    with open(LICENSE_FILE) as (data_file):
        data = json.load(data_file)
    expiry_date = datetime.strptime(data['expiry_date'], '%Y%m%d')
    if expiry_date < datetime.today():
        print('Product code expired.')
        return False
    issue_date = datetime.strptime(data['issue_date'], '%Y%m%d')
    if datetime.today() < issue_date:
        print('System time invalid.')
        return False
    else:
        return verify(**data)


__all__ = [
 'prepare_msg', 'verify', 'verify_sign', 'health_check', 'LICENSE_FILE']
# okay decompiling ./restful/hawkeye/common/yunquAuthorization.pyc
