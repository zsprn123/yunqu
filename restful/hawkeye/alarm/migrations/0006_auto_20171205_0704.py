# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./alarm/migrations/0006_auto_20171205_0704.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 563 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('alarm', '0005_auto_20171130_0904')]
    operations = [
     migrations.AlterModelOptions(name='warn_config',
       options={'ordering': ('-created_at', )}),
     migrations.AlterModelOptions(name='warn_config_template',
       options={'ordering': ('-created_at', )})]
# okay decompiling ./restful/hawkeye/alarm/migrations/0006_auto_20171205_0704.pyc
