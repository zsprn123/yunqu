# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./monitor/migrations/0042_auto_20180301_0959.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 612 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('monitor', '0041_auto_20180301_0832')]
    operations = [
     migrations.RemoveField(model_name='database',
       name='conn_type'),
     migrations.RemoveField(model_name='database',
       name='remote_port'),
     migrations.AddField(model_name='database',
       name='last_archived_date',
       field=models.DateField(null=True))]
# okay decompiling ./restful/hawkeye/monitor/migrations/0042_auto_20180301_0959.pyc
