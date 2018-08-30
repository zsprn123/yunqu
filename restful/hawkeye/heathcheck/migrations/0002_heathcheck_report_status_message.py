# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./heathcheck/migrations/0002_heathcheck_report_status_message.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 420 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('heathcheck', '0001_initial')]
    operations = [
     migrations.AddField(model_name='heathcheck_report',
       name='status_message',
       field=models.CharField(blank=True, max_length=2000, null=True))]
# okay decompiling ./restful/hawkeye/heathcheck/migrations/0002_heathcheck_report_status_message.pyc
