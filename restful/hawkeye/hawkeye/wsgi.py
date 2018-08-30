# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./hawkeye/wsgi.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 397 bytes
"""
WSGI config for hawkeye project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hawkeye.settings.prod')
application = get_wsgi_application()
# okay decompiling ./restful/hawkeye/hawkeye/wsgi.pyc
