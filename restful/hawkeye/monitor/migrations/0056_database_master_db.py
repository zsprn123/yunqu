# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./monitor/migrations/0056_database_master_db.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 499 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('monitor', '0055_auto_20180703_1439')]
    operations = [
     migrations.AddField(model_name='database',
       name='master_db',
       field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitor.Database'))]
# okay decompiling ./restful/hawkeye/monitor/migrations/0056_database_master_db.pyc
