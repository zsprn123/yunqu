# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./sqlaudit/migrations/0042_auto_20180323_1010.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 723 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('sqlaudit', '0041_auto_20180131_1012')]
    operations = [
     migrations.AddField(model_name='audit_job',
       name='snapshot_begin_time',
       field=models.DateTimeField(null=True)),
     migrations.AddField(model_name='audit_job',
       name='snapshot_end_time',
       field=models.DateTimeField(null=True)),
     migrations.AddField(model_name='audit_job',
       name='time_span',
       field=models.DateTimeField(null=True))]
# okay decompiling ./restful/hawkeye/sqlaudit/migrations/0042_auto_20180323_1010.pyc
