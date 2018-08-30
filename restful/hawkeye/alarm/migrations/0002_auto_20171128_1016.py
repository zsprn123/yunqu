# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./alarm/migrations/0002_auto_20171128_1016.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 2735 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion, uuid

class Migration(migrations.Migration):
    dependencies = [
     ('alarm', '0001_initial')]
    operations = [
     migrations.CreateModel(name='Warn_Config_Template',
       fields=[
      (
       'id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
      (
       'created_at', models.DateTimeField(auto_now_add=True)),
      (
       'updated_at', models.DateTimeField(auto_now=True)),
      (
       'category', models.CharField(blank=True, max_length=100, null=True, verbose_name='')),
      (
       'warn_threshold', models.CharField(blank=True, max_length=1000, null=True, verbose_name='warn ')),
      (
       'critical_threshold', models.CharField(blank=True, max_length=1000, null=True, verbose_name='critical ')),
      (
       'warning_interval', models.CharField(blank=True, default='300', max_length=1000, null=True, verbose_name='')),
      (
       'pre_warning_times', models.CharField(blank=True, default='0', max_length=100, null=True, verbose_name='')),
      (
       'description', models.CharField(blank=True, max_length=1000, null=True)),
      (
       'db_type', models.CharField(blank=True, max_length=100, null=True, unique=True)),
      (
       'receivers', models.ManyToManyField(to='alarm.Receiver'))],
       options={'abstract': False}),
     migrations.RemoveField(model_name='warn_config',
       name='polling_interval'),
     migrations.AddField(model_name='warn_config',
       name='critical_threshold',
       field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='critical ')),
     migrations.AddField(model_name='warn_config',
       name='warn_threshold',
       field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='warn ')),
     migrations.AlterField(model_name='warn_config',
       name='pre_warning_times',
       field=models.CharField(blank=True, default='0', max_length=100, null=True, verbose_name='')),
     migrations.AddField(model_name='warn_config',
       name='template',
       field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='alarm.Warn_Config_Template'))]
# okay decompiling ./restful/hawkeye/alarm/migrations/0002_auto_20171128_1016.pyc
