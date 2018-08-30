# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/sqlaudit/serializers.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 6074 bytes
from django.db.models import Q
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from requests import Response
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin
from rest_framework_filters.compat import set_many
from common.aes import aes_encode
from common.serializers import DynamicFieldsModelSerializer
from sqlaudit.models import Audit_Job, Audit_Result, Audit_Rule, Audit_SQL_Result, Optimization_Job, Audit_Schema, SQL_Perf_Diff
import uuid
from rest_framework import serializers
import json
from api.v1.monitor.services.activityService import get_sql_perf
ANALYSIS_FUNCTION = 'api.tasks.sql_audit_analysis'

class Audit_JobSerializer(DynamicFieldsModelSerializer):
    database_alias = serializers.SlugRelatedField(read_only=True, slug_field='alias', source='database')

    class Meta:
        model = Audit_Job
        list_serializer_class = BulkListSerializer
        fields = '__all__'

    def create(self, validated_data):
        instance = super(Audit_JobSerializer, self).create(validated_data)
        datetime = validated_data['plan_time']
        is_static_job = validated_data.get('is_static_job', False)
        schedule = CrontabSchedule.objects.filter((Q(minute=datetime.minute)) & (Q(hour=datetime.hour)) & (Q(day_of_month=datetime.day)) & (Q(month_of_year=datetime.month)))
        if not schedule:
            schedule = CrontabSchedule(minute=datetime.minute, hour=datetime.hour, day_of_month=datetime.day, month_of_year=datetime.month)
            schedule.save()
        else:
            schedule = schedule[0]
        task = PeriodicTask(crontab=schedule, name=str(uuid.uuid4()), task=ANALYSIS_FUNCTION,
          args=json.dumps([str(instance.id)]),
          description='audit_job')
        task.save()
        instance.task = task
        instance.save()
        return instance

    def validate(self, attrs):
        begin_time = attrs.get('plan_time')
        database = attrs.get('database')
        if not begin_time or not database:
            raise serializers.ValidationError('plan_time and database_id is required')
        return super(Audit_JobSerializer, self).validate(attrs)


class Audit_ResultSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Audit_Result
        list_serializer_class = BulkListSerializer
        fields = ('name', 'target', 'audit_type', 'score', 'problem', 'total', 'problem_rate',
                  'result')


class Audit_RuleSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Audit_Rule
        list_serializer_class = BulkListSerializer
        fields = '__all__'

    def to_representation(self, obj):
        output = super(Audit_RuleSerializer, self).to_representation(obj)
        if output.get('is_static_rule', False):
            output.pop('single')
        return output


class Audit_SQL_ResultSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Audit_SQL_Result
        list_serializer_class = BulkListSerializer
        fields = '__all__'


class Optimization_JobSerializer(DynamicFieldsModelSerializer):
    database_alias = serializers.SlugRelatedField(read_only=True, slug_field='alias', source='database')
    audit_job_name = serializers.SlugRelatedField(read_only=True, slug_field='name', source='audit_job')
    owner_name = serializers.SlugRelatedField(read_only=True, slug_field='fullname', source='owner')

    class Meta:
        model = Optimization_Job
        list_serializer_class = BulkListSerializer
        fields = '__all__'


class Audit_SchemaSerializer(DynamicFieldsModelSerializer):
    database_alias = serializers.SlugRelatedField(read_only=True, slug_field='alias', source='database')

    def create(self, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = aes_encode(validated_data['password'])
        item = Audit_Schema.objects.create(**validated_data)
        item.save()
        return item

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = aes_encode(validated_data['password'])
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)
        for attr, value in validated_data.items():
            if attr in info.relations:
                if info.relations[attr].to_many:
                    set_many(instance, attr, value)
            else:
                setattr(instance, attr, value)

        instance.save()
        return instance

    class Meta:
        model = Audit_Schema
        list_serializer_class = BulkListSerializer
        fields = '__all__'


def default_serializer(model):
    return type(model.__name__, (BulkSerializerMixin, DynamicFieldsModelSerializer), dict({'Meta': type('Meta', (object,), {'model':model,  'list_serializer_class':BulkListSerializer,  'fields':'__all__'})}))


class SQL_Perf_Diff_Serializer(DynamicFieldsModelSerializer):
    database_alias = serializers.SlugRelatedField(read_only=True, slug_field='alias', source='database')

    class Meta:
        model = SQL_Perf_Diff
        list_serializer_class = BulkListSerializer
        fields = '__all__'

    def create(self, validated_data):
        instance = super(SQL_Perf_Diff_Serializer, self).create(validated_data)
        db = instance.database
        pk = db.pk
        sql_id_list = instance.sql_id_list
        instance.snapshot_begin_time = instance.created_at
        instance.begin_result = get_sql_perf(pk, sql_id_list)
        instance.save()
        return instance
# okay decompiling ./restful/hawkeye/api/v1/sqlaudit/serializers.pyc
