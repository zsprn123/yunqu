# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./monitor/migrations/0009_auto_20171120_0656.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 478 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('monitor', '0008_auto_20171110_0902')]
    operations = [
     migrations.AlterField(model_name='database',
       name='instance_id_list',
       field=models.CharField(default='1', max_length=1000))]
# okay decompiling ./restful/hawkeye/monitor/migrations/0009_auto_20171120_0656.pyc
