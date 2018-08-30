# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./sqlaudit/enum/total_template_enum.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 2779 bytes
TotalTemplateJSON = {'oracle':{u'SQL\u6587\u672c':{'sql':'select count(*) COUNT from gv$sqlarea where {schema_pred} and {inst_id_pred} and {sql_text_pred}', 
   'schema_name':'PARSING_SCHEMA_NAME'}, 
  u'\u6267\u884c\u8ba1\u5212':{'sql':'select count(*) COUNT from gv$sql where {schema_pred} and {inst_id_pred} and {sql_text_pred}', 
   'schema_name':'PARSING_SCHEMA_NAME'}, 
  u'SQL\u76d1\u89c6':{'sql':'select count(*) COUNT from gv$sql_monitor where {schema_pred} and {inst_id_pred}', 
   'schema_name':'username'}, 
  u'\u8868':{'sql':"select count(*) COUNT from dba_tables where temporary = 'N' and {schema_pred}", 
   'schema_name':'owner'}, 
  u'\u4e34\u65f6\u8868':{'sql':"select count(*) COUNT from dba_tables where temporary = 'Y' and {schema_pred}", 
   'schema_name':'owner'}, 
  u'\u5206\u533a':{'sql':'select count(*) COUNT from dba_tab_partitions where {schema_pred}', 
   'schema_name':'table_owner'}, 
  u'\u7d22\u5f15':{'sql':"select count(*) COUNT from dba_indexes where index_type != 'LOB' and {schema_pred}", 
   'schema_name':'table_owner'}, 
  u'\u5e8f\u5217':{'sql':'select count(*) COUNT from dba_sequences where {schema_pred}', 
   'schema_name':'SEQUENCE_OWNER'}, 
  u'\u5b57\u6bb5':{'sql':'select count(*) COUNT from dba_tab_columns where {schema_pred}', 
   'schema_name':'owner'}, 
  u'\u5916\u952e\u7ea6\u675f':{'sql':"select count(*) COUNT from dba_constraints where {schema_pred} and constraint_type = 'R'", 
   'schema_name':'owner'}, 
  u'\u5bf9\u8c61':{'sql':'select count(*) COUNT from dba_objects where {schema_pred}', 
   'schema_name':'owner'}}, 
 'db2':{u'\u8868':{'sql':'select count(*) COUNT from syscat.tables where {schema_pred}', 
   'schema_name':'tabschema'}, 
  u'\u7d22\u5f15':{'sql':'select count(*) COUNT from syscat.indexes where {schema_pred}', 
   'schema_name':'tabschema'}, 
  u'\u5916\u952e\u7ea6\u675f':{'sql':'select count(*) COUNT from syscat.references where {schema_pred}', 
   'schema_name':'tabschema'}}, 
 'sqlserver':{u'\u8868':{'sql':'select count(*) COUNT from sys.tables', 
   'schema_name':'tabschema'}, 
  u'\u7d22\u5f15':{'sql':'select count(*) COUNT from sys.indexes', 
   'schema_name':'tabschema'}}, 
 'mysql':{u'\u8868':{'sql':'select count(*) COUNT FROM information_schema.TABLES where {schema_pred}', 
   'schema_name':'TABLE_SCHEMA'}, 
  u'\u7d22\u5f15':{'sql':'select count(*) COUNT from syscat.indexes where {schema_pred}', 
   'schema_name':'tabschema'}, 
  u'\u5916\u952e\u7ea6\u675f':{'sql':'select count(*) COUNT from syscat.references where {schema_pred}', 
   'schema_name':'tabschema'}}}
# okay decompiling ./restful/hawkeye/sqlaudit/enum/total_template_enum.pyc
