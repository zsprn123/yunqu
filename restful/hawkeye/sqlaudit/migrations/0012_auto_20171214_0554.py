# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./sqlaudit/migrations/0012_auto_20171214_0554.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 768 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('sqlaudit', '0011_auto_20171214_0551')]
    operations = [
     migrations.AlterModelOptions(name='audit_result',
       options={}),
     migrations.AlterModelOptions(name='audit_sql_result',
       options={}),
     migrations.AlterIndexTogether(name='audit_result',
       index_together=set([('job', )])),
     migrations.AlterIndexTogether(name='audit_sql_result',
       index_together=set([('sql_id', )]))]
# okay decompiling ./restful/hawkeye/sqlaudit/migrations/0012_auto_20171214_0554.pyc
