# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./monitor/migrations/0038_auto_20180226_1420.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 2303 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('monitor', '0037_auto_20180226_1406')]
    operations = [
     migrations.AlterModelOptions(name='db2_ash',
       options={'ordering': ('-created_at', )}),
     migrations.AlterModelOptions(name='mysql_ash',
       options={'ordering': ('-created_at', )}),
     migrations.AlterModelOptions(name='oracle_ash',
       options={'ordering': ('-created_at', )}),
     migrations.AddField(model_name='mysql_ash',
       name='program',
       field=models.CharField(max_length=100, null=True)),
     migrations.AlterField(model_name='mssql_ash',
       name='command',
       field=models.CharField(max_length=100, null=True)),
     migrations.AlterField(model_name='mssql_ash',
       name='machine',
       field=models.CharField(max_length=100, null=True)),
     migrations.AlterField(model_name='mssql_ash',
       name='program',
       field=models.CharField(max_length=100, null=True)),
     migrations.AlterField(model_name='mssql_ash',
       name='sql_elapsed_time',
       field=models.BigIntegerField(null=True)),
     migrations.AlterField(model_name='mssql_ash',
       name='sql_id',
       field=models.CharField(max_length=100, null=True)),
     migrations.AlterField(model_name='mssql_ash',
       name='username',
       field=models.CharField(max_length=100, null=True)),
     migrations.AlterField(model_name='mysql_ash',
       name='sql_elapsed_time',
       field=models.BigIntegerField(null=True)),
     migrations.AlterIndexTogether(name='db2_ash',
       index_together={
      ('session_id', 'created_at'), ('database', 'created_at'), ('sql_id', 'created_at')}),
     migrations.AlterIndexTogether(name='mssql_ash',
       index_together={
      ('linked_ip', 'linked_spid')})]
# okay decompiling ./restful/hawkeye/monitor/migrations/0038_auto_20180226_1420.pyc
