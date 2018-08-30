# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./sqlaudit/migrations/0047_sql_perf_diff.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 1713 bytes
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion, uuid

class Migration(migrations.Migration):
    dependencies = [
     ('monitor', '0055_auto_20180703_1439'),
     ('sqlaudit', '0046_auto_20180326_2128')]
    operations = [
     migrations.CreateModel(name='SQL_Perf_Diff',
       fields=[
      (
       'id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
      (
       'created_at', models.DateTimeField(auto_now_add=True)),
      (
       'updated_at', models.DateTimeField(auto_now=True)),
      (
       'name', models.CharField(max_length=10000000, null=True)),
      (
       'sql_id_list', models.CharField(max_length=10000000, null=True)),
      (
       'snapshot_begin_time', models.DateTimeField(null=True)),
      (
       'snapshot_end_time', models.DateTimeField(null=True)),
      (
       'begin_result', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}, null=True)),
      (
       'end_result', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}, null=True)),
      (
       'summary_result', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}, null=True)),
      (
       'status', models.IntegerField(default=1)),
      (
       'database', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitor.Database'))],
       options={'ordering':('-created_at', ), 
      'abstract':False})]
# okay decompiling ./restful/hawkeye/sqlaudit/migrations/0047_sql_perf_diff.pyc
