# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./monitor/migrations/0002_auto_20171026_0655.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 8087 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('monitor', '0001_initial')]
    operations = [
     migrations.CreateModel(name='DB2_Lock_History',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created_at', models.DateTimeField()),
      (
       'lock_name', models.CharField(max_length=1000, null=True)),
      (
       'lock_object_type', models.CharField(max_length=1000, null=True)),
      (
       'lock_wait_elapsed_time', models.IntegerField(null=True)),
      (
       'tabschema', models.CharField(max_length=1000, null=True)),
      (
       'tabname', models.CharField(max_length=1000, null=True)),
      (
       'data_partition_id', models.IntegerField(null=True)),
      (
       'lock_mode', models.CharField(max_length=1000, null=True)),
      (
       'lock_current_mode', models.CharField(max_length=1000, null=True)),
      (
       'lock_mode_requested', models.CharField(max_length=1000, null=True)),
      (
       'req_application_handle', models.IntegerField(null=True)),
      (
       'req_agent_tid', models.IntegerField(null=True)),
      (
       'req_member', models.IntegerField(null=True)),
      (
       'req_application_name', models.CharField(max_length=1000, null=True)),
      (
       'req_userid', models.CharField(max_length=1000, null=True)),
      (
       'req_executable_id', models.CharField(max_length=100, null=True)),
      (
       'req_stmt_text', models.TextField(max_length=100000, null=True)),
      (
       'hld_application_handle', models.IntegerField(null=True)),
      (
       'hld_member', models.IntegerField(null=True)),
      (
       'hld_application_name', models.CharField(max_length=1000, null=True)),
      (
       'hld_userid', models.CharField(max_length=1000, null=True)),
      (
       'hld_current_stmt_text', models.TextField(max_length=100000, null=True)),
      (
       'hld_executable_id', models.CharField(max_length=100, null=True)),
      (
       'database', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitor.Database'))]),
     migrations.CreateModel(name='MSSQL_Lock_History',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created_at', models.DateTimeField()),
      (
       'b_sessionid', models.IntegerField()),
      (
       'b_login_name', models.CharField(max_length=1000, null=True)),
      (
       'b_status', models.CharField(max_length=1000, null=True)),
      (
       'b_text', models.TextField(max_length=100000, null=True)),
      (
       'b_sql_handle', models.CharField(max_length=1000, null=True)),
      (
       'w_sessionid', models.IntegerField()),
      (
       'w_login_name', models.CharField(max_length=1000, null=True)),
      (
       'w_status', models.CharField(max_length=1000, null=True)),
      (
       'w_waitduration', models.IntegerField()),
      (
       'w_waittype', models.CharField(max_length=1000, null=True)),
      (
       'w_waitrequestmode', models.CharField(max_length=1000, null=True)),
      (
       'w_waitresource', models.CharField(max_length=1000, null=True)),
      (
       'w_waitresourcetype', models.CharField(max_length=1000, null=True)),
      (
       'w_waitresourcedatabasename', models.CharField(max_length=1000, null=True)),
      (
       'w_text', models.TextField(max_length=100000, null=True)),
      (
       'w_sql_handle', models.CharField(max_length=1000, null=True)),
      (
       'database', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitor.Database'))]),
     migrations.CreateModel(name='MySQL_Lock_History',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created_at', models.DateTimeField()),
      (
       'w_trx_id', models.CharField(blank=True, max_length=100, null=True)),
      (
       'w_thread_id', models.CharField(blank=True, max_length=100, null=True)),
      (
       'w_wait_time', models.IntegerField(null=True)),
      (
       'w_waiting_query', models.CharField(blank=True, max_length=4000, null=True)),
      (
       'w_waiting_table_lock', models.CharField(blank=True, max_length=100, null=True)),
      (
       'b_trx_id', models.CharField(blank=True, max_length=100, null=True)),
      (
       'b_thread_id', models.CharField(blank=True, max_length=100, null=True)),
      (
       'b_host', models.CharField(blank=True, max_length=100, null=True)),
      (
       'b_port', models.CharField(blank=True, max_length=100, null=True)),
      (
       'b_idle_in_trx', models.IntegerField(null=True)),
      (
       'b_trx_query', models.CharField(blank=True, max_length=4000, null=True)),
      (
       'database', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitor.Database'))]),
     migrations.CreateModel(name='Oracle_Lock_History',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created_at', models.DateTimeField()),
      (
       'b_res', models.CharField(blank=True, max_length=100, null=True)),
      (
       'b_blocker', models.CharField(blank=True, max_length=100, null=True)),
      (
       'b_blocked_cnt', models.IntegerField(null=True)),
      (
       'b_request', models.IntegerField(null=True)),
      (
       'b_lmode', models.IntegerField(null=True)),
      (
       'b_username', models.CharField(blank=True, max_length=100, null=True)),
      (
       'b_sql_id', models.CharField(blank=True, max_length=100, null=True)),
      (
       'b_sqltext', models.TextField(max_length=100000, null=True)),
      (
       'b_prev_sql_id', models.CharField(blank=True, max_length=100, null=True)),
      (
       'b_prev_sqltext', models.TextField(max_length=100000, null=True)),
      (
       'b_ctime', models.IntegerField(null=True)),
      (
       'w_waiter', models.CharField(blank=True, max_length=100, null=True)),
      (
       'w_request', models.IntegerField(null=True)),
      (
       'w_lmode', models.IntegerField(null=True)),
      (
       'w_username', models.CharField(blank=True, max_length=100, null=True)),
      (
       'w_sql_id', models.CharField(blank=True, max_length=100, null=True)),
      (
       'w_sqltext', models.TextField(max_length=100000, null=True)),
      (
       'w_prev_sql_id', models.CharField(blank=True, max_length=100, null=True)),
      (
       'w_prev_sqltext', models.TextField(max_length=100000, null=True)),
      (
       'w_ctime', models.IntegerField(null=True)),
      (
       'database', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitor.Database'))]),
     migrations.AlterIndexTogether(name='oracle_lock_history',
       index_together=set([('database', 'created_at')])),
     migrations.AlterIndexTogether(name='mysql_lock_history',
       index_together=set([('database', 'created_at')])),
     migrations.AlterIndexTogether(name='mssql_lock_history',
       index_together=set([('database', 'created_at')])),
     migrations.AlterIndexTogether(name='db2_lock_history',
       index_together=set([('database', 'created_at')]))]
# okay decompiling ./restful/hawkeye/monitor/migrations/0002_auto_20171026_0655.pyc
