# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./alarm/migrations/0008_mail_config.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 1064 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('alarm', '0007_auto_20171205_0917')]
    operations = [
     migrations.CreateModel(name='Mail_Config',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'host', models.CharField(blank=True, max_length=50, null=True)),
      (
       'port', models.IntegerField(blank=True, default=25)),
      (
       'username', models.CharField(blank=True, max_length=50, null=True)),
      (
       'password', models.CharField(blank=True, max_length=50, null=True)),
      (
       'address', models.EmailField(blank=True, max_length=254, null=True)),
      (
       'use_tls', models.BooleanField(default=False)),
      (
       'use_ssl', models.BooleanField(default=False))])]
# okay decompiling ./restful/hawkeye/alarm/migrations/0008_mail_config.pyc
