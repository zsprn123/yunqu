# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./hawkeye/asgi.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 155 bytes
import os, channels.asgi
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hawkeye.settings.prod')
channel_layer = channels.asgi.get_channel_layer()
# okay decompiling ./restful/hawkeye/hawkeye/asgi.pyc
