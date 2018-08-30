# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./heathcheck/migrations/0004_auto_20180228_1113.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 417 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('heathcheck', '0003_heathcheck_report_status')]
    operations = [
     migrations.AlterField(model_name='heathcheck_report',
       name='status',
       field=models.IntegerField(blank=True, null=True))]
# okay decompiling ./restful/hawkeye/heathcheck/migrations/0004_auto_20180228_1113.pyc
