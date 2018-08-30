# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./common/models.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 606 bytes
import uuid, time
from django.db import models

class CoreModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        columns = self.__table__.columns.keys()
        return {key:getattr(self, key) for key in columns}

    class Meta:
        ordering = ('-created_at', )
        abstract = True


class PerformanceModel(models.Model):
    created_at = models.DateTimeField()

    class Meta:
        abstract = True
# okay decompiling ./restful/hawkeye/common/models.pyc
