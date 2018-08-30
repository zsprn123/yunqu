# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./monitor/migrations/0051_auto_20180610_1112.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 1109 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('monitor', '0050_auto_20180610_1007')]
    operations = [
     migrations.DeleteModel(name='Performance_OLD'),
     migrations.CreateModel(name='Performance',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created_at', models.DateTimeField()),
      (
       'inst_id', models.IntegerField(default=0, null=True)),
      (
       'name_id', models.IntegerField(default=1, null=True)),
      (
       'value', models.FloatField()),
      (
       'database', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitor.Database'))]),
     migrations.AlterIndexTogether(name='performance',
       index_together={
      ('database', 'name_id', 'created_at')})]
# okay decompiling ./restful/hawkeye/monitor/migrations/0051_auto_20180610_1112.pyc
