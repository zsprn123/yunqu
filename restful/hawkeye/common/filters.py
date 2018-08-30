# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./common/filters.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 2264 bytes
from django.core.exceptions import FieldDoesNotExist
from django.db.models.fields.related import ForeignObjectRel
from rest_framework.filters import OrderingFilter, DjangoObjectPermissionsFilter

class RelatedOrderingFilter(OrderingFilter):
    """
    Extends OrderingFilter to support ordering by fields in related models
    using the Django ORM __ notation
    """

    def is_valid_field(self, model, field):
        """
        Return true if the field exists within the model (or in the related
        model specified using the Django ORM __ notation)
        """
        components = field.split('__', 1)
        try:
            field, parent_model, direct, m2m = model._meta.get_field_by_name(components[0])
            if isinstance(field, ForeignObjectRel):
                return self.is_valid_field(field.model, components[1])
            if field.rel:
                if len(components) == 2:
                    return self.is_valid_field(field.rel.to, components[1])
            return True
        except FieldDoesNotExist:
            return False

    def remove_invalid_fields(self, queryset, ordering, view):
        return [term for term in ordering if self.is_valid_field(queryset.model, term.lstrip('-'))]


class DjangoModelObjectPermissionsFilter(DjangoObjectPermissionsFilter):

    def filter_queryset(self, request, queryset, view):
        from guardian.shortcuts import get_objects_for_user
        user = request.user
        model_cls = queryset.model
        kwargs = {'app_label':model_cls._meta.app_label, 
         'model_name':model_cls._meta.model_name}
        permission = self.perm_format % kwargs
        extra = {'accept_global_perms': True}
        return get_objects_for_user(user, permission, queryset, **extra)
# okay decompiling ./restful/hawkeye/common/filters.pyc
