# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./monitor/migrations/0055_auto_20180703_1439.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 553 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('monitor', '0054_merge_20180627_1526')]
    operations = [
     migrations.AddField(model_name='database',
       name='dg_stats',
       field=models.BooleanField(default=False)),
     migrations.AddField(model_name='database',
       name='hist_sqlmon',
       field=models.BooleanField(default=False))]
# okay decompiling ./restful/hawkeye/monitor/migrations/0055_auto_20180703_1439.pyc
