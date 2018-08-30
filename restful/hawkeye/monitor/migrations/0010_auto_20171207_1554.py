# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./monitor/migrations/0010_auto_20171207_1554.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 1783 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('monitor', '0009_auto_20171120_0656')]
    operations = [
     migrations.CreateModel(name='SQLMON',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created_at', models.DateTimeField()),
      (
       'status', models.CharField(max_length=100, null=True)),
      (
       'sql_id', models.CharField(max_length=100, null=True)),
      (
       'elapsed_time', models.BigIntegerField(null=True)),
      (
       'db_time', models.BigIntegerField(null=True)),
      (
       'db_cpu', models.BigIntegerField(null=True)),
      (
       'sql_exec_id', models.BigIntegerField(null=True)),
      (
       'sql_exec_start', models.CharField(max_length=100, null=True)),
      (
       'sql_plan_hash_value', models.BigIntegerField(null=True)),
      (
       'inst_id', models.IntegerField(null=True)),
      (
       'username', models.CharField(max_length=100, null=True)),
      (
       'sql_text', models.TextField(max_length=100000, null=True)),
      (
       'sqlmon', models.TextField(max_length=100000, null=True)),
      (
       'database', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitor.Database'))]),
     migrations.AlterIndexTogether(name='sqlmon',
       index_together=set([('database', 'sql_id', 'sql_exec_id'), ('database', 'created_at')]))]
# okay decompiling ./restful/hawkeye/monitor/migrations/0010_auto_20171207_1554.pyc
