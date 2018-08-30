# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./hosts/migrations/0011_auto_20180513_1454.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 401 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('hosts', '0010_logmatchkey')]
    operations = [
     migrations.AlterField(model_name='host',
       name='address',
       field=models.CharField(max_length=100, null=True, unique=True))]
# okay decompiling ./restful/hawkeye/hosts/migrations/0011_auto_20180513_1454.pyc
