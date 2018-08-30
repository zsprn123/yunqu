# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./hawkeye/urls.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 1334 bytes
"""hawkeye URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from .views import index
apidoc = []
from rest_framework_swagger.views import get_swagger_view
from django.urls import path
schema_view = get_swagger_view(title=' API')
apidoc = [path('apidoc/', schema_view)]
urlpatterns = [
 path('', index),
 path('api/', include('api.urls')),
 path('admin/', admin.site.urls)] + apidoc
# okay decompiling ./restful/hawkeye/hawkeye/urls.pyc
