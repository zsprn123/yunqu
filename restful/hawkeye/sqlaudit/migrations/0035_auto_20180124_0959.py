# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./sqlaudit/migrations/0035_auto_20180124_0959.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 780 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('sqlaudit', '0034_optimization_job_target')]
    operations = [
     migrations.RenameField(model_name='optimization_job',
       old_name='sql_id',
       new_name='detail_id'),
     migrations.AddField(model_name='optimization_job',
       name='detail_name',
       field=models.CharField(blank=True, max_length=1000, null=True)),
     migrations.AddField(model_name='optimization_job',
       name='optimized_detail_id',
       field=models.CharField(blank=True, max_length=1000, null=True))]
# okay decompiling ./restful/hawkeye/sqlaudit/migrations/0035_auto_20180124_0959.pyc
