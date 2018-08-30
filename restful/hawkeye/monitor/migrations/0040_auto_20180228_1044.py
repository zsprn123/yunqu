# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./monitor/migrations/0040_auto_20180228_1044.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 382 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('monitor', '0039_auto_20180226_2218')]
    operations = [
     migrations.RenameField(model_name='mssql_ash',
       old_name='blocking_session_id',
       new_name='b_blocker')]
# okay decompiling ./restful/hawkeye/monitor/migrations/0040_auto_20180228_1044.pyc
