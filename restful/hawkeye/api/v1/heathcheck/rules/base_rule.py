# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/heathcheck/rules/base_rule.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 2304 bytes
from datetime import datetime
import logging
from api.v1.monitor.services.runsqlService import run_sql
logger = logging.getLogger(__file__)

class Rule(object):

    def __init__(self):
        self.check_sql = ''
        self.result = ''
        self.category = ''
        self.description = ''
        self.advise = ''
        self.database_type = ''
        self.supported_db_versions = []
        self.score = 10
        self.priority = ''
        self.elapse_time = ''
        self.title = ''
        self.pre_check_sql = ''
        self.pre_check_pass_condition = ''
        self.db_name = ''
        self.result_raw = ''
        self.exe_advise = ''

    def check(self, database, db_version):
        if self.is_right_version(db_version):
            if self.is_pre_check_pass(database):
                start_time = datetime.now().timestamp()
                self._check(database)
                end_time = datetime.now().timestamp()
                self.elapse_time = round(float(str(end_time - start_time)), 2)
                self.__dict__.pop('check_sql', None)
                self.__dict__.pop('result_raw', None)
                self.__dict__.pop('exe_advise', None)
        return self.__dict__

    def resize_result_raw(self):
        self.result_raw = len(self.result_raw) > 50 and self.result_raw[0:49] if isinstance(self.result_raw, list) else self.result_raw

    def is_right_version(self, db_version):
        return db_version in self.supported_db_versions

    def _check(self, cursor):
        pass

    def is_pre_check_pass(self, database):
        if self.pre_check_sql == '':
            return True
        try:
            return self.pre_check_compare(database)
        except Exception as e:
            logger.exception('health pre check queries, error: %s', e)
            return False

    def pre_check_compare(self, database):
        return True

    def set_db_name(self, name):
        self.db_name = name
        return self

    def add_markdown_style(self):
        pass

    def set_id_and_db_name(self, db_id, name):
        self.db_id = str(db_id)
        self.db_name = name
        return self
# okay decompiling ./restful/hawkeye/api/v1/heathcheck/rules/base_rule.pyc
