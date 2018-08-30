# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./sqlaudit/migrations/0001_initial.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 6039 bytes
from __future__ import unicode_literals
from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion, uuid

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('monitor', '0012_auto_20171210_1257')]
    operations = [
     migrations.CreateModel(name='Audit_Job',
       fields=[
      (
       'id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
      (
       'created_at', models.DateTimeField(auto_now_add=True)),
      (
       'updated_at', models.DateTimeField(auto_now=True)),
      (
       'name', models.CharField(max_length=100, null=True)),
      (
       'strategy', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}, null=True)),
      (
       'schema', models.CharField(blank=True, max_length=100, null=True)),
      (
       'begin_time', models.DateTimeField(null=True)),
      (
       'end_time', models.DateTimeField(null=True)),
      (
       'finish_at', models.DateTimeField(null=True)),
      (
       'timeout', models.IntegerField(null=True)),
      (
       'max_row', models.IntegerField(null=True)),
      (
       'status', models.CharField(blank=True, max_length=100, null=True)),
      (
       'sql_set', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}, null=True)),
      (
       'compare_audit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sqlaudit.Audit_Job')),
      (
       'database', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitor.Database'))],
       options={'ordering':('-created_at', ), 
      'abstract':False}),
     migrations.CreateModel(name='Audit_Result',
       fields=[
      (
       'id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
      (
       'created_at', models.DateTimeField(auto_now_add=True)),
      (
       'updated_at', models.DateTimeField(auto_now=True)),
      (
       'score', models.CharField(blank=True, max_length=100, null=True)),
      (
       'record_num', models.IntegerField(null=True)),
      (
       'checked_num', models.IntegerField(null=True)),
      (
       'problem_rate', models.CharField(blank=True, max_length=1000, null=True)),
      (
       'result', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}, null=True)),
      (
       'job', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sqlaudit.Audit_Job'))],
       options={'ordering':('-created_at', ), 
      'abstract':False}),
     migrations.CreateModel(name='Audit_Strategy',
       fields=[
      (
       'id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
      (
       'created_at', models.DateTimeField(auto_now_add=True)),
      (
       'updated_at', models.DateTimeField(auto_now=True)),
      (
       'name', models.CharField(max_length=100, null=True)),
      (
       'description', models.CharField(max_length=100, null=True)),
      (
       'weight', models.CharField(max_length=100, null=True)),
      (
       'predicate', models.CharField(max_length=1000, null=True)),
      (
       'status', models.CharField(max_length=100, null=True)),
      (
       'remarks', models.CharField(max_length=1000, null=True)),
      (
       'is_static_rule', models.CharField(max_length=100, null=True)),
      (
       'database', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitor.Database'))],
       options={'ordering':('-created_at', ), 
      'abstract':False}),
     migrations.CreateModel(name='Optimization_Job',
       fields=[
      (
       'id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
      (
       'created_at', models.DateTimeField(auto_now_add=True)),
      (
       'updated_at', models.DateTimeField(auto_now=True)),
      (
       'name', models.CharField(max_length=100, null=True)),
      (
       'status', models.CharField(blank=True, max_length=100, null=True)),
      (
       'schema', models.CharField(blank=True, max_length=100, null=True)),
      (
       'deadline', models.DateTimeField()),
      (
       'closed_at', models.DateTimeField()),
      (
       'sql_text', models.CharField(blank=True, max_length=1000, null=True)),
      (
       'sql_id', models.CharField(blank=True, max_length=1000, null=True)),
      (
       'optimized_sql_text', models.CharField(blank=True, max_length=1000, null=True)),
      (
       'optimized_sql_id', models.CharField(blank=True, max_length=1000, null=True)),
      (
       'optimize_description', models.CharField(blank=True, max_length=5000, null=True)),
      (
       'audit_job', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sqlaudit.Audit_Job')),
      (
       'owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL))],
       options={'ordering':('-created_at', ), 
      'abstract':False}),
     migrations.AddField(model_name='audit_result',
       name='strategy',
       field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sqlaudit.Audit_Strategy'))]
# okay decompiling ./restful/hawkeye/sqlaudit/migrations/0001_initial.pyc
