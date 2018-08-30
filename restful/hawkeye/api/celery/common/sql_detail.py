# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/celery/common/sql_detail.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 714 bytes
from api.v1.monitor.services.sqldetail.generalSQLDetail import db2_gen_sql_detail
from datetime import datetime
from common.util import get_1s_timestamp
from api.enum.activity_enum import TABLE_HEADERS
from api.v1.monitor.services.activityService import get_activity_dimension
INTERVAL = 600

def get_top_sql_detail(database):
    db_type = database.db_type
    dim = len(TABLE_HEADERS.get(db_type)) - 1
    end_time = get_1s_timestamp()
    begin_time = end_time - INTERVAL
    top_sql_list = get_activity_dimension(str(database.id), begin_time=begin_time, end_time=end_time, dim=dim)
    for x in top_sql_list.get('data'):
        db2_gen_sql_detail(database, x.get('SQL_ID'), x.get('SQL_TEXT'), x.get('SCHEMA'))
# okay decompiling ./restful/hawkeye/api/celery/common/sql_detail.pyc
