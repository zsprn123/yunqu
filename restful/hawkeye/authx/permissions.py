# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./authx/permissions.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 1674 bytes
from guardian.compat import is_authenticated
from rest_framework.permissions import BasePermission, IsAdminUser as DrfIsAdminUser, DjangoObjectPermissions

class IsAdminUser(DrfIsAdminUser):

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsSuperUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsAdmin(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_admin

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class CustomObjectPermissions(DjangoObjectPermissions):
    """
    Obsolete !!!
        I don't know why I am following the example mentioned below...  
    
    Similar to `DjangoObjectPermissions`, but adding 'view' permissions.
    refer to 
    http://www.django-rest-framework.org/api-guide/filtering/#djangoobjectpermissionsfilter
    """
    perms_map = {'GET':[
      '%(app_label)s.view_%(model_name)s'], 
     'POST':[
      '%(app_label)s.view_%(model_name)s'], 
     'OPTIONS':[
      '%(app_label)s.view_%(model_name)s'], 
     'HEAD':[
      '%(app_label)s.view_%(model_name)s'], 
     'PUT':[
      '%(app_label)s.change_%(model_name)s'], 
     'PATCH':[
      '%(app_label)s.change_%(model_name)s'], 
     'DELETE':[
      '%(app_label)s.delete_%(model_name)s']}
# okay decompiling ./restful/hawkeye/authx/permissions.pyc
