# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/alarm/services/warnConfigService.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 731 bytes
import os
from alarm.models import Warn_Config

def update_database_warn_config(global_warn_config):
    (Warn_Config.objects.filter(template=global_warn_config, category=global_warn_config.category)).update(category=global_warn_config.category,
      warn_threshold=global_warn_config.warn_threshold,
      critical_threshold=global_warn_config.critical_threshold,
      warning_interval=global_warn_config.warning_interval,
      pre_warning_times=global_warn_config.pre_warning_times,
      status=global_warn_config.status,
      description=global_warn_config.description,
      optional=global_warn_config.optional)
# okay decompiling ./restful/hawkeye/api/v1/alarm/services/warnConfigService.pyc
