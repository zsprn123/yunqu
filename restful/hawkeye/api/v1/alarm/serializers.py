# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/alarm/serializers.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 2104 bytes
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from rest_framework_bulk.serializers import BulkSerializerMixin, BulkListSerializer
from alarm.models import Warn_Config, Warn_Config_Template, Warn_Result, Receiver, Mail_Config
from common.serializers import DynamicFieldsModelSerializer
from rest_framework import serializers

class Warn_ConfigSerializer(BulkSerializerMixin, DynamicFieldsModelSerializer):

    class Meta:
        model = Warn_Config
        list_serializer_class = BulkListSerializer
        exclude = ('created_at', 'updated_at')


class Warn_Config_TemplateSerializer(BulkSerializerMixin, DynamicFieldsModelSerializer):

    class Meta:
        model = Warn_Config_Template
        list_serializer_class = BulkListSerializer
        exclude = ('created_at', 'updated_at')


class ReceiverSerializer(BulkSerializerMixin, DynamicFieldsModelSerializer):

    class Meta:
        model = Receiver
        list_serializer_class = BulkListSerializer
        exclude = ('created_at', 'updated_at')


class Warn_ResultSerializer(BulkSerializerMixin, DynamicFieldsModelSerializer):
    database_alias = serializers.SlugRelatedField(read_only=True, slug_field='alias', source='database')
    warn_type = serializers.SlugRelatedField(read_only=True, slug_field='description', source='warn')

    class Meta:
        model = Warn_Result
        list_serializer_class = BulkListSerializer
        exclude = ('id', 'updated_at', 'database', 'warn')


class PeriodicTaskSerializer(BulkSerializerMixin, DynamicFieldsModelSerializer):

    class Meta:
        model = PeriodicTask
        list_serializer_class = BulkListSerializer
        fields = '__all__'


class IntervalScheduleSerializer(BulkSerializerMixin, DynamicFieldsModelSerializer):

    class Meta:
        model = IntervalSchedule
        list_serializer_class = BulkListSerializer
        fields = '__all__'


class Mail_ConfigSerializer(BulkSerializerMixin, DynamicFieldsModelSerializer):

    class Meta:
        model = Mail_Config
        list_serializer_class = BulkListSerializer
        fields = '__all__'
# okay decompiling ./restful/hawkeye/api/v1/alarm/serializers.pyc
