# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./hawkeye/views.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 180 bytes
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def index(request):
    return Response({'msg': 'Hello Dashboard'})
# okay decompiling ./restful/hawkeye/hawkeye/views.pyc
