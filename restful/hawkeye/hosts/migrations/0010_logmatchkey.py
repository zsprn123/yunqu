# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./hosts/migrations/0010_logmatchkey.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 845 bytes
from django.db import migrations, models
import uuid

class Migration(migrations.Migration):
    dependencies = [
     ('hosts', '0009_host_ssh_key')]
    operations = [
     migrations.CreateModel(name='LogMatchKey',
       fields=[
      (
       'id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
      (
       'created_at', models.DateTimeField(auto_now_add=True)),
      (
       'updated_at', models.DateTimeField(auto_now=True)),
      (
       'value', models.CharField(max_length=300)),
      (
       'db_type', models.CharField(max_length=100))],
       options={'ordering':('-created_at', ), 
      'abstract':False})]
# okay decompiling ./restful/hawkeye/hosts/migrations/0010_logmatchkey.pyc
