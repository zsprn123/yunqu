# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./monitor/migrations/0007_mysql_ash_sql_id.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 469 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('monitor', '0006_database_instance_count')]
    operations = [
     migrations.AddField(model_name='mysql_ash',
       name='sql_id',
       field=models.CharField(max_length=100, null=True))]
# okay decompiling ./restful/hawkeye/monitor/migrations/0007_mysql_ash_sql_id.pyc
