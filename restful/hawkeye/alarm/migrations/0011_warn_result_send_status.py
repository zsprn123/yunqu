# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./alarm/migrations/0011_warn_result_send_status.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 493 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('alarm', '0010_remove_warn_result_send_status')]
    operations = [
     migrations.AddField(model_name='warn_result',
       name='send_status',
       field=models.CharField(blank=True, max_length=200, null=True))]
# okay decompiling ./restful/hawkeye/alarm/migrations/0011_warn_result_send_status.pyc
