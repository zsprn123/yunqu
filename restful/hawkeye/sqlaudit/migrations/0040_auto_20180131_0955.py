# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./sqlaudit/migrations/0040_auto_20180131_0955.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 505 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('sqlaudit', '0039_auto_20180129_1658')]
    operations = [
     migrations.AlterField(model_name='audit_result',
       name='rule',
       field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sqlaudit.Audit_Rule'))]
# okay decompiling ./restful/hawkeye/sqlaudit/migrations/0040_auto_20180131_0955.pyc
