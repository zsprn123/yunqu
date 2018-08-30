# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/heathcheck/filtersets.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 315 bytes
import rest_framework_filters as filters
from heathcheck.models import Heathcheck_Report

class Heathcheck_ReportFilterSet(filters.FilterSet):
    created_at = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Heathcheck_Report
        exclude = ('report_detail', )
# okay decompiling ./restful/hawkeye/api/v1/heathcheck/filtersets.pyc
