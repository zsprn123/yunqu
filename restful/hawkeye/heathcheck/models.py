# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./heathcheck/models.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 563 bytes
from django.contrib.postgres.fields import JSONField
from django.db import models
from common.models import CoreModel
from monitor.models import Database

class Heathcheck_Report(CoreModel):
    database = models.ForeignKey(Database, blank=True, null=True, on_delete=models.CASCADE)
    report_detail = JSONField(null=True, blank=True, default={})
    status_message = models.CharField(max_length=2000, null=True, blank=True)
    status = models.IntegerField(null=True, blank=True)
# okay decompiling ./restful/hawkeye/heathcheck/models.pyc
