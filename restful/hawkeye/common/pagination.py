# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./common/pagination.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 979 bytes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class StandardResultsSetPagination(PageNumberPagination):
    """
        doing this class only to make page_size work...
    """
    page_size_query_param = 'page_size'


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        next_link_str = self.get_next_link()
        previous_link_str = self.get_previous_link()
        if next_link_str != None:
            if next_link_str.find('http://127.0.0.1:8000') == 0:
                next_link_str = next_link_str[21:]
        if previous_link_str != None:
            if previous_link_str.find('http://127.0.0.1:8000') == 0:
                previous_link_str = previous_link_str[21:]
        return Response({'next':next_link_str, 
         'previous':previous_link_str, 
         'count':self.page.paginator.count, 
         'results':data})
# okay decompiling ./restful/hawkeye/common/pagination.pyc
