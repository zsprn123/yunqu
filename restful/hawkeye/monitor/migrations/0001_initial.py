# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./monitor/migrations/0001_initial.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 11584 bytes
from __future__ import unicode_literals
from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion, uuid

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name='Database',
       fields=[
      (
       'id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
      (
       'created_at', models.DateTimeField(auto_now_add=True)),
      (
       'updated_at', models.DateTimeField(auto_now=True)),
      (
       'db_type', models.CharField(max_length=100, null=True)),
      (
       'username', models.CharField(max_length=100, null=True)),
      (
       'password', models.CharField(max_length=100, null=True)),
      (
       'hostname', models.CharField(max_length=100, null=True)),
      (
       'port', models.IntegerField(null=True)),
      (
       'db_name', models.CharField(max_length=100, null=True)),
      (
       'alias', models.CharField(default='', max_length=100, null=True)),
      (
       'encoding', models.CharField(blank=True, default='', max_length=1000, null=True)),
      (
       'translate_map', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}, null=True)),
      (
       'role', models.CharField(default='PRIMARY', max_length=100)),
      (
       'num_sqlmon_per_minute', models.IntegerField(default=2, null=True)),
      (
       'disabled', models.BooleanField(default=False)),
      (
       'retention_days', models.IntegerField(default=90)),
      (
       'remote_port', models.IntegerField(blank=True, default=22, null=True)),
      (
       'conn_type', models.CharField(blank=True, default='SSH', max_length=32, null=True)),
      (
       'version', models.CharField(blank=True, max_length=32, null=True)),
      (
       'owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL))],
       options={'permissions': (('view_database', 'Can view database'), )}),
     migrations.CreateModel(name='DB2_ASH',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created_at', models.DateTimeField()),
      (
       'db_name', models.CharField(max_length=100, null=True)),
      (
       'agent_id', models.BigIntegerField(null=True)),
      (
       'appl_id', models.CharField(max_length=100, null=True)),
      (
       'appl_name', models.CharField(max_length=100, null=True)),
      (
       'appl_status', models.CharField(max_length=100, null=True)),
      (
       'authid', models.CharField(max_length=100, null=True)),
      (
       'activity_state', models.CharField(max_length=100, null=True)),
      (
       'activity_type', models.CharField(max_length=100, null=True)),
      (
       'elapsed_time_sec', models.BigIntegerField(null=True)),
      (
       'total_cpu_time', models.BigIntegerField(null=True)),
      (
       'rows_read', models.BigIntegerField(null=True)),
      (
       'rows_returned', models.BigIntegerField(null=True)),
      (
       'query_cost_estimate', models.BigIntegerField(null=True)),
      (
       'direct_reads', models.BigIntegerField(null=True)),
      (
       'direct_writes', models.BigIntegerField(null=True)),
      (
       'stmt_text', models.TextField(max_length=100000, null=True)),
      (
       'executable_id', models.CharField(max_length=100, null=True)),
      (
       'database', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitor.Database'))]),
     migrations.CreateModel(name='MSSQL_ASH',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created_at', models.DateTimeField()),
      (
       'session_id', models.IntegerField()),
      (
       'start_time', models.DateTimeField(null=True)),
      (
       'status', models.CharField(max_length=30, null=True)),
      (
       'command', models.CharField(max_length=32, null=True)),
      (
       'db_name', models.CharField(max_length=128, null=True)),
      (
       'login_name', models.CharField(max_length=128, null=True)),
      (
       'host_name', models.CharField(max_length=128, null=True)),
      (
       'program_name', models.CharField(max_length=128, null=True)),
      (
       'blocking_session_id', models.IntegerField(null=True)),
      (
       'wait_type', models.CharField(max_length=60, null=True)),
      (
       'wait_time', models.IntegerField(null=True)),
      (
       'wait_resource', models.CharField(max_length=256, null=True)),
      (
       'total_elapsed_time', models.IntegerField(null=True)),
      (
       'row_count', models.BigIntegerField(null=True)),
      (
       'sqltext', models.TextField(max_length=100000, null=True)),
      (
       'sql_handle', models.TextField(max_length=100000, null=True)),
      (
       'client_net_address', models.CharField(max_length=128, null=True)),
      (
       'linked_ip', models.CharField(max_length=128, null=True)),
      (
       'linked_spid', models.BigIntegerField(null=True)),
      (
       'database', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitor.Database'))]),
     migrations.CreateModel(name='MySQL_ASH',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created_at', models.DateTimeField()),
      (
       'conn_id', models.IntegerField()),
      (
       'user', models.CharField(max_length=100)),
      (
       'host', models.CharField(max_length=100)),
      (
       'db', models.CharField(max_length=100, null=True)),
      (
       'command', models.CharField(max_length=100)),
      (
       'time', models.IntegerField()),
      (
       'state', models.CharField(max_length=100, null=True)),
      (
       'wait_class', models.CharField(default='Others', max_length=100)),
      (
       'info', models.TextField(max_length=100000, null=True)),
      (
       'database', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitor.Database'))]),
     migrations.CreateModel(name='Oracle_ASH',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created_at', models.DateTimeField()),
      (
       'inst_id', models.IntegerField(null=True)),
      (
       'sid', models.IntegerField(null=True)),
      (
       'serial', models.IntegerField(null=True)),
      (
       'username', models.CharField(max_length=100, null=True)),
      (
       'machine', models.CharField(max_length=100, null=True)),
      (
       'program', models.CharField(max_length=100, null=True)),
      (
       'status', models.CharField(max_length=100, null=True)),
      (
       'command', models.CharField(max_length=100, null=True)),
      (
       'sql_hash_value', models.BigIntegerField(null=True)),
      (
       'sql_id', models.CharField(max_length=100, null=True)),
      (
       'sql_plan_hash_value', models.BigIntegerField(null=True)),
      (
       'event', models.CharField(default='f', max_length=100, null=True)),
      (
       'p1', models.BigIntegerField(null=True)),
      (
       'p2', models.BigIntegerField(null=True)),
      (
       'p3', models.BigIntegerField(null=True)),
      (
       'wait_class', models.CharField(max_length=100, null=True)),
      (
       'module', models.CharField(max_length=1000, null=True)),
      (
       'action', models.CharField(max_length=1000, null=True)),
      (
       'service_name', models.CharField(max_length=1000, null=True)),
      (
       'plsql_object_name', models.CharField(max_length=1000, null=True)),
      (
       'plsql_entry_object_name', models.CharField(max_length=1000, null=True)),
      (
       'sqltext', models.TextField(max_length=100000, null=True)),
      (
       'database', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitor.Database'))]),
     migrations.CreateModel(name='Performance',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created_at', models.DateTimeField()),
      (
       'inst_id', models.IntegerField(default=0, null=True)),
      (
       'name', models.CharField(blank=True, max_length=100, null=True)),
      (
       'value', models.FloatField()),
      (
       'database', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitor.Database'))]),
     migrations.CreateModel(name='Postgres_ASH',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created_at', models.DateTimeField()),
      (
       'pid', models.IntegerField(null=True)),
      (
       'user', models.CharField(max_length=100, null=True)),
      (
       'host', models.CharField(max_length=100, null=True)),
      (
       'port', models.IntegerField(null=True)),
      (
       'db', models.CharField(max_length=100, null=True)),
      (
       'waiting', models.CharField(default='f', max_length=100, null=True)),
      (
       'query', models.TextField(max_length=100000, null=True)),
      (
       'database', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitor.Database'))]),
     migrations.AlterIndexTogether(name='postgres_ash',
       index_together=set([('pid', 'created_at'), ('database', 'created_at'), ('query', 'created_at')])),
     migrations.AlterIndexTogether(name='performance',
       index_together=set([('database', 'name', 'created_at')])),
     migrations.AlterIndexTogether(name='oracle_ash',
       index_together=set([('sid', 'serial', 'created_at'), ('database', 'created_at'), ('sql_id', 'created_at')])),
     migrations.AlterIndexTogether(name='mysql_ash',
       index_together=set([('info', 'created_at'), ('database', 'created_at'), ('conn_id', 'created_at')])),
     migrations.AlterIndexTogether(name='mssql_ash',
       index_together=set([('sql_handle', 'created_at'), ('database', 'created_at'), ('linked_ip', 'linked_spid'), ('session_id', 'created_at')])),
     migrations.AlterIndexTogether(name='db2_ash',
       index_together=set([('executable_id', 'created_at'), ('database', 'created_at'), ('appl_id', 'created_at')]))]
# okay decompiling ./restful/hawkeye/monitor/migrations/0001_initial.pyc
