# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./monitor/migrations/0023_auto_20180126_2318.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 364 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('monitor', '0022_merge_20180120_1242')]
    operations = [
     migrations.RenameField(model_name='space',
       old_name='total',
       new_name='total_mb')]
# okay decompiling ./restful/hawkeye/monitor/migrations/0023_auto_20180126_2318.pyc
