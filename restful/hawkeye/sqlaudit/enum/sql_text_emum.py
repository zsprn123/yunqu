# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./sqlaudit/enum/sql_text_emum.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 335 bytes
COLLECT_SQL_TEXT = {'sql':'\n    select to_char(FORCE_MATCHING_SIGNATURE) FORCE_MATCHING_SIGNATURE,\n           max(sql_id) SQL_ID,\n           max(sql_text) SQL_TEXT\n           from gv$sqlarea where {inst_id_pred} and {schema_pred}\n           group by FORCE_MATCHING_SIGNATURE', 
 'schema_name':'PARSING_SCHEMA_NAME'}
# okay decompiling ./restful/hawkeye/sqlaudit/enum/sql_text_emum.pyc
