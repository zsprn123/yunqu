# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./hosts/models.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 1027 bytes
from django.contrib.postgres.fields import JSONField
from django.db import models
from common.aes import aes_decode
from common.models import CoreModel

class Host(CoreModel):
    address = models.CharField(max_length=100, null=True, unique=True)
    port = models.IntegerField(default=22)
    username = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=100, null=True)
    ssh_key = models.CharField(max_length=5000, null=True)
    disabled = models.BooleanField(default=False)

    def get_password(self):
        if not self.password:
            return ''
        else:
            return aes_decode(self.password)


class HostDetail(CoreModel):
    name = models.CharField(max_length=100, null=True)
    value = JSONField(null=True, blank=True, default={})
    host = models.ForeignKey('hosts.Host', blank=True, null=True, on_delete=models.CASCADE)


class LogMatchKey(CoreModel):
    value = models.CharField(max_length=300)
    db_type = models.CharField(max_length=100)
# okay decompiling ./restful/hawkeye/hosts/models.pyc
