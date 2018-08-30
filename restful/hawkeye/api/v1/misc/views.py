# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/misc/views.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 547 bytes
from django.contrib.contenttypes.models import ContentType
from rest_framework.permissions import IsAuthenticated
from rest_framework_bulk.generics import BulkModelViewSet
from api.v1.misc.filtersets import ContentTypeFilterSet
from api.v1.misc.serializers import ContentTypeSerializer

class ContentTypeViewSet(BulkModelViewSet):
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer
    filter_class = ContentTypeFilterSet
    search_fields = ('app_label', 'model')
    permission_classes = (IsAuthenticated,)
# okay decompiling ./restful/hawkeye/api/v1/misc/views.pyc
