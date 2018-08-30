# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./monitor/migrations/0048_table_rows.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 994 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('monitor', '0047_space_type')]
    operations = [
     migrations.CreateModel(name='Table_Rows',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created_at', models.DateTimeField()),
      (
       'owner', models.CharField(blank=True, max_length=100, null=True)),
      (
       'table_name', models.CharField(blank=True, max_length=100, null=True)),
      (
       'rows', models.IntegerField(blank=True, null=True)),
      (
       'database', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitor.Database'))],
       options={'abstract': False})]
# okay decompiling ./restful/hawkeye/monitor/migrations/0048_table_rows.pyc
