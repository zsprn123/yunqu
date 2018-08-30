# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./sqlaudit/migrations/0020_auto_20171218_1144.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 1345 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion, uuid

class Migration(migrations.Migration):
    dependencies = [
     ('sqlaudit', '0019_auto_20171218_1107')]
    operations = [
     migrations.CreateModel(name='Audit_SQL_TEXT',
       fields=[
      (
       'id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
      (
       'created_at', models.DateTimeField(auto_now_add=True)),
      (
       'updated_at', models.DateTimeField(auto_now=True)),
      (
       'sql_id', models.CharField(max_length=100, null=True)),
      (
       'sql_text', models.CharField(max_length=3000, null=True)),
      (
       'force_matching_signature', models.BigIntegerField(null=True)),
      (
       'job', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sqlaudit.Audit_Job'))]),
     migrations.RemoveField(model_name='audit_sql_result',
       name='sql_text'),
     migrations.AlterIndexTogether(name='audit_sql_text',
       index_together=set([('force_matching_signature', )]))]
# okay decompiling ./restful/hawkeye/sqlaudit/migrations/0020_auto_20171218_1144.pyc
