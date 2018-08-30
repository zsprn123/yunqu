# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./sqlaudit/migrations/0046_auto_20180326_2128.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 415 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('sqlaudit', '0045_auto_20180326_2126')]
    operations = [
     migrations.AlterField(model_name='audit_job',
       name='schema',
       field=models.CharField(blank=True, max_length=5000, null=True))]
# okay decompiling ./restful/hawkeye/sqlaudit/migrations/0046_auto_20180326_2128.pyc
