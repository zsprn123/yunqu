# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./alarm/migrations/0012_auto_20180116_1002.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 615 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('alarm', '0011_warn_result_send_status')]
    operations = [
     migrations.AlterField(model_name='warn_config',
       name='receivers',
       field=models.ManyToManyField(blank=True, to='alarm.Receiver')),
     migrations.AlterField(model_name='warn_config_template',
       name='receivers',
       field=models.ManyToManyField(blank=True, to='alarm.Receiver'))]
# okay decompiling ./restful/hawkeye/alarm/migrations/0012_auto_20180116_1002.pyc
