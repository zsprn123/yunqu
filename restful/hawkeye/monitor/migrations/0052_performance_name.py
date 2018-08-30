# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./monitor/migrations/0052_performance_name.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 411 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('monitor', '0051_auto_20180610_1112')]
    operations = [
     migrations.AddField(model_name='performance',
       name='name',
       field=models.CharField(blank=True, max_length=100, null=True))]
# okay decompiling ./restful/hawkeye/monitor/migrations/0052_performance_name.pyc
