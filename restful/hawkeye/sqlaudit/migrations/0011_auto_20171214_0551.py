# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./sqlaudit/migrations/0011_auto_20171214_0551.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 2365 bytes
from __future__ import unicode_literals
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion, uuid

class Migration(migrations.Migration):
    dependencies = [
     ('sqlaudit', '0010_auto_20171213_0954')]
    operations = [
     migrations.CreateModel(name='Audit_SQL_Result',
       fields=[
      (
       'id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
      (
       'created_at', models.DateTimeField(auto_now_add=True)),
      (
       'updated_at', models.DateTimeField(auto_now=True)),
      (
       'sql_id', models.CharField(max_length=100, null=True)),
      (
       'sql_detail', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}, null=True))],
       options={'ordering':('-created_at', ), 
      'abstract':False}),
     migrations.RenameField(model_name='audit_job',
       old_name='end_time',
       new_name='plan_time'),
     migrations.RenameField(model_name='audit_result',
       old_name='checked_num',
       new_name='problem'),
     migrations.RenameField(model_name='audit_result',
       old_name='record_num',
       new_name='total'),
     migrations.RemoveField(model_name='audit_result',
       name='strategy'),
     migrations.AddField(model_name='audit_result',
       name='audit_type',
       field=models.CharField(max_length=100, null=True)),
     migrations.AddField(model_name='audit_result',
       name='name',
       field=models.CharField(max_length=100, null=True)),
     migrations.AddField(model_name='audit_result',
       name='target',
       field=models.CharField(max_length=100, null=True)),
     migrations.AddField(model_name='audit_sql_result',
       name='job',
       field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sqlaudit.Audit_Job'))]
# okay decompiling ./restful/hawkeye/sqlaudit/migrations/0011_auto_20171214_0551.pyc
