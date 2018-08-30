# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./monitor/migrations/0034_auto_20180225_2021.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 1005 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('monitor', '0033_mssql_ash_time')]
    operations = [
     migrations.RenameField(model_name='mssql_lock_history',
       old_name='w_waitresource',
       new_name='b_res'),
     migrations.RemoveField(model_name='mssql_lock_history',
       name='b_sessionid'),
     migrations.RemoveField(model_name='mssql_lock_history',
       name='w_sessionid'),
     migrations.AddField(model_name='mssql_lock_history',
       name='b_blocker',
       field=models.CharField(blank=True, max_length=100, null=True)),
     migrations.AddField(model_name='mssql_lock_history',
       name='w_waiter',
       field=models.CharField(blank=True, max_length=100, null=True))]
# okay decompiling ./restful/hawkeye/monitor/migrations/0034_auto_20180225_2021.pyc
