# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/monitor/serializers.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 3549 bytes
from guardian.shortcuts import assign_perm
from rest_framework.serializers import raise_errors_on_nested_writes, ModelSerializer
from rest_framework.utils import model_meta
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin
from rest_framework import serializers
from rest_framework_filters.compat import set_many
from api.v1.monitor.services.createdbService import init_warnconfig
from api.v1.sqlaudit.services.initialService import sqlaudit_init
from common.aes import aes_encode
from common.serializers import DynamicFieldsModelSerializer
from monitor.models import Database, Performance, DB2_ASH, MySQL_ASH, MSSQL_ASH

class DatabaseSerializer(BulkSerializerMixin, ModelSerializer):
    owner_name = serializers.SlugRelatedField(read_only=True, slug_field='username', source='owner')

    def create(self, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = aes_encode(validated_data['password'])
        item = Database.objects.create(**validated_data)
        item.save()
        if item.owner:
            if item.owner.is_admin or item.owner.is_superuser:
                assign_perm('view_database', item.owner, item)
        init_warnconfig(item)
        sqlaudit_init(item)
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
        init_warnconfig(instance)
        return instance

    def validate(self, attrs):
        for k, v in attrs.items():
            attrs[k] = v.strip() if type(v) == str else v

        return super(DatabaseSerializer, self).validate(attrs)

    class Meta:
        model = Database
        list_serializer_class = BulkListSerializer
        fields = '__all__'


class PerformanceSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Performance
        list_serializer_class = BulkListSerializer
        fields = '__all__'


class DB2_ASHSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = DB2_ASH
        list_serializer_class = BulkListSerializer
        exclude = ('id', 'activity_state', 'query_cost_estimate', 'direct_reads', 'direct_writes',
                   'database')


class MySQL_ASHSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = MySQL_ASH
        list_serializer_class = BulkListSerializer
        exclude = ('id', 'database')


class MSSQL_ASHSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = MSSQL_ASH
        list_serializer_class = BulkListSerializer
        exclude = ('id', 'database', 'linked_ip', 'linked_spid')


def default_serializer(model):
    return type(model.__name__, (BulkSerializerMixin, DynamicFieldsModelSerializer), dict({'Meta': type('Meta', (object,), {'model':model,  'list_serializer_class':BulkListSerializer,  'fields':'__all__'})}))
# okay decompiling ./restful/hawkeye/api/v1/monitor/serializers.pyc
