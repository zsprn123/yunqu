# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./alarm/migrations/0001_initial.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 3725 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion, uuid

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     ('monitor', '0009_auto_20171120_0656')]
    operations = [
     migrations.CreateModel(name='Receiver',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'name', models.CharField(blank=True, max_length=1000, null=True)),
      (
       'phone_number', models.CharField(blank=True, max_length=100, null=True)),
      (
       'email', models.EmailField(blank=True, max_length=254, null=True))]),
     migrations.CreateModel(name='Warn_Config',
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
       'polling_interval', models.CharField(blank=True, default='300', max_length=100, null=True, verbose_name='')),
      (
       'warning_interval', models.CharField(blank=True, default='300', max_length=1000, null=True, verbose_name='')),
      (
       'pre_warning_times', models.CharField(blank=True, default='0', max_length=100, null=True, verbose_name='')),
      (
       'description', models.CharField(blank=True, max_length=1000, null=True)),
      (
       'database', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitor.Database')),
      (
       'receivers', models.ManyToManyField(to='alarm.Receiver'))],
       options={'abstract': False}),
     migrations.CreateModel(name='Warn_Result',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'warn_message', models.CharField(blank=True, max_length=200, null=True)),
      (
       'description', models.CharField(blank=True, max_length=1000, null=True)),
      (
       'database', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitor.Database'))]),
     migrations.CreateModel(name='Warn_Send_Status',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'status', models.CharField(blank=True, max_length=1000, null=True)),
      (
       'send_type', models.CharField(blank=True, max_length=1000, null=True)),
      (
       'exception', models.CharField(blank=True, max_length=10000, null=True)),
      (
       'receiver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='alarm.Receiver'))]),
     migrations.AddField(model_name='warn_result',
       name='send_status',
       field=models.ManyToManyField(blank=True, to='alarm.Warn_Send_Status')),
     migrations.AddField(model_name='warn_result',
       name='warn',
       field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='alarm.Warn_Config'))]
# okay decompiling ./restful/hawkeye/alarm/migrations/0001_initial.pyc
