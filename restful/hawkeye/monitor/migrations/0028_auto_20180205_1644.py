# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./monitor/migrations/0028_auto_20180205_1644.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 849 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('monitor', '0027_space_used_pct')]
    operations = [
     migrations.RenameField(model_name='db2_lock_history',
       old_name='hld_application_name',
       new_name='b_blocker'),
     migrations.RenameField(model_name='db2_lock_history',
       old_name='lock_name',
       new_name='b_res'),
     migrations.RemoveField(model_name='db2_lock_history',
       name='req_application_handle'),
     migrations.AddField(model_name='db2_lock_history',
       name='w_waiter',
       field=models.CharField(max_length=1000, null=True))]
# okay decompiling ./restful/hawkeye/monitor/migrations/0028_auto_20180205_1644.pyc
