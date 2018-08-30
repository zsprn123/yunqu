# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./sqlaudit/enum/sqlserver_problem_template_enum.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 1944 bytes
ProblemTemplateJSON = {'NO_INDEX':{'sql':"SELECT\n     COUNT(*) COUNT\nFROM sys.objects o\nINNER JOIN sys.indexes i ON i.OBJECT_ID = o.OBJECT_ID\n-- tables that are heaps without any nonclustered indexes\nWHERE (\n        o.type = 'U'\n        AND o.OBJECT_ID NOT IN (\n            SELECT OBJECT_ID\n            FROM sys.indexes\n            WHERE index_id > 0\n            )\n        )", 
  'schema_name':''}, 
 'TABLE_OLD_STATS':{'sql': "\n    SELECT      COUNT(*) COUNT\nFROM sys.stats s\nJOIN sys.stats_columns sc\nON sc.[object_id] = s.[object_id] AND sc.stats_id = s.stats_id\nJOIN sys.columns c ON c.[object_id] = sc.[object_id] AND c.column_id = sc.column_id\nJOIN sys.partitions par ON par.[object_id] = s.[object_id]\nJOIN sys.objects obj ON par.[object_id] = obj.[object_id]\nWHERE OBJECTPROPERTY(s.OBJECT_ID,'IsUserTable') = 1\nAND (s.auto_created = 1 OR s.user_created = 1)\nAND DATEDIFF(d,STATS_DATE(s.[object_id], s.stats_id),getdate()) > {pred}"}, 
 'MISSING_INDEX':{'sql': '\n    select\nCOUNT(*) COUNT\nFROM sys.dm_db_missing_index_details AS mid\nINNER JOIN sys.tables t ON t.OBJECT_ID = mid.object_id\nINNER JOIN sys.dm_db_missing_index_groups AS mig\nON mig.index_handle = mid.index_handle\nINNER JOIN sys.dm_db_missing_index_group_stats  AS migs\nON mig.index_group_handle=migs.group_handle'}, 
 'INDEX_COLUMNS':{'sql': "\nwith v as\n(\nSELECT\n    DB_NAME() + '.' + schema_name(s.schema_id) as [OWNER],\n    t.name as [TABLE_NAME],\n    INDEX_NAME = ind.name,\n    count(*) as [MESSAGE]\nFROM\n    sys.indexes ind\nINNER JOIN\n    sys.index_columns ic ON  ind.object_id = ic.object_id and ind.index_id = ic.index_id\nINNER JOIN\n    sys.columns col ON ic.object_id = col.object_id and ic.column_id = col.column_id\nINNER JOIN\n    sys.tables t ON ind.object_id = t.object_id\nLEFT OUTER JOIN\n    sys.schemas s ON t.schema_id = s.schema_id\ngroup by s.schema_id,t.name,ind.name\nhaving count(*) > {pred})\nselect COUNT(*) COUNT from v\n"}}
# okay decompiling ./restful/hawkeye/sqlaudit/enum/sqlserver_problem_template_enum.pyc
