# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./sqlaudit/enum/db2_single_sql_rule_enum.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 5460 bytes
DB2SingleTemplateJson = {'TABLE_OLD_STATS':{'sql':"select\n  TABSCHEMA as OWNER,\n  TABNAME as TABLE_NAME,\n  COLCOUNT,\n  card as card,\n  NPAGES,\n  FPAGES,\n  FPAGES - NPAGES EPAGES,\n  tbspace,\n  to_char(stats_time,'yyyy-mm-dd hh24:mi:ss') as stats_time,\n  days(current DATE) - days(stats_time) MESSAGE\nfrom syscat.tables\nwhere {table_pred}\nand days(current DATE) - days(stats_time) > {pred}", 
  'schema_name':'TABSCHEMA,TABNAME'}, 
 'TABLE_MISSING_STATS':{'sql':"select\n  TABSCHEMA as OWNER,\n  TABNAME as TABLE_NAME,\n  COLCOUNT,\n  card as card,\n  NPAGES,\n  FPAGES,\n  FPAGES - NPAGES EPAGES,\n  tbspace,\n  to_char(create_time,'yyyy-mm-dd hh24:mi:ss') as MESSAGE\nfrom syscat.tables\nwhere {table_pred}\nand stats_time is null\n    ", 
  'schema_name':'TABSCHEMA,TABNAME'}, 
 'INDEX_MISSING_STATS':{'sql':"\n  SELECT\n      c.indname,\n      c.indextype,\n      c.uniquerule,\n      c.colnames,\n      c.NLEVELS,\n      c.nleaf,\n      c.num_empty_leafs,\n      c.numrids_deleted,\n      to_char(c.create_time,'yyyy-mm-dd hh24:mi:ss') as MESSAGE\n  FROM syscat.indexes c\n    where {table_pred}\n    and c.stats_time is null", 
  'schema_name':'INDSCHEMA,INDNAME'}, 
 'INDEX_OLD_STATS':{'sql':"\n      SELECT\n      c.indname,\n      c.indextype,\n      c.uniquerule,\n      c.colnames,\n      c.NLEVELS,\n      c.nleaf,\n      c.num_empty_leafs,\n      c.numrids_deleted,\n      to_char(c.stats_time,'yyyy-mm-dd hh24:mi:ss') as stats_time,\n      days(current DATE) - days(stats_time) MESSAGE\n  FROM syscat.indexes c\n    where {table_pred}\n    and days(current DATE) - days(stats_time) > {pred}", 
  'schema_name':'INDSCHEMA,INDNAME'}, 
 'TABLE_INCONSISTENT_STATS':{'sql':"select\n      TABSCHEMA as OWNER,\n      TABNAME as TABLE_NAME,\n      COLCOUNT,\n      card as card,\n      NPAGES,\n      FPAGES,\n      FPAGES - NPAGES EPAGES,\n      tbspace,\n      to_char(stats_time,'yyyy-mm-dd hh24:mi:ss') as stats_time,\n      NPAGES MESSAGE\n    from syscat.tables\n    where {table_pred}\n    and NPAGES > {pred} and card = 0", 
  'schema_name':'TABSCHEMA,TABNAME'}, 
 'TABLE_EMPTY_STATS':{'sql':"select\n  TABSCHEMA as OWNER,\n  TABNAME as TABLE_NAME,\n  COLCOUNT,\n  card as card,\n  NPAGES,\n  FPAGES,\n  FPAGES - NPAGES EPAGES,\n  tbspace,\n  to_char(stats_time,'yyyy-mm-dd hh24:mi:ss') as stats_time\nfrom syscat.tables\nwhere {table_pred}\nand NPAGES = 0 and card = 0", 
  'schema_name':'TABSCHEMA,TABNAME'}, 
 'INDEX_EMPTY_LEAFS':{'sql':"\nSELECT\n    c.indname,\n    c.indextype,\n    c.uniquerule,\n    c.colnames,\n    c.NLEVELS,\n    c.nleaf,\n    c.num_empty_leafs MESSAGE,\n    c.numrids_deleted,\n    to_char(c.stats_time,'yyyy-mm-dd hh24:mi:ss') stat_time\nFROM syscat.indexes c\n  where {table_pred}\n  and c.num_empty_leafs > {pred}", 
  'schema_name':'INDSCHEMA,INDNAME'}, 
 'INDEX_RIDS_DELETED':{'sql':"\nSELECT\n    c.indname,\n    c.indextype,\n    c.uniquerule,\n    c.colnames,\n    c.NLEVELS,\n    c.nleaf,\n    c.num_empty_leafs,\n    c.numrids_deleted MESSAGE,\n    to_char(c.stats_time,'yyyy-mm-dd hh24:mi:ss') as stats_time\nFROM syscat.indexes c\n  where {table_pred}\n  and c.numrids_deleted > {pred}", 
  'schema_name':'INDSCHEMA,INDNAME'}, 
 'INDEX_NLEVELS':{'sql':"\nSELECT\n    c.indname,\n    c.indextype,\n    c.uniquerule,\n    c.colnames,\n    c.NLEVELS MESSAGE,\n    c.nleaf,\n    c.num_empty_leafs,\n    c.numrids_deleted,\n    to_char(c.stats_time,'yyyy-mm-dd hh24:mi:ss') stats_time\nFROM syscat.indexes c\n  where {table_pred}\n  and c.NLEVELS > {pred}", 
  'schema_name':'INDSCHEMA,INDNAME'}, 
 'TABLE_EMPTY_PAGES':{'sql':"select\n  TABSCHEMA as OWNER,\n  TABNAME as TABLE_NAME,\n  COLCOUNT,\n  card as card,\n  NPAGES,\n  FPAGES,\n  FPAGES - NPAGES MESSAGE,\n  tbspace,\n  to_char(stats_time,'yyyy-mm-dd hh24:mi:ss') as stats_time\nfrom syscat.tables\nwhere {table_pred}\nand (FPAGES - NPAGES) > {pred}", 
  'schema_name':'TABSCHEMA,TABNAME'}, 
 'INDEX_COLUMNS':{'sql':"\nSELECT\n    c.indname,\n    c.indextype,\n    c.uniquerule,\n    c.colnames,\n    c.NLEVELS,\n    c.nleaf,\n    c.num_empty_leafs,\n    c.numrids_deleted,\n    to_char(c.stats_time,'yyyy-mm-dd hh24:mi:ss') stats_time,\n    colcount MESSAGE\nFROM syscat.indexes c\n  where {table_pred}\n  and c.COLCOUNT > {pred}", 
  'schema_name':'INDSCHEMA,INDNAME'}, 
 'UNINDEXED_FK':{'sql':"\nselect tabschema, tabname, fk_colnames\nfrom\n(\nselect r.tabschema, r.tabname, fk_colnames, replace(r.fk_colnames, ' ', '') rcols, cast(replace(i.colnames, '+', '') as varchar(100)) icols\nfrom syscat.references r\nleft OUTER JOIN syscat.indexes i\non r.tabschema = i.tabschema\nand r.tabname = i.tabname\nwhere {table_pred}\n)\ngroup by tabschema, tabname, fk_colnames\nhaving max(LOCATE(rcols, icols)) < 1 or max(LOCATE(rcols, icols)) is null", 
  'schema_name':'r.TABSCHEMA,r.TABNAME'}, 
 'REDUNDANT_INDEX':{'sql':"\nSELECT\n    c1.TABSCHEMA,\n    c1.TABNAME,\n    c1.indname INDEX_NAME1,\n    c2.indname INDEX_NAME2,\n    c1.colnames || ':' || c2.colnames MESSAGE\nFROM syscat.indexes c1, syscat.indexes c2\n  where {table_pred}\n  and c1.TABSCHEMA = c2.TABSCHEMA\n  and c1.TABNAME = c2.TABNAME\n  and c1.INDNAME != c2.INDNAME\n  and c1.colnames != c2.colnames\n  and c1.colcount != c2.colcount\n  and LOCATE(c1.colnames, c2.colnames) = 1", 
  'schema_name':'c1.TABSCHEMA,c1.TABNAME'}, 
 'SINGLE_TABLE_INDEXES':{'sql':'\n    select tabschema, tabname, count(*) MESSAGE\n    from syscat.indexes\n    where {table_pred}\n    group by tabschema, tabname\n    having count(*) > {pred}', 
  'schema_name':'TABSCHEMA,TABNAME'}}
# okay decompiling ./restful/hawkeye/sqlaudit/enum/db2_single_sql_rule_enum.pyc
