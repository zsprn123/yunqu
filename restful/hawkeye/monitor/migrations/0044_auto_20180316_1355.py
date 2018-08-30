# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./monitor/migrations/0044_auto_20180316_1355.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 396 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('monitor', '0043_auto_20180301_1153')]
    operations = [
     migrations.AlterField(model_name='database',
       name='retention_days',
       field=models.IntegerField(default=30))]
# okay decompiling ./restful/hawkeye/monitor/migrations/0044_auto_20180316_1355.pyc
