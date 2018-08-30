# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./monitor/migrations/0050_auto_20180612_1223.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 588 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('monitor', '0049_auto_20180404_1603')]
    operations = [
     migrations.AlterField(model_name='database',
       name='version',
       field=models.CharField(blank=True, max_length=320, null=True)),
     migrations.AlterIndexTogether(name='table_rows',
       index_together={
      ('database', 'created_at'), ('database', 'owner', 'table_name')})]
# okay decompiling ./restful/hawkeye/monitor/migrations/0050_auto_20180612_1223.pyc
