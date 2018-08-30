# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./common/middleware.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 902 bytes
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from .yunquAuthorizationUtil import get_lisence_info

class YunquAuthorizationCheckMiddleware(MiddlewareMixin):
    """
    Middleware that handles whether license validates
    """

    def process_request(self, request):
        login_url = '/api/v1/auth/login/'
        license_info_url = ['/api/v1/auth/license_info/', '/api/v1/auth/grant_license/']
        if request.path_info in login_url or request.path_info in license_info_url:
            return
        info = get_lisence_info()
        if not info.get('certificated', False) or info.get('days') is not None and info['days'] <= 0:
            return redirect('http://localhost:3000/activation/')
# okay decompiling ./restful/hawkeye/common/middleware.pyc
