# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./monitor/migrations/0014_auto_20180111_2248.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 1746 bytes
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('monitor', '0013_auto_20180109_2257')]
    operations = [
     migrations.CreateModel(name='Space',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created_at', models.DateTimeField()),
      (
       'name', models.CharField(max_length=100, null=True)),
      (
       'total', models.FloatField()),
      (
       'free', models.FloatField()),
      (
       'used', models.FloatField()),
      (
       'database', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitor.Database'))]),
     migrations.CreateModel(name='Space_Detail',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created_at', models.DateTimeField()),
      (
       'detail', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}, null=True)),
      (
       'database', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitor.Database'))]),
     migrations.AlterIndexTogether(name='space_detail',
       index_together={
      ('database', 'created_at')}),
     migrations.AlterIndexTogether(name='space',
       index_together={
      ('database', 'created_at')})]
# okay decompiling ./restful/hawkeye/monitor/migrations/0014_auto_20180111_2248.pyc
