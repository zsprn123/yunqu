# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./hawkeye/celery.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 4005 bytes
from __future__ import absolute_import
import os
from celery import Celery, schedules
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hawkeye.settings.celery')
import django
django.setup()

def install_default_entries(self, data):
    entries = {}
    if self.app.conf.result_expires:
        entries.setdefault('celery.backend_cleanup', {'task':'celery.backend_cleanup', 
         'schedule':schedules.crontab('0', '4', '*'), 
         'options':{'expires': 43200}})
    entries.setdefault('', {'task':'api.tasks.performance', 
     'schedule':10.0, 
     'args':()})
    entries.setdefault('', {'task':'api.tasks.activity', 
     'schedule':10.0, 
     'args':()})
    entries.setdefault('', {'task':'api.tasks.lock_history', 
     'schedule':60.0, 
     'args':()})
    entries.setdefault('SQL', {'task':'api.tasks.sqlmon', 
     'schedule':600.0, 
     'args':()})
    entries.setdefault('', {'task':'api.tasks.space', 
     'schedule':3600.0, 
     'args':()})
    entries.setdefault('', {'task':'api.tasks.check_database_alive', 
     'schedule':60.0, 
     'args':()})
    entries.setdefault('', {'task':'api.tasks.standby', 
     'schedule':600.0, 
     'args':()})
    entries.setdefault('', {'task':'api.tasks.plan_change', 
     'schedule':3600.0, 
     'args':()})
    entries.setdefault('DDL', {'task':'api.tasks.object_change', 
     'schedule':3660.0, 
     'args':()})
    entries.setdefault('', {'task':'api.tasks.update_index_data', 
     'schedule':30.0, 
     'args':()})
    entries.setdefault('', {'task':'api.tasks.send_warn_message', 
     'schedule':60.0, 
     'args':()})
    self.update_from_dict(entries)


from django.conf import settings
from django_celery_beat.schedulers import DatabaseScheduler
DatabaseScheduler.install_default_entries = install_default_entries
app = Celery('hawkeye')
app.conf.enable_utc = False
app.conf.broker_url = settings.REDIS_CONN_STR
app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'
app.autodiscover_tasks(lambda : settings.INSTALLED_APPS)
# okay decompiling ./restful/hawkeye/hawkeye/celery.pyc
