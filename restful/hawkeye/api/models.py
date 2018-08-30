# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/models.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 201 bytes
from django.db import models

class graph_object_json:

    def __init__(self, name, type, data):
        self.name = name
        self.type = type
        self.data = data
# okay decompiling ./restful/hawkeye/api/models.pyc
