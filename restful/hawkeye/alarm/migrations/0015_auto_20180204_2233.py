# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./alarm/migrations/0015_auto_20180204_2233.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 704 bytes
import django.contrib.postgres.fields.jsonb
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('alarm', '0014_remove_warn_result_description')]
    operations = [
     migrations.AddField(model_name='warn_config',
       name='optional',
       field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}, null=True)),
     migrations.AddField(model_name='warn_config_template',
       name='optional',
       field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}, null=True))]
# okay decompiling ./restful/hawkeye/alarm/migrations/0015_auto_20180204_2233.pyc
