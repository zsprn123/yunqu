# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./sqlaudit/enum/db2_function_enum.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 1227 bytes
import re

def FULL_SCAN(rule, sql_text=None, plans=[]):
    audit_result = []
    for x in plans:
        object_name, operator_type, cost = x.get('OBJECT_NAME'), x.get('OPERATOR_TYPE'), x.get('COST')
        predicate = 0
        display_x = {k:v for k, v in x.items() if k not in ('OPERATOR_TYPE', 'PREVIOUS_OPERATOR_TYPE')}
        try:
            predicate = int(rule.predicat)
        except:
            pass

        if object_name != None:
            if operator_type == 'TBSCAN':
                if cost > predicate:
                    audit_result.append(display_x)

    return audit_result


def INDEX_ROWS(rule, sql_text=None, plans=[]):
    audit_result = []
    for x in plans:
        object_name, operator_type, cost, previous_operator_type = (
         x.get('OBJECT_NAME'), x.get('OPERATOR_TYPE'), x.get('COST'), x.get('PREVIOUS_OPERATOR_TYPE'))
        predicate = 0
        display_x = {k:v for k, v in x.items() if k not in ('OPERATOR_TYPE', 'PREVIOUS_OPERATOR_TYPE')}
        try:
            predicate = int(rule.predicat)
        except:
            pass

        if object_name != None:
            if operator_type == 'IXSCAN':
                if previous_operator_type == 'TBSCAN':
                    if cost > predicate:
                        audit_result.append(display_x)

    return audit_result
# okay decompiling ./restful/hawkeye/sqlaudit/enum/db2_function_enum.pyc
