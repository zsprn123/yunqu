# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./sqlaudit/migrations/0033_auto_20180119_0007.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 511 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('sqlaudit', '0032_optimization_job_database')]
    operations = [
     migrations.RenameField(model_name='audit_sql_result',
       old_name='sql_detail',
       new_name='detail'),
     migrations.AlterIndexTogether(name='audit_sql_result',
       index_together={
      ('job', )})]
# okay decompiling ./restful/hawkeye/sqlaudit/migrations/0033_auto_20180119_0007.pyc
