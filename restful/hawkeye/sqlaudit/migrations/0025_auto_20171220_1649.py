# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./sqlaudit/migrations/0025_auto_20171220_1649.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 759 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('sqlaudit', '0024_audit_result_rule')]
    operations = [
     migrations.RemoveField(model_name='audit_strategy',
       name='weight'),
     migrations.AddField(model_name='audit_rule',
       name='risky',
       field=models.CharField(default='', max_length=1000, null=True)),
     migrations.AddField(model_name='audit_rule',
       name='weight',
       field=models.IntegerField(default=4, null=True))]
# okay decompiling ./restful/hawkeye/sqlaudit/migrations/0025_auto_20171220_1649.pyc
