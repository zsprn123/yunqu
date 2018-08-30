# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./alarm/models.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 4648 bytes
import os
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models import signals
from common.models import CoreModel
from django.contrib.postgres.fields import JSONField

class Receiver(models.Model):
    name = models.CharField(max_length=1000, blank=True, null=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Warn_Config_Template(CoreModel):
    category = models.CharField(max_length=100, blank=True, null=True, verbose_name='')
    warn_threshold = models.CharField(max_length=1000, blank=True, null=True, verbose_name='warn ')
    critical_threshold = models.CharField(max_length=1000, blank=True, null=True, verbose_name='critical ')
    warning_interval = models.CharField(max_length=1000, blank=True, null=True, verbose_name='', default='300')
    pre_warning_times = models.CharField(max_length=100, blank=True, null=True, verbose_name='', default='0')
    description = models.CharField(max_length=1000, blank=True, null=True)
    db_type = models.CharField(max_length=100, blank=True, null=True)
    status = models.BooleanField(default=True)
    receivers = models.ManyToManyField(Receiver, blank=True)
    optional = JSONField(null=True, blank=True, default={})


class Warn_Config(CoreModel):
    category = models.CharField(max_length=100, blank=True, null=True, verbose_name='')
    warn_threshold = models.CharField(max_length=1000, blank=True, null=True, verbose_name='warn ')
    critical_threshold = models.CharField(max_length=1000, blank=True, null=True, verbose_name='critical ')
    warning_interval = models.CharField(max_length=1000, blank=True, null=True, verbose_name='', default='300')
    pre_warning_times = models.CharField(max_length=100, blank=True, null=True, verbose_name='', default='0')
    description = models.CharField(max_length=1000, blank=True, null=True)
    status = models.BooleanField(default=True)
    database = models.ForeignKey('monitor.Database', blank=True, null=True, on_delete=models.CASCADE)
    host = models.ForeignKey('hosts.Host', blank=True, null=True, on_delete=models.CASCADE)
    receivers = models.ManyToManyField(Receiver, blank=True)
    template = models.ForeignKey('Warn_Config_Template', blank=True, null=True, on_delete=models.CASCADE)
    optional = JSONField(null=True, blank=True, default={})


class Warn_Send_Status(models.Model):
    status = models.CharField(max_length=1000, blank=True, null=True)
    receiver = models.ForeignKey('Receiver', blank=True, null=True, on_delete=models.CASCADE)
    send_type = models.CharField(max_length=1000, blank=True, null=True)
    exception = models.CharField(max_length=10000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Warn_Result(models.Model):
    warn = models.ForeignKey('Warn_Config', blank=True, null=True, on_delete=models.CASCADE)
    send_status = models.CharField(max_length=200, blank=True, null=True)
    warn_message = models.TextField(blank=True, null=True)
    database = models.ForeignKey('monitor.Database', blank=True, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    link = JSONField(null=True, blank=True, default={})

    class Meta:
        ordering = ('-created_at', )


class Mail_Config(models.Model):
    host = models.CharField(max_length=50, blank=True, null=True)
    port = models.IntegerField(blank=True, default=25)
    username = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)
    address = models.EmailField(blank=True, null=True)
    use_tls = models.BooleanField(default=False)
    use_ssl = models.BooleanField(default=False)


def export_warn_log(**kwargs):
    instance = kwargs.get('instance')
    op = os.path.exists('/home/hawkeye/hawkeye_logs/warn_result.txt')'xt''at'
    with open('/home/hawkeye/hawkeye_logs/warn_result.txt', op, encoding='utf8') as (f):
        f.write(f'''[{(str(instance.created_at))}]:{(str(instance.warn_message))},:{(str(instance.database.alias))}
''')
# okay decompiling ./restful/hawkeye/alarm/models.pyc
