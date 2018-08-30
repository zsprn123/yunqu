# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./monitor/migrations/0036_auto_20180226_1405.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 564 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('monitor', '0035_auto_20180226_1403')]
    operations = [
     migrations.RenameField(model_name='mysql_ash',
       old_name='conn_id',
       new_name='session_id'),
     migrations.AlterIndexTogether(name='mysql_ash',
       index_together={
      ('session_id', 'created_at'), ('database', 'created_at'), ('sql_id', 'created_at')})]
# okay decompiling ./restful/hawkeye/monitor/migrations/0036_auto_20180226_1405.pyc
