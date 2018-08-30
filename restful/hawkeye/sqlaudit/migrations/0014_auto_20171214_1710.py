# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./sqlaudit/migrations/0014_auto_20171214_1710.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 441 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('sqlaudit', '0013_remove_audit_job_sql_set')]
    operations = [
     migrations.RenameField(model_name='audit_job',
       old_name='max_row',
       new_name='max_rows')]
# okay decompiling ./restful/hawkeye/sqlaudit/migrations/0014_auto_20171214_1710.pyc
