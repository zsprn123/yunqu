# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./sqlaudit/migrations/0004_auto_20171211_0701.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 562 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('sqlaudit', '0003_auto_20171211_0227')]
    operations = [
     migrations.RenameField(model_name='audit_rule',
       old_name='audit_trategy',
       new_name='audit_strategy'),
     migrations.RemoveField(model_name='audit_strategy',
       name='predicate')]
# okay decompiling ./restful/hawkeye/sqlaudit/migrations/0004_auto_20171211_0701.pyc
