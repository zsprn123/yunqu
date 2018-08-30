# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./sqlaudit/migrations/0037_auto_20180126_1025.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 2091 bytes
from django.db import migrations, models
import django.db.models.deletion, uuid

class Migration(migrations.Migration):
    dependencies = [
     ('monitor', '0022_merge_20180120_1242'),
     ('sqlaudit', '0036_auto_20180124_1016')]
    operations = [
     migrations.CreateModel(name='Audit_Schema',
       fields=[
      (
       'id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
      (
       'created_at', models.DateTimeField(auto_now_add=True)),
      (
       'updated_at', models.DateTimeField(auto_now=True)),
      (
       'username', models.CharField(max_length=100, null=True)),
      (
       'password', models.CharField(max_length=100, null=True)),
      (
       'database', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitor.Database'))],
       options={'ordering':('-created_at', ), 
      'abstract':False}),
     migrations.CreateModel(name='Audit_Static_Content',
       fields=[
      (
       'id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
      (
       'created_at', models.DateTimeField(auto_now_add=True)),
      (
       'updated_at', models.DateTimeField(auto_now=True)),
      (
       'content', models.TextField(max_length=1000000000, null=True))]),
     migrations.AddField(model_name='audit_job',
       name='static_job',
       field=models.BooleanField(default=False)),
     migrations.AddField(model_name='audit_static_content',
       name='job',
       field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sqlaudit.Audit_Job')),
     migrations.AlterIndexTogether(name='audit_static_content',
       index_together={
      ('job', )})]
# okay decompiling ./restful/hawkeye/sqlaudit/migrations/0037_auto_20180126_1025.pyc
