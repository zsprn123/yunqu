# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./sqlaudit/migrations/0003_auto_20171211_0227.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 576 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('sqlaudit', '0002_auto_20171211_0212')]
    operations = [
     migrations.AlterField(model_name='audit_strategy',
       name='predicate',
       field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sqlaudit.Audit_Rule'))]
# okay decompiling ./restful/hawkeye/sqlaudit/migrations/0003_auto_20171211_0227.pyc
