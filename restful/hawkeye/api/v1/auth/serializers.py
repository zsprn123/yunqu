# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/auth/serializers.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 2306 bytes
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from guardian.models import UserObjectPermission
from rest_framework.fields import SerializerMethodField
from common.serializers import DynamicFieldsModelSerializer
from rest_framework import serializers

class UserSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = get_user_model()
        fields = '__all__'

    def create(self, validated_data):
        user = get_user_model().objects.create(username=validated_data['username'])
        user.fullname = validated_data['fullname']
        user.set_password(validated_data['password'])
        user.is_superuser = validated_data['is_superuser']
        user.is_staff = validated_data['is_staff']
        user.is_admin = validated_data['is_admin']
        user.owner = validated_data['owner']
        user.save()
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                if 'old_password' not in self.initial_data or not instance.check_password(self.initial_data['old_password']):
                    raise serializers.ValidationError({'error_message': ''})
                else:
                    instance.set_password(value)
            else:
                setattr(instance, attr, value)

        instance.save()
        return instance


class UserGroupSerializer(DynamicFieldsModelSerializer):
    groups = SerializerMethodField()

    class Meta:
        model = get_user_model()
        exclude = ('password', )

    def get_groups(self, obj):
        return []


class PermissionSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Permission
        fields = '__all__'


class UserObjectPermissionSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = UserObjectPermission
        fields = '__all__'
# okay decompiling ./restful/hawkeye/api/v1/auth/serializers.pyc
