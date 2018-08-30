# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./heathcheck/migrations/0001_initial.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 1090 bytes
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion, uuid

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     ('monitor', '0039_auto_20180226_2218')]
    operations = [
     migrations.CreateModel(name='Heathcheck_Report',
       fields=[
      (
       'id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
      (
       'created_at', models.DateTimeField(auto_now_add=True)),
      (
       'updated_at', models.DateTimeField(auto_now=True)),
      (
       'report_detail', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}, null=True)),
      (
       'database', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitor.Database'))],
       options={'ordering':('-created_at', ), 
      'abstract':False})]
# okay decompiling ./restful/hawkeye/heathcheck/migrations/0001_initial.pyc
