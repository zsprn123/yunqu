# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./sqlaudit/migrations/0032_optimization_job_database.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 621 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('monitor', '0012_auto_20171210_1257'),
     ('sqlaudit', '0031_merge_20171229_1021')]
    operations = [
     migrations.AddField(model_name='optimization_job',
       name='database',
       field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitor.Database'))]
# okay decompiling ./restful/hawkeye/sqlaudit/migrations/0032_optimization_job_database.pyc
