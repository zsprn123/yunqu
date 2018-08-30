# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./sqlaudit/migrations/0002_auto_20171211_0212.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 2310 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('monitor', '0012_auto_20171210_1257'),
     ('sqlaudit', '0001_initial')]
    operations = [
     migrations.CreateModel(name='Audit_Rule',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'audit_type', models.CharField(max_length=100, null=True)),
      (
       'target', models.CharField(max_length=100, null=True)),
      (
       'predicate', models.CharField(max_length=1000, null=True)),
      (
       'status', models.CharField(max_length=100, null=True)),
      (
       'remarks', models.CharField(max_length=1000, null=True))]),
     migrations.AlterModelOptions(name='audit_strategy',
       options={}),
     migrations.RenameField(model_name='audit_strategy',
       old_name='name',
       new_name='audit_type'),
     migrations.AlterField(model_name='audit_result',
       name='problem_rate',
       field=models.FloatField(blank=True, null=True)),
     migrations.AlterField(model_name='audit_result',
       name='score',
       field=models.FloatField(blank=True, null=True)),
     migrations.AlterIndexTogether(name='audit_strategy',
       index_together=set([('database', )])),
     migrations.AddField(model_name='audit_rule',
       name='audit_trategy',
       field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sqlaudit.Audit_Strategy')),
     migrations.AddField(model_name='audit_rule',
       name='database',
       field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitor.Database')),
     migrations.AlterIndexTogether(name='audit_rule',
       index_together=set([('database', )]))]
# okay decompiling ./restful/hawkeye/sqlaudit/migrations/0002_auto_20171211_0212.pyc
