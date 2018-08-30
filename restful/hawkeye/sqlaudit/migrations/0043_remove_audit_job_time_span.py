# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./sqlaudit/migrations/0043_remove_audit_job_time_span.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 335 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('sqlaudit', '0042_auto_20180323_1010')]
    operations = [
     migrations.RemoveField(model_name='audit_job',
       name='time_span')]
# okay decompiling ./restful/hawkeye/sqlaudit/migrations/0043_remove_audit_job_time_span.pyc
