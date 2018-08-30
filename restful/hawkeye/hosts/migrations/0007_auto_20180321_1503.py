# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./hosts/migrations/0007_auto_20180321_1503.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 644 bytes
import django.contrib.postgres.fields.jsonb
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('hosts', '0006_auto_20180319_0929')]
    operations = [
     migrations.RemoveField(model_name='memory',
       name='host'),
     migrations.AlterField(model_name='hostdetail',
       name='value',
       field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}, null=True)),
     migrations.DeleteModel(name='Memory')]
# okay decompiling ./restful/hawkeye/hosts/migrations/0007_auto_20180321_1503.pyc
