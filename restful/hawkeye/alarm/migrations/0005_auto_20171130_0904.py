# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./alarm/migrations/0005_auto_20171130_0904.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 488 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('alarm', '0004_auto_20171130_0727')]
    operations = [
     migrations.AlterField(model_name='warn_config_template',
       name='db_type',
       field=models.CharField(blank=True, max_length=100, null=True))]
# okay decompiling ./restful/hawkeye/alarm/migrations/0005_auto_20171130_0904.pyc
