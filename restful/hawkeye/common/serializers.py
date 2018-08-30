# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./common/serializers.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 936 bytes
from rest_framework import serializers

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    refer to http://stackoverflow.com/questions/23643204/django-rest-framework-dynamically-return-subset-of-fields
    """

    def __init__(self, *args, **kwargs):
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)
        fields = self.context['request'].query_params.get('fields') if 'request' in self.context else None
        if fields:
            fields = fields.split(',')
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)
# okay decompiling ./restful/hawkeye/common/serializers.pyc
