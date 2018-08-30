# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./sqlaudit/migrations/0039_auto_20180129_1658.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 378 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('sqlaudit', '0038_auto_20180129_1436')]
    operations = [
     migrations.RenameField(model_name='audit_job',
       old_name='static_job',
       new_name='is_static_job')]
# okay decompiling ./restful/hawkeye/sqlaudit/migrations/0039_auto_20180129_1658.pyc
