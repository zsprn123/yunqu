# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./sqlaudit/enum/db2_detail_template_enum.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 5606 bytes
DetailTemplateJson = {'TABLE_OLD_STATS':{'sql':"select\n  TABSCHEMA as OWNER,\n  TABNAME as TABLE_NAME,\n  COLCOUNT,\n  card as card,\n  NPAGES,\n  FPAGES,\n  FPAGES - NPAGES EPAGES,\n  tbspace,\n  to_char(stats_time,'yyyy-mm-dd hh24:mi:ss') as stats_time,\n  days(current DATE) - days(stats_time) MESSAGE\nfrom syscat.tables\nwhere {schema_pred}\nand days(current DATE) - days(stats_time) > {pred}\norder by TABNAME", 
  'schema_name':'TABSCHEMA'}, 
 'TABLE_MISSING_STATS':{'sql':"select\n  TABSCHEMA as OWNER,\n  TABNAME as TABLE_NAME,\n  COLCOUNT,\n  card as card,\n  NPAGES,\n  FPAGES,\n  FPAGES - NPAGES EPAGES,\n  tbspace,\n  to_char(create_time,'yyyy-mm-dd hh24:mi:ss') as MESSAGE\nfrom syscat.tables\nwhere {schema_pred}\nand stats_time is null\norder by TABNAME\n    ", 
  'schema_name':'TABSCHEMA'}, 
 'INDEX_MISSING_STATS':{'sql':"\n  SELECT\n      c.indname,\n      c.indextype,\n      c.uniquerule,\n      c.colnames,\n      c.NLEVELS,\n      c.nleaf,\n      c.num_empty_leafs,\n      c.numrids_deleted,\n      to_char(c.create_time,'yyyy-mm-dd hh24:mi:ss') as MESSAGE\n  FROM syscat.indexes c\n    where {schema_pred}\n    and c.stats_time is null\n    order by 1", 
  'schema_name':'INDSCHEMA'}, 
 'INDEX_OLD_STATS':{'sql':"\n      SELECT\n      c.indname,\n      c.indextype,\n      c.uniquerule,\n      c.colnames,\n      c.NLEVELS,\n      c.nleaf,\n      c.num_empty_leafs,\n      c.numrids_deleted,\n      to_char(c.stats_time,'yyyy-mm-dd hh24:mi:ss') as stats_time,\n      days(current DATE) - days(stats_time) MESSAGE\n  FROM syscat.indexes c\n    where {schema_pred}\n    and days(current DATE) - days(stats_time) > {pred}\n    order by 1", 
  'schema_name':'INDSCHEMA'}, 
 'TABLE_INCONSISTENT_STATS':{'sql':"select\n      TABSCHEMA as OWNER,\n      TABNAME as TABLE_NAME,\n      COLCOUNT,\n      card as card,\n      NPAGES,\n      FPAGES,\n      FPAGES - NPAGES EPAGES,\n      tbspace,\n      to_char(stats_time,'yyyy-mm-dd hh24:mi:ss') as stats_time,\n      NPAGES MESSAGE\n    from syscat.tables\n    where {schema_pred}\n    and NPAGES > {pred} and card = 0\n    order by TABNAME", 
  'schema_name':'TABSCHEMA'}, 
 'TABLE_EMPTY_STATS':{'sql':"select\n  TABSCHEMA as OWNER,\n  TABNAME as TABLE_NAME,\n  COLCOUNT,\n  card as card,\n  NPAGES,\n  FPAGES,\n  FPAGES - NPAGES EPAGES,\n  tbspace,\n  to_char(stats_time,'yyyy-mm-dd hh24:mi:ss') as stats_time\nfrom syscat.tables\nwhere {schema_pred}\nand NPAGES = 0 and card = 0\norder by TABNAME", 
  'schema_name':'TABSCHEMA'}, 
 'INDEX_EMPTY_LEAFS':{'sql':"\nSELECT\n    c.indname,\n    c.indextype,\n    c.uniquerule,\n    c.colnames,\n    c.NLEVELS,\n    c.nleaf,\n    c.num_empty_leafs MESSAGE,\n    c.numrids_deleted,\n    to_char(c.stats_time,'yyyy-mm-dd hh24:mi:ss') stat_time\nFROM syscat.indexes c\n  where {schema_pred}\n  and c.num_empty_leafs > {pred}\n  order by indname", 
  'schema_name':'INDSCHEMA'}, 
 'INDEX_RIDS_DELETED':{'sql':"\nSELECT\n    c.indname,\n    c.indextype,\n    c.uniquerule,\n    c.colnames,\n    c.NLEVELS,\n    c.nleaf,\n    c.num_empty_leafs,\n    c.numrids_deleted MESSAGE,\n    to_char(c.stats_time,'yyyy-mm-dd hh24:mi:ss') as stats_time\nFROM syscat.indexes c\n  where {schema_pred}\n  and c.numrids_deleted > {pred}\n  order by indname", 
  'schema_name':'INDSCHEMA'}, 
 'INDEX_NLEVELS':{'sql':"\nSELECT\n    c.indname,\n    c.indextype,\n    c.uniquerule,\n    c.colnames,\n    c.NLEVELS MESSAGE,\n    c.nleaf,\n    c.num_empty_leafs,\n    c.numrids_deleted,\n    to_char(c.stats_time,'yyyy-mm-dd hh24:mi:ss') stats_time\nFROM syscat.indexes c\n  where {schema_pred}\n  and c.NLEVELS > {pred}\n  order by indname", 
  'schema_name':'INDSCHEMA'}, 
 'TABLE_EMPTY_PAGES':{'sql':"select\n  TABSCHEMA as OWNER,\n  TABNAME as TABLE_NAME,\n  COLCOUNT,\n  card as card,\n  NPAGES,\n  FPAGES,\n  FPAGES - NPAGES MESSAGE,\n  tbspace,\n  to_char(stats_time,'yyyy-mm-dd hh24:mi:ss') as stats_time\nfrom syscat.tables\nwhere {schema_pred}\nand (FPAGES - NPAGES) > {pred}\norder by tabname", 
  'schema_name':'TABSCHEMA'}, 
 'INDEX_COLUMNS':{'sql':"\nSELECT\n    c.indname,\n    c.indextype,\n    c.uniquerule,\n    c.colnames,\n    c.NLEVELS,\n    c.nleaf,\n    c.num_empty_leafs,\n    c.numrids_deleted,\n    to_char(c.stats_time,'yyyy-mm-dd hh24:mi:ss') stats_time,\n    colcount MESSAGE\nFROM syscat.indexes c\n  where {schema_pred}\n  and c.COLCOUNT > {pred}\n  order by indname", 
  'schema_name':'INDSCHEMA'}, 
 'UNINDEXED_FK':{'sql':"\nselect tabschema, tabname, fk_colnames\nfrom\n(\nselect r.tabschema, r.tabname, fk_colnames, replace(r.fk_colnames, ' ', '') rcols, cast(replace(i.colnames, '+', '') as varchar(100)) icols\nfrom syscat.references r\nleft OUTER JOIN syscat.indexes i\non r.tabschema = i.tabschema\nand r.tabname = i.tabname\nwhere {schema_pred}\n)\ngroup by tabschema, tabname, fk_colnames\nhaving max(LOCATE(rcols, icols)) < 1 or max(LOCATE(rcols, icols)) is null\norder by tabname", 
  'schema_name':'r.TABSCHEMA'}, 
 'REDUNDANT_INDEX':{'sql':"\nSELECT\n    c1.TABSCHEMA,\n    c1.TABNAME,\n    c1.indname INDEX_NAME1,\n    c2.indname INDEX_NAME2,\n    c1.colnames || ':' || c2.colnames MESSAGE\nFROM syscat.indexes c1, syscat.indexes c2\n  where {schema_pred}\n  and c1.TABSCHEMA = c2.TABSCHEMA\n  and c1.TABNAME = c2.TABNAME\n  and c1.INDNAME != c2.INDNAME\n  and c1.colnames != c2.colnames\n  and c1.colcount != c2.colcount\n  and LOCATE(c1.colnames, c2.colnames) = 1\n  order by tabname", 
  'schema_name':'c1.TABSCHEMA'}, 
 'SINGLE_TABLE_INDEXES':{'sql':'\n    select tabschema, tabname, count(*) MESSAGE\n    from syscat.indexes\n    where {schema_pred}\n    group by tabschema, tabname\n    having count(*) > {pred}\n    order by tabname', 
  'schema_name':'TABSCHEMA'}}
# okay decompiling ./restful/hawkeye/sqlaudit/enum/db2_detail_template_enum.pyc
