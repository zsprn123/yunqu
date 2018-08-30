# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./monitor/migrations/0012_auto_20171210_1257.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 479 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('monitor', '0011_auto_20171208_0745')]
    operations = [
     migrations.AlterField(model_name='database',
       name='num_sqlmon_per_minute',
       field=models.IntegerField(default=10, null=True))]
# okay decompiling ./restful/hawkeye/monitor/migrations/0012_auto_20171210_1257.pyc
