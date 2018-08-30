# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./monitor/migrations/0013_auto_20180109_2257.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 988 bytes
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('monitor', '0012_auto_20171210_1257')]
    operations = [
     migrations.CreateModel(name='Transaction',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created_at', models.DateTimeField()),
      (
       'transactions', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}, null=True)),
      (
       'database', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitor.Database'))]),
     migrations.AlterIndexTogether(name='transaction',
       index_together={
      ('database', 'created_at')})]
# okay decompiling ./restful/hawkeye/monitor/migrations/0013_auto_20180109_2257.pyc
