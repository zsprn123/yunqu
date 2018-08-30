# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/sqlaudit/filtersets.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 1368 bytes
import rest_framework_filters as filters
from monitor.models import Database, Performance
from sqlaudit.models import Audit_Job, Optimization_Job, Audit_SQL_Result, SQL_Perf_Diff

class Audit_JobFilterSet(filters.FilterSet):

    class Meta:
        model = Audit_Job
        fields = {'database':('exact', ), 
         'status':('exact', ), 
         'compare_audit':('exact', ), 
         'is_static_job':('exact', )}


class Optimization_JobFilterSet(filters.FilterSet):

    class Meta:
        model = Optimization_Job
        fields = {'status':('exact', ), 
         'owner':('exact', ), 
         'audit_job__database':('exact', )}


class Audit_SQL_ResultFilterSet(filters.FilterSet):

    class Meta:
        model = Audit_SQL_Result
        fields = {'id':('exact', ), 
         'job':('exact', )}


def default_filterset(model):
    return type(model.__name__, (filters.FilterSet,), dict({'created_at':filters.DateFromToRangeFilter(),  'Meta':type('Meta', (object,), {'model':model,  'fields':'__all__'})}))


class SQL_Perf_DiffFilterSet(filters.FilterSet):

    class Meta:
        model = SQL_Perf_Diff
        fields = {'database': ('exact', )}
# okay decompiling ./restful/hawkeye/api/v1/sqlaudit/filtersets.pyc
