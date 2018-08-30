# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/auth/urls.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 833 bytes
from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path
from . import views
from rest_framework_jwt.views import verify_jwt_token
router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('permissions', views.PermissionViewSet)
router.register('userobjectpermissions', views.UserObjectPermissionViewSet)
urlpatterns = [
 path('', include(router.urls)),
 path('token/', views.obtain_jwt_token),
 path('token/refresh/', views.refresh_jwt_token),
 path('token/verify/', verify_jwt_token),
 path('register/', views.register),
 path('login/', views.login),
 path('grant-license/', views.grantYunquAuthorization),
 path('license-info/', views.license_info),
 path('test/', views.test),
 path('version/', views.version)]
# okay decompiling ./restful/hawkeye/api/v1/auth/urls.pyc
