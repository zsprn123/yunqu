# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./sqlaudit/enum/db2_problem_template_enum.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 2951 bytes
ProblemTemplateJSON = {'TABLE_OLD_STATS':{'sql':'select\ncount(*) COUNT\nfrom syscat.tables\nwhere {schema_pred}\nand days(current DATE) - days(stats_time) > {pred}', 
  'schema_name':'TABSCHEMA'}, 
 'TABLE_MISSING_STATS':{'sql':'select\ncount(*) COUNT\nfrom syscat.tables\nwhere {schema_pred}\nand stats_time is null\n    ', 
  'schema_name':'TABSCHEMA'}, 
 'INDEX_MISSING_STATS':{'sql':'\n  SELECT\ncount(*) COUNT\n  FROM syscat.indexes c\n    where {schema_pred}\n    and c.stats_time is null', 
  'schema_name':'INDSCHEMA'}, 
 'INDEX_OLD_STATS':{'sql':'\n      SELECT\ncount(*) COUNT\n  FROM syscat.indexes c\n    where {schema_pred}\n    and days(current DATE) - days(stats_time) > {pred}', 
  'schema_name':'INDSCHEMA'}, 
 'TABLE_INCONSISTENT_STATS':{'sql':'select\ncount(*) COUNT\n    from syscat.tables\n    where {schema_pred}\n    and NPAGES > {pred} and card = 0', 
  'schema_name':'TABSCHEMA'}, 
 'TABLE_EMPTY_STATS':{'sql':'select\ncount(*) COUNT\nfrom syscat.tables\nwhere {schema_pred}\nand NPAGES = 0 and card = 0', 
  'schema_name':'TABSCHEMA'}, 
 'INDEX_EMPTY_LEAFS':{'sql':'\nSELECT\ncount(*) COUNT\nFROM syscat.indexes c\n  where {schema_pred}\n  and c.num_empty_leafs > {pred}', 
  'schema_name':'INDSCHEMA'}, 
 'INDEX_RIDS_DELETED':{'sql':'\nSELECT\ncount(*) COUNT\nFROM syscat.indexes c\n  where {schema_pred}\n  and c.numrids_deleted > {pred}', 
  'schema_name':'INDSCHEMA'}, 
 'INDEX_NLEVELS':{'sql':'\nSELECT\ncount(*) COUNT\nFROM syscat.indexes c\n  where {schema_pred}\n  and c.NLEVELS > {pred}', 
  'schema_name':'INDSCHEMA'}, 
 'TABLE_EMPTY_PAGES':{'sql':'select\ncount(*) COUNT\nfrom syscat.tables\nwhere {schema_pred}\nand (FPAGES - NPAGES) > {pred}', 
  'schema_name':'TABSCHEMA'}, 
 'INDEX_COLUMNS':{'sql':'\nSELECT\ncount(*) COUNT\nFROM syscat.indexes c\n  where {schema_pred}\n  and c.COLCOUNT > {pred}', 
  'schema_name':'INDSCHEMA'}, 
 'UNINDEXED_FK':{'sql':"\nselect count(*) COUNT\nfrom\n(\nselect r.tabschema, r.tabname, fk_colnames, replace(r.fk_colnames, ' ', '') rcols, cast(replace(i.colnames, '+', '') as varchar(100)) icols\nfrom syscat.references r\nleft OUTER JOIN syscat.indexes i\non r.tabschema = i.tabschema\nand r.tabname = i.tabname\nwhere {schema_pred}\n)\ngroup by tabschema, tabname, fk_colnames\nhaving max(LOCATE(rcols, icols)) < 1 or max(LOCATE(rcols, icols)) is null", 
  'schema_name':'r.TABSCHEMA'}, 
 'REDUNDANT_INDEX':{'sql':'\nSELECT\n    count(*) COUNT\nFROM syscat.indexes c1, syscat.indexes c2\n  where {schema_pred}\n  and c1.TABSCHEMA = c2.TABSCHEMA\n  and c1.TABNAME = c2.TABNAME\n  and c1.INDNAME != c2.INDNAME\n  and c1.colnames != c2.colnames\n  and c1.colcount != c2.colcount\n  and LOCATE(c1.colnames, c2.colnames) = 1', 
  'schema_name':'c1.TABSCHEMA'}, 
 'SINGLE_TABLE_INDEXES':{'sql':'\n    select count(*) COUNT\n    from syscat.indexes\n    where {schema_pred}\n    group by tabschema, tabname\n    having count(*) > {pred}', 
  'schema_name':'TABSCHEMA'}}
# okay decompiling ./restful/hawkeye/sqlaudit/enum/db2_problem_template_enum.pyc
