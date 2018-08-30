# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./authx/authentication.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 457 bytes
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from django.conf import settings

class JSONWebTokenAuthenticationQS(BaseJSONWebTokenAuthentication):

    def get_jwt_value(self, request):
        return request.query_params.get(settings.QS_JWT_KEY)


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        pass
# okay decompiling ./restful/hawkeye/authx/authentication.pyc
