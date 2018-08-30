# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/misc/serializers.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 413 bytes
from django.contrib.contenttypes.models import ContentType
from rest_framework_bulk.serializers import BulkSerializerMixin, BulkListSerializer
from common.serializers import DynamicFieldsModelSerializer

class ContentTypeSerializer(BulkSerializerMixin, DynamicFieldsModelSerializer):

    class Meta:
        model = ContentType
        list_serializer_class = BulkListSerializer
        fields = '__all__'
# okay decompiling ./restful/hawkeye/api/v1/misc/serializers.pyc
