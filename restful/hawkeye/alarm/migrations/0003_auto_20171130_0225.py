# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./alarm/migrations/0003_auto_20171130_0225.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 1538 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
     ('alarm', '0002_auto_20171128_1016')]
    operations = [
     migrations.AddField(model_name='receiver',
       name='created_at',
       field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
       preserve_default=False),
     migrations.AddField(model_name='receiver',
       name='updated_at',
       field=models.DateTimeField(auto_now=True)),
     migrations.AddField(model_name='warn_result',
       name='created_at',
       field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
       preserve_default=False),
     migrations.AddField(model_name='warn_result',
       name='updated_at',
       field=models.DateTimeField(auto_now=True)),
     migrations.AddField(model_name='warn_send_status',
       name='created_at',
       field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
       preserve_default=False),
     migrations.AddField(model_name='warn_send_status',
       name='updated_at',
       field=models.DateTimeField(auto_now=True))]
# okay decompiling ./restful/hawkeye/alarm/migrations/0003_auto_20171130_0225.pyc
