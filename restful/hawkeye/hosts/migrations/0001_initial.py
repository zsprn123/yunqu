# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./hosts/migrations/0001_initial.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 1804 bytes
from django.db import migrations, models
import django.db.models.deletion, uuid

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='Host',
       fields=[
      (
       'id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
      (
       'created_at', models.DateTimeField(auto_now_add=True)),
      (
       'updated_at', models.DateTimeField(auto_now=True)),
      (
       'address', models.CharField(max_length=100, null=True)),
      (
       'username', models.CharField(max_length=100, null=True)),
      (
       'password', models.CharField(max_length=100, null=True))],
       options={'ordering':('-created_at', ), 
      'abstract':False}),
     migrations.CreateModel(name='Memory',
       fields=[
      (
       'id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
      (
       'created_at', models.DateTimeField(auto_now_add=True)),
      (
       'updated_at', models.DateTimeField(auto_now=True)),
      (
       'total', models.IntegerField(blank=True, default=0, null=True)),
      (
       'used', models.IntegerField(blank=True, default=0, null=True)),
      (
       'free', models.IntegerField(blank=True, default=0, null=True)),
      (
       'host', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hosts.Host'))],
       options={'ordering':('-created_at', ), 
      'abstract':False})]
# okay decompiling ./restful/hawkeye/hosts/migrations/0001_initial.pyc
