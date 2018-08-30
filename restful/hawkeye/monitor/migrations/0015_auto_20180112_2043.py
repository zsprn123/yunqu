# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./monitor/migrations/0015_auto_20180112_2043.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 1112 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('monitor', '0014_auto_20180111_2248')]
    operations = [
     migrations.AlterField(model_name='sqlmon_plan',
       name='first_refresh_time',
       field=models.CharField(max_length=100, null=True)),
     migrations.AlterField(model_name='sqlmon_plan',
       name='last_refresh_time',
       field=models.CharField(max_length=100, null=True)),
     migrations.AlterField(model_name='sqlmon_plan',
       name='sql_exec_id',
       field=models.BigIntegerField(null=True)),
     migrations.AlterField(model_name='sqlmon_plan',
       name='sql_exec_start',
       field=models.CharField(max_length=100, null=True)),
     migrations.AlterField(model_name='sqlmon_plan',
       name='sql_plan_hash_value',
       field=models.BigIntegerField(null=True))]
# okay decompiling ./restful/hawkeye/monitor/migrations/0015_auto_20180112_2043.pyc
