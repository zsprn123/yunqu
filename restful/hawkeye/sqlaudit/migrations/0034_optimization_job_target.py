# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./sqlaudit/migrations/0034_optimization_job_target.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 407 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('sqlaudit', '0033_auto_20180119_0007')]
    operations = [
     migrations.AddField(model_name='optimization_job',
       name='target',
       field=models.CharField(max_length=100, null=True))]
# okay decompiling ./restful/hawkeye/sqlaudit/migrations/0034_optimization_job_target.pyc
