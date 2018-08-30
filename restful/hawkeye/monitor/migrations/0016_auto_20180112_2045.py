# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./monitor/migrations/0016_auto_20180112_2045.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 1760 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('monitor', '0015_auto_20180112_2043')]
    operations = [
     migrations.AlterField(model_name='sqlmon_plan',
       name='output_rows',
       field=models.BigIntegerField(null=True)),
     migrations.AlterField(model_name='sqlmon_plan',
       name='physical_read_bytes',
       field=models.BigIntegerField(null=True)),
     migrations.AlterField(model_name='sqlmon_plan',
       name='physical_read_requests',
       field=models.BigIntegerField(null=True)),
     migrations.AlterField(model_name='sqlmon_plan',
       name='physical_write_bytes',
       field=models.BigIntegerField(null=True)),
     migrations.AlterField(model_name='sqlmon_plan',
       name='physical_write_requests',
       field=models.BigIntegerField(null=True)),
     migrations.AlterField(model_name='sqlmon_plan',
       name='plan_cardinality',
       field=models.BigIntegerField(null=True)),
     migrations.AlterField(model_name='sqlmon_plan',
       name='plan_cost',
       field=models.BigIntegerField(null=True)),
     migrations.AlterField(model_name='sqlmon_plan',
       name='plan_temp_space',
       field=models.BigIntegerField(null=True)),
     migrations.AlterField(model_name='sqlmon_plan',
       name='starts',
       field=models.BigIntegerField(null=True))]
# okay decompiling ./restful/hawkeye/monitor/migrations/0016_auto_20180112_2045.pyc
