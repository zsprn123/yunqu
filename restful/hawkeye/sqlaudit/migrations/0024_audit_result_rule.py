# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./sqlaudit/migrations/0024_audit_result_rule.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 568 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('sqlaudit', '0023_merge_20171218_1800')]
    operations = [
     migrations.AddField(model_name='audit_result',
       name='rule',
       field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sqlaudit.Audit_Rule'))]
# okay decompiling ./restful/hawkeye/sqlaudit/migrations/0024_audit_result_rule.pyc
