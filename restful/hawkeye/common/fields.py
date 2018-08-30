# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./common/fields.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 922 bytes
from django.db.models.fields import BinaryField
from jsonfield.fields import JSONCharField
__special_binary_prefix = True
try:
    import pymysql
except ImportError:
    __special_binary_prefix = False

def need_special_binary_prefix():
    return __special_binary_prefix


class XBinaryField(BinaryField):

    def get_placeholder(self, value, compiler, connection):
        if need_special_binary_prefix():
            return '%s'
        else:
            return super().get_placeholder(value, compiler, connection)


class XJSONCharField(JSONCharField):

    def pre_init(self, value, obj):
        if self.blank:
            if not value:
                return
            return super().pre_init(value, obj)
# okay decompiling ./restful/hawkeye/common/fields.pyc
