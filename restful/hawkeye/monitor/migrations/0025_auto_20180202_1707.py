# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./monitor/migrations/0025_auto_20180202_1707.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 1082 bytes
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('monitor', '0024_auto_20180202_0225')]
    operations = [
     migrations.CreateModel(name='SQL_Detail',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created_at', models.DateTimeField()),
      (
       'sql_id', models.CharField(max_length=1000, null=True)),
      (
       'sql_detail', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}, null=True)),
      (
       'database', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitor.Database'))]),
     migrations.AlterIndexTogether(name='sql_detail',
       index_together={
      ('database', 'created_at'), ('database', 'sql_id')})]
# okay decompiling ./restful/hawkeye/monitor/migrations/0025_auto_20180202_1707.pyc
