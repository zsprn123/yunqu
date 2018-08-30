# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./common/storages.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 348 bytes
from django.conf import settings
import redis as redis_module
redis = redis_module.StrictRedis(host=settings.REDIS_HOST,
  port=settings.REDIS_PORT,
  password=settings.REDIS_PASSWORD,
  decode_responses=True,
  charset='utf-8')
pubsub = redis.pubsub(ignore_subscribe_messages=True)
# okay decompiling ./restful/hawkeye/common/storages.pyc
