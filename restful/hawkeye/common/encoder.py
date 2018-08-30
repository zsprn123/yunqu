# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./common/encoder.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 262 bytes
from django.core.serializers.json import DjangoJSONEncoder

class BlobJsonEncoder(DjangoJSONEncoder):

    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode('utf-8')
        else:
            return super(BlobJsonEncoder, self).default(obj)
# okay decompiling ./restful/hawkeye/common/encoder.pyc
