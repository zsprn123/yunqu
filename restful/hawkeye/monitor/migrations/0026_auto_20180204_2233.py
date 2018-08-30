# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./monitor/migrations/0026_auto_20180204_2233.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 358 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('monitor', '0025_auto_20180202_1707')]
    operations = [
     migrations.AlterModelOptions(name='performance',
       options={'ordering': ('-created_at', )})]
# okay decompiling ./restful/hawkeye/monitor/migrations/0026_auto_20180204_2233.pyc
