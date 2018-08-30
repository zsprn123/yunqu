# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./monitor/migrations/0011_auto_20171208_0745.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 6722 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('monitor', '0010_auto_20171207_1554')]
    operations = [
     migrations.CreateModel(name='Oracle_SQL',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created_at', models.DateTimeField()),
      (
       'inst_id', models.IntegerField(null=True)),
      (
       'sql_id', models.CharField(max_length=100, null=True)),
      (
       'plan_hash_value', models.IntegerField(null=True)),
      (
       'optimizer_cost', models.IntegerField(null=True)),
      (
       'optimizer_mode', models.CharField(max_length=100, null=True)),
      (
       'module', models.CharField(max_length=100, null=True)),
      (
       'action', models.CharField(max_length=100, null=True)),
      (
       'sql_profile', models.CharField(max_length=100, null=True)),
      (
       'force_matching_signature', models.IntegerField(null=True)),
      (
       'parsing_schema_name', models.CharField(max_length=100, null=True)),
      (
       'fetches_delta', models.IntegerField(null=True)),
      (
       'end_of_fetch_count_delta', models.IntegerField(null=True)),
      (
       'sorts_delta', models.IntegerField(null=True)),
      (
       'executions_delta', models.IntegerField(null=True)),
      (
       'px_servers_execs_delta', models.IntegerField(null=True)),
      (
       'disk_reads_delta', models.IntegerField(null=True)),
      (
       'buffer_gets_delta', models.IntegerField(null=True)),
      (
       'rows_processed_delta', models.IntegerField(null=True)),
      (
       'cpu_time_delta', models.IntegerField(null=True)),
      (
       'elapsed_time_delta', models.IntegerField(null=True)),
      (
       'database', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitor.Database'))]),
     migrations.CreateModel(name='Oracle_SQL_Plan',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created_at', models.DateTimeField()),
      (
       'inst_id', models.IntegerField(null=True)),
      (
       'sql_id', models.CharField(max_length=100, null=True)),
      (
       'plan_hash_value', models.IntegerField(null=True)),
      (
       'operation', models.CharField(max_length=100, null=True)),
      (
       'options', models.CharField(max_length=100, null=True)),
      (
       'object_owner', models.CharField(max_length=100, null=True)),
      (
       'object_name', models.CharField(max_length=100, null=True)),
      (
       'object_type', models.CharField(max_length=100, null=True)),
      (
       'plan_line_id', models.IntegerField(null=True)),
      (
       'parent_id', models.IntegerField(null=True)),
      (
       'depth', models.IntegerField(null=True)),
      (
       'position', models.IntegerField(null=True)),
      (
       'cost', models.IntegerField(null=True)),
      (
       'cardinality', models.IntegerField(null=True)),
      (
       'partition_id', models.IntegerField(null=True)),
      (
       'access_predicates', models.CharField(max_length=100, null=True)),
      (
       'filter_predicates', models.CharField(max_length=100, null=True)),
      (
       'database', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitor.Database'))]),
     migrations.CreateModel(name='SQLMON_Plan',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created_at', models.DateTimeField()),
      (
       'inst_id', models.IntegerField(null=True)),
      (
       'status', models.CharField(max_length=100, null=True)),
      (
       'first_refresh_time', models.DateTimeField(blank=True, null=True)),
      (
       'last_refresh_time', models.DateTimeField(blank=True, null=True)),
      (
       'sid', models.IntegerField(null=True)),
      (
       'sql_id', models.CharField(max_length=100, null=True)),
      (
       'sql_exec_start', models.DateTimeField(blank=True, null=True)),
      (
       'sql_exec_id', models.IntegerField(null=True)),
      (
       'sql_plan_hash_value', models.IntegerField(null=True)),
      (
       'plan_parent_id', models.IntegerField(null=True)),
      (
       'plan_line_id', models.IntegerField(null=True)),
      (
       'plan_operation', models.CharField(max_length=100, null=True)),
      (
       'plan_options', models.CharField(max_length=100, null=True)),
      (
       'plan_object_owner', models.CharField(max_length=100, null=True)),
      (
       'plan_object_name', models.CharField(max_length=100, null=True)),
      (
       'plan_object_type', models.CharField(max_length=100, null=True)),
      (
       'plan_depth', models.IntegerField(null=True)),
      (
       'plan_position', models.IntegerField(null=True)),
      (
       'plan_cost', models.IntegerField(null=True)),
      (
       'plan_cardinality', models.IntegerField(null=True)),
      (
       'plan_temp_space', models.IntegerField(null=True)),
      (
       'starts', models.IntegerField(null=True)),
      (
       'output_rows', models.IntegerField(null=True)),
      (
       'physical_read_requests', models.IntegerField(null=True)),
      (
       'physical_read_bytes', models.IntegerField(null=True)),
      (
       'physical_write_requests', models.IntegerField(null=True)),
      (
       'physical_write_bytes', models.IntegerField(null=True)),
      (
       'database', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitor.Database'))]),
     migrations.AlterIndexTogether(name='sqlmon_plan',
       index_together=set([('database', 'sql_id', 'sql_exec_id'), ('database', 'created_at')])),
     migrations.AlterIndexTogether(name='oracle_sql_plan',
       index_together=set([('database', 'sql_id'), ('database', 'created_at')])),
     migrations.AlterIndexTogether(name='oracle_sql',
       index_together=set([('database', 'sql_id'), ('database', 'created_at')]))]
# okay decompiling ./restful/hawkeye/monitor/migrations/0011_auto_20171208_0745.pyc
