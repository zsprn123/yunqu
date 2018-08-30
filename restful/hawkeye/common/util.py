# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./common/util.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 7953 bytes
from collections import defaultdict
from datetime import datetime
import time, requests
from channels import Group
from django.db import connection
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import hashlib, struct, operator
from alarm.models import Receiver
import logging
from api.enum.performance_enum import VALUE_ENUM, NAME_ENUM
from xml.etree import ElementTree as ET
logger = logging.getLogger(__name__)

def get_performance_name(key):
    return VALUE_ENUM.get(str(key), key)


def get_performance_name_id(key):
    return NAME_ENUM.get(key, key)


def view_try_except(func, *args, **kw):

    def exec_func(*args, **kw):
        try:
            return func(*args, **kw)
        except Exception as e:
            error = e.args
            print(error)
            return Response({'error_message': error}, status=status.HTTP_400_BAD_REQUEST)

    return exec_func


def timestamp_to_datetime(ts):
    return datetime.fromtimestamp(ts)


def timestamp_to_char(ts):
    return datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')


def get_1s_timestamp():
    return int(round(time.time() - time.time() % 10))


def get_timestamp():
    return int(round(time.time() * 1000))


def get_10s_timestamp():
    return int(round(time.time() - time.time() % 10) * 1000)


def get_10s_time():
    return datetime.strptime(str(datetime.now())[:18] + '0', '%Y-%m-%d %H:%M:%S')


def get_10s_time_str():
    return str(datetime.now())[:18] + '0'


def to_date(datetime_str):
    return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')


def to_str(date):
    return str(date)


def is_response_error(r):
    if r.status_code == 500:
        return True
    else:
        return False


def get_url(url):
    return settings.BASE_URL + url


def get_java_response(method, jsonobj):
    if not jsonobj:
        jsonobj = {}
    return requests.post(get_url(method), json=jsonobj, timeout=10000)


def new_execute_cpu_return_json(query):
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    if not rows:
        return {}
    else:
        data_dic = {'HOST CPU UTILIZATION (%)': {}}
        for row in rows:
            if row[1] in data_dic.get('HOST CPU UTILIZATION (%)'):
                data_dic['HOST CPU UTILIZATION (%)'][row[1]].append([row[3], row[2]])
            else:
                data_dic['HOST CPU UTILIZATION (%)'][row[1]] = [
                 [
                  row[3], row[2]]]

        return data_dic


def execute_ash_return_json(query):
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    if not rows:
        return {}
    else:
        data_dic = defaultdict(list)
        for row in rows:
            data_dic[row[0]].append([row[2], row[1]])

        return data_dic


def execute_performance_return_json(query):
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    if not rows:
        return {'error_message': '.'}
    else:
        data_dic = {}
        for row in rows:
            data_dic[row[0]] = [
             row[2], row[1]]

        return data_dic


def new_execute_ash_return_json(query):
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    if not rows:
        return {}
    else:
        data_dic = defaultdict(list)
        for row in rows:
            data_dic[get_performance_name(row[0])].append([row[2], row[1]])

        return data_dic


def new_execute_performance_return_json(query):
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    if not rows:
        return {'error_message': '.'}
    else:
        data_dic = {}
        for row in rows:
            data_dic[get_performance_name(row[0])] = [
             row[2], row[1]]

        return data_dic


def execute_query_return_top_dimension(query, wait_class_list, group_by_len, table_header):
    cursor = connection.cursor()
    cursor.execute(query)
    resultSet = cursor.fetchall()
    result = []
    start_point = group_by_len + 2
    for x in resultSet:
        top_item = {}
        color_value = {}
        for i in range(0, len(wait_class_list)):
            if x[start_point + i] > 0:
                color_value[wait_class_list[i]] = float(x[start_point + i])

        sorted_x = sorted(color_value.items(), key=operator.itemgetter(1))
        sorted_x.reverse()
        bar_data = [{item[0]: item[1]} for item in sorted_x]
        top_item[table_header[0]] = {'percent':x[group_by_len], 
         'bar_data':bar_data}
        top_item[table_header[1]] = x[group_by_len + 1]
        for i in range(0, group_by_len):
            top_item[table_header[2 + i]] = x[i]

        result.append(top_item)

    return result


def dictfetchall(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0].upper() for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def execute_return_json(query):
    cursor = connection.cursor()
    cursor.execute(query)
    return dictfetchall(cursor)


def enum2str(enum):
    if not enum:
        raise SystemError
    result = []
    for e in enum:
        value = e.value
        result.append(value.upper())

    result = (',').join(result)
    return result


def gen_sql_id(stmt):
    stmt = stmt + '\x00'
    stmt = str.encode(stmt)
    h = hashlib.md5(stmt).digest()
    sqlid = str(struct.unpack('IIII', h)[3])
    return sqlid


def build_exception_from_java(result):
    return Exception('%s %s' % (result.get('exception'), result.get('message')))


def has_instance(database):
    if not database:
        return False
    elif database.instance_count == 1:
        return False
    else:
        return True


def send_alarm(database_id, text):
    Group('alarm-' + str(database_id)).send({'text': text}, immediately=True)


def default_to_regular(d):
    if isinstance(d, defaultdict):
        d = {k:default_to_regular(v) for k, v in d.items()}
    return d


def send_osb_sms(text):
    receivers = Receiver.objects.all()
    if receivers:
        for receiver in receivers:
            mobile = receiver.phone_number
            if mobile:
                obs_send(mobile, text)
            else:
                logger.info('send_osb_sms:recevier ' + receiver.name + ' no phone number')

    else:
        logger.info('send_osb_sms:recevier is not exits')


def obs_send(mobile, text):
    url = settings.OBS_URL + '/TFGZRC/ProxyServices/SMS/HTTP.SMS.PUBLIC.proxy'
    request_tree = ET.parse('osb.xml')
    request_root = request_tree.getroot()
    mobileTeleNumber = request_root.find('body').find('request').find('xfaceTradeDTO').find('smsMT').find('mobileTeleNumber')
    mobileTeleNumber.text = mobile
    msg = request_root.find('body').find('request').find('xfaceTradeDTO').find('smsMT').find('msg')
    msg.text = text
    xml_str = ET.tostring(request_root, encoding='utf-8', method='xml')
    r = requests.post(url=url, data=xml_str, headers={'Content-Type': 'text/xml'})
    response_root = ET.XML(r.text)
    errCode = response_root.find('body').find('response').find('xfaceTradeDTO').find('responseDTO').find('errCode')
    if errCode.text == '0':
        logger.info('send_osb_sms: msg to ' + mobile + 'send success')
    else:
        logger.error('send_osb_sms: msg to ' + mobile + 'send falied errorCode ' + errCode.text)
# okay decompiling ./restful/hawkeye/common/util.pyc
