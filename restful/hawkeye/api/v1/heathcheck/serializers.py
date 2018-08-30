# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/heathcheck/serializers.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 739 bytes
from rest_framework_bulk import BulkListSerializer
from common.serializers import DynamicFieldsModelSerializer
from heathcheck.models import Heathcheck_Report
from rest_framework import serializers

class Heathcheck_ReportSerializer(DynamicFieldsModelSerializer):
    database_name = serializers.SerializerMethodField()

    class Meta:
        model = Heathcheck_Report
        list_serializer_class = BulkListSerializer
        fields = '__all__'

    def get_database_name(self, obj):
        if obj.status == 4:
            return ''
        elif obj.database:
            return obj.database.alias
        else:
            return ''
# okay decompiling ./restful/hawkeye/api/v1/heathcheck/serializers.pyc
