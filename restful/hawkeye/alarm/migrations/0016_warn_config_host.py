# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./alarm/migrations/0016_warn_config_host.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 535 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('hosts', '0007_auto_20180321_1503'),
     ('alarm', '0015_auto_20180204_2233')]
    operations = [
     migrations.AddField(model_name='warn_config',
       name='host',
       field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hosts.Host'))]
# okay decompiling ./restful/hawkeye/alarm/migrations/0016_warn_config_host.pyc
