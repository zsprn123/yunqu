# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/enum/schema_enum.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 20421 bytes
from api.v1.monitor.services.runsqlService import run_sql
from common.util import build_exception_from_java
Schema_Query = {'oracle':"select OWNER, OBJECT_TYPE, OBJECT_NAME\n    from dba_objects\n    where\n        owner not in ('MGMT_VIEW','MDDATA','MDSYS','SI_INFORMTN_SCHEMA','ORDPLUGINS','ORDSYS','OLAPSYS','SYSMAN','ANONYMOUS','XDB','CTXSYS','EXFSYS','WMSYS','ORACLE_OCM','DBSNMP','TSMSYS','DMSYS','DIP','OUTLN','SYSTEM','SYS','APPQOSSYS', 'FLOWS_FILES', 'JWT', 'ORDDATA', 'OWBSYS', 'OWBSYS_AUDIT', 'SCOTT', 'SPATIAL_CSW_ADMIN_USR', 'SPATIAL_WFS_ADMIN_USR', 'XS$NULL', 'YUNQU')\n    and owner not like 'APEX%' and object_name not like 'SYS_IL%'\n    and object_type in (\n        'SEQUENCE',\n        'PACKAGE',\n        'FUNCTION',\n        'PROCEDURE',\n        'DATABASE LINK',\n        'TRIGGER',\n        'DIRECTORY',\n        'MATERIALIZED VIEW',\n        'TABLE',\n        'INDEX',\n        'VIEW',\n        'TYPE',\n        'JOB',\n        'SCHEDULE'\n    )\n    order by owner, object_type, object_name", 
 'db2':"\n    select\n      rtrim(OBJECTSCHEMA) as OWNER\n    , OBJECTTYPE as OBJECT_TYPE\n    , case when OBJECTTYPE not in ('PROCEDURE', 'FUNCTION')\n      then OBJECTNAME\n      else (select routinename\n            from syscat.ROUTINES\n            where routineschema = OBJECTSCHEMA and specificname = OBJECTNAME)\n      end as OBJECT_NAME\nfrom SYSIBMADM.OBJECTOWNERS\nwhere OWNERTYPE <> 'S' and OBJECTTYPE in (\n-- 'DB2 PACKAGE',\n'FUNCTION',\n'INDEX',\n--'MATERIALIZED QUERY TABLE',\n'PROCEDURE',\n'SEQUENCE',\n'TABLE',\n'TRIGGER',\n'VIEW'\n) and rtrim(OBJECTSCHEMA) not in ('SQLJ', 'SYSCAT', 'SYSFUN','SYSIBM','SYSPROC','SYSSTAT','SYSIBMADM','SYSIBMINTERNAL', 'SYSTOOLS')\norder by 1, 2, 3", 
 'mysql':"\n    SELECT OBJECT_TYPE\n\t,OBJECT_SCHEMA as OWNER\n\t,OBJECT_NAME\nFROM (\n\tSELECT 'TABLE' AS OBJECT_TYPE\n\t\t,TABLE_NAME AS OBJECT_NAME\n\t\t,TABLE_SCHEMA AS OBJECT_SCHEMA\n\tFROM information_schema.TABLES\n\tUNION\n\tSELECT 'VIEW' AS OBJECT_TYPE\n\t\t,TABLE_NAME AS OBJECT_NAME\n\t\t,TABLE_SCHEMA AS OBJECT_SCHEMA\n\tFROM information_schema.VIEWS\n\tUNION\n\tSELECT ROUTINE_TYPE AS OBJECT_TYPE\n\t\t,ROUTINE_NAME AS OBJECT_NAME\n\t\t,ROUTINE_SCHEMA AS OBJECT_SCHEMA\n\tFROM information_schema.ROUTINES\n\tUNION\n\tSELECT 'TRIGGER' AS OBJECT_TYPE\n\t\t,TRIGGER_NAME AS OBJECT_NAME\n\t\t,TRIGGER_SCHEMA AS OBJECT_SCHEMA\n\tFROM information_schema.triggers\n\t) R\n/* WHERE R.OBJECT_SCHEMA not in ('mysql', 'sys', 'performance_schema', 'information_schema') */\n    ", 
 'sqlserver':"\n    select DB_NAME() + '.' + schema_name(schema_id) as [OWNER], NAME as [OBJECT_NAME], TYPE_DESC as [OBJECT_TYPE] from sys.objects\nWHERE  is_ms_shipped = 'false' and TYPE_DESC in (\n'CHECK_CONSTRAINT',\n'DEFAULT_CONSTRAINT',\n'SQL_STORED_PROCEDURE',\n'SQL_SCALAR_FUNCTION',\n'RULE',\n'REPLICATION_FILTER_PROCEDURE',\n'SQL_TRIGGER',\n'SQL_INLINE_TABLE_VALUED_FUNCTION',\n'SQL_TABLE_VALUED_FUNCTION',\n'VIEW',\n'USER_TABLE')"}
Ordered_List = [
 '', '', '', '', '', '', '', 'DDL', '']
Object_Detail_Query = {'oracle':{u'\u8868':{u'\u8868':"\n            select\n  OWNER,\n  TABLE_NAME,\n  NUM_ROWS,\n  BLOCKS,\n  AVG_ROW_LEN,\n  GLOBAL_STATS,\n  SAMPLE_SIZE,\n  DEGREE,\n  to_char(last_analyzed,'YYYY-MM-DD HH24') last_analyzed\nfrom dba_tables\n where OWNER = '{OWNER}' and  TABLE_NAME = '{OBJECT_NAME}'\n            ", 
   u'\u5217':"\nselect\n    column_id,\n    column_name,\n    data_type||CASE\n                    WHEN data_type = 'NUMBER' THEN '('||data_precision||','||data_scale||')'\n                    ELSE '('||data_length||')'\n                END AS data_type,\n    to_char(last_analyzed,'YYYY-MM-DD HH24') last_analyzed,\n    nullable,\n    num_distinct,\n    num_nulls,\n    histogram,\n    num_buckets\nFROM\n    dba_tab_cols\nwhere OWNER = '{OWNER}' and TABLE_NAME = '{OBJECT_NAME}'\norder by 1\n            ", 
   u'\u7d22\u5f15':"\nselect\n    index_name,\n    index_type,\n    uniqueness,\n    status,\n    partitioned,\n    temporary,\n    blevel+1 blevel,\n    leaf_blocks,\n    distinct_keys,\n    num_rows,\n    clustering_factor ,\n    DEGREE,\n    to_char(last_analyzed,'YYYY-MM-DD HH24') last_analyzed\nfrom\n    dba_indexes\n where table_owner = '{OWNER}' and TABLE_NAME = '{OBJECT_NAME}'\n order by 2\n            ", 
   u'\u7d22\u5f15\u5217':"\nselect\n    c.index_name,\n    c.column_position,\n    c.column_name,\n    c.descend\nfrom\n    dba_ind_columns c\nwhere table_owner = '{OWNER}' and TABLE_NAME = '{OBJECT_NAME}'\norder by 1,2", 
   u'\u5206\u533a':"\nselect\n  partition_position\n  , partition_name\n  , composite\n  , num_rows\n  , blocks\n  , subpartition_count\n  , high_value\n  , compression\nfrom\n    dba_tab_partitions\n where table_owner = '{OWNER}' and TABLE_NAME = '{OBJECT_NAME}'\n order by partition_position\n            ", 
   u'\u5b50\u5206\u533a':"\nselect\n    partition_name\n    , subpartition_position\n    , subpartition_name\n    , num_rows\n    , blocks\n    , high_value\n    , compression\nFrom\nall_tab_subpartitions\nwhere table_owner = '{OWNER}' and TABLE_NAME = '{OBJECT_NAME}'\norder by partition_name, subpartition_position", 
   u'\u7ea6\u675f':"\nselect\n     co.constraint_name,\n     co.constraint_type,\n     co.r_constraint_name,\n     cc.column_name,\n     cc.position,\n     co.status,\n     co.validated\nfrom\n     dba_constraints co,\n     dba_cons_columns cc\nwhere\n    co.owner              = cc.owner\nand co.table_name         = cc.table_name\nand co.constraint_name    = cc.constraint_name\nand co.owner = '{OWNER}' and co.TABLE_NAME = '{OBJECT_NAME}'\norder by co.constraint_name,cc.position"}, 
  u'\u7d22\u5f15':{u'\u7d22\u5f15':"\n            select\n                index_name,\n                index_type,\n                uniqueness,\n                status,\n                partitioned,\n                temporary,\n                blevel+1 blevel,\n                leaf_blocks,\n                distinct_keys,\n                num_rows,\n                clustering_factor ,\n                DEGREE,\n                to_char(last_analyzed,'YYYY-MM-DD HH24') last_analyzed\n            from\n                dba_indexes\n             where OWNER = '{OWNER}' and INDEX_NAME = '{OBJECT_NAME}'\n             order by 2\n                        ", 
   u'\u7d22\u5f15\u5217':"\n            select\n                c.index_name,\n                c.column_position,\n                c.column_name,\n                c.descend\n            from\n                dba_ind_columns c\n            where INDEX_OWNER = '{OWNER}' and INDEX_NAME = '{OBJECT_NAME}'\n            order by c.index_name, c.column_position"}, 
  u'\u5206\u533a':{'': "\nselect\n  partition_position\n  , partition_name\n  , composite\n  , num_rows\n  , blocks\n  , subpartition_count\n  , high_value\n  , compression\nfrom\n    dba_tab_partitions\n where table_owner = '{OWNER}' and TABLE_NAME = '{OBJECT_NAME}' and partition_name = '{SUBOBJECT_NAME}'"}, 
  u'\u5b57\u6bb5':{'': "\nselect\n    column_id,\n    column_name,\n    data_type||CASE\n                    WHEN data_type = 'NUMBER' THEN '('||data_precision||','||data_scale||')'\n                    ELSE '('||data_length||')'\n                END AS data_type,\n    to_char(last_analyzed,'YYYY-MM-DD HH24') last_analyzed,\n    nullable,\n    num_distinct,\n    num_nulls,\n    histogram,\n    num_buckets\nFROM\n    dba_tab_cols\nwhere OWNER = '{OWNER}' and TABLE_NAME = '{OBJECT_NAME}' and column_name = '{SUBOBJECT_NAME}'"}}, 
 'db2':{u'\u8868':{u'\u8868':"\n            select\n  rtrim(TABSCHEMA) as OWNER,\n  TABNAME as TABLE_NAME,\n  COLCOUNT,\n  card as card,\n  NPAGES,\n  FPAGES,\n  FPAGES - NPAGES EPAGES,\n  tbspace,\n  to_char(stats_time,'yyyy-mm-dd hh24:mi:ss') as stats_time\nfrom syscat.tables\nwhere TABSCHEMA = '{OWNER}' and TABNAME = '{OBJECT_NAME}'", 
   u'\u5217':"\n              select\n    COLNO,\n    colname,\n    typename,\n    colcard,\n    length,\n    scale,\n    default,\n    nulls,\n    identity,\n    generated,\n    remarks,\n    keyseq\n  from\n    syscat.columns\n  where TABSCHEMA = '{OWNER}' and TABNAME = '{OBJECT_NAME}'\n  order by COLNO\n            ", 
   u'\u7d22\u5f15':"\n             SELECT\n      c.indname,\n      c.indextype,\n      c.uniquerule,\n      c.colnames,\n      c.NLEVELS,\n      c.nleaf,\n      c.num_empty_leafs,\n      c.numrids_deleted,\n      to_char(c.stats_time,'yyyy-mm-dd hh24:mi:ss') as stats_time\n  FROM syscat.indexes c\n    where TABSCHEMA = '{OWNER}' and TABNAME = '{OBJECT_NAME}'\norder by 1", 
   u'\u7d22\u5f15\u5217':"\nSELECT\n       key.indname,\n       key.colname,\n       key.colseq,\n       key.colorder\nFROM   SYSIBM.SYSINDEXCOLUSE KEY\n       JOIN sysibm.sysindexes IX\nON KEY.INDNAME = IX.name\n    where IX.TBCREATOR = '{OWNER}' and IX.TBNAME = '{OBJECT_NAME}'\n order by key.indname, key.colseq"}, 
  u'\u7d22\u5f15':{u'\u7d22\u5f15':"\n             SELECT\n      rtrim(c.TABSCHEMA) as OWNER,\n      c.TABNAME as TABLE_NAME,\n      c.indname,\n      c.indextype,\n      c.uniquerule,\n      c.colnames,\n      c.NLEVELS,\n      c.nleaf,\n      c.num_empty_leafs,\n      c.numrids_deleted,\n      to_char(c.stats_time,'yyyy-mm-dd hh24:mi:ss') as stats_time\n  FROM syscat.indexes c\n    where TABSCHEMA = '{OWNER}' and indname = '{OBJECT_NAME}'\norder by 1", 
   u'\u7d22\u5f15\u5217':"\nSELECT\n       key.indname,\n       key.colname,\n       key.colseq,\n       key.colorder\nFROM   SYSIBM.SYSINDEXCOLUSE KEY\n       JOIN sysibm.sysindexes IX\nON KEY.INDNAME = IX.name\n    where IX.TBCREATOR = '{OWNER}' and IX.name = '{OBJECT_NAME}'\n order by key.indname, key.colseq"}, 
  u'\u89c6\u56fe':{'DDL': "\n            select view_definition DDL from sysibm.VIEWS\nwhere table_schema = '{OWNER}' and TABLE_NAME = '{OBJECT_NAME}'"}, 
  u'\u51fd\u6570':{'DDL': "\n              select text DDL from syscat.ROUTINES\n              where routineschema='{OWNER}' and routinename = '{OBJECT_NAME}'\n          "}, 
  u'\u8fc7\u7a0b':{'DDL': "\n      select text DDL from syscat.ROUTINES\n      where routineschema='{OWNER}' and routinename = '{OBJECT_NAME}'"}, 
  u'\u89e6\u53d1\u5668':{'DDL': "\n            SELECT TEXT DDL\nFROM SYSIBM.SYSTRIGGERS\nWHERE  SCHEMA = '{OWNER}' and name = '{OBJECT_NAME}'"}, 
  u'\u5e8f\u5217':{'': "\n            select SEQSCHEMA OWNER, SEQNAME NAME, INCREMENT, START, MAXVALUE, CYCLE, CACHE, ORDER\nfrom syscat.sequences\nwhere SEQSCHEMA = '{OWNER}' and SEQNAME = '{OBJECT_NAME}'"}}, 
 'sqlserver':{'': {u'\u8868':"\n            SELECT\n    s.Name AS [SCHEMA],\n    t.NAME AS TABLE_NAME,\n    i.name as INDEX_NAME,\n    p.rows AS RowCounts,\n    a.total_pages*8/1024 SIZE_MB,\n    a.used_pages*8/1024 USED,\n    (a.total_pages - a.used_pages)*8/1024 FREE\nFROM\n    sys.tables t\nINNER JOIN\n    sys.indexes i ON t.OBJECT_ID = i.object_id\nINNER JOIN\n    sys.partitions p ON i.object_id = p.OBJECT_ID AND i.index_id = p.index_id\nINNER JOIN\n    sys.allocation_units a ON p.partition_id = a.container_id\nLEFT OUTER JOIN\n    sys.schemas s ON t.schema_id = s.schema_id\nWHERE\n    s.name = '{OWNER}' and t.name = '{OBJECT_NAME}'", 
       u'\u5217':"\n            SELECT ORDINAL_POSITION as [COLUMN_POSITION],COLUMN_NAME,DATA_TYPE,IS_NULLABLE as [NULLABLE],COLUMN_DEFAULT as [DEFAULT]\nFROM INFORMATION_SCHEMA.COLUMNS\nwhere TABLE_SCHEMA = '{OWNER}' and table_name = '{OBJECT_NAME}'\norder by ORDINAL_POSITION", 
       u'\u7d22\u5f15':"\n            SELECT\n    INDEX_NAME = ind.name,\n    INDEX_ID = ind.index_id,\n    INDEX_TYPE = ind.type_desc,\n    UNIQUENESS = ind.is_unique,\n    COLUMN_ID = ic.index_column_id,\n    COLUMN_NAME = col.name\nFROM\n    sys.indexes ind\nINNER JOIN\n    sys.index_columns ic ON  ind.object_id = ic.object_id and ind.index_id = ic.index_id\nINNER JOIN\n    sys.columns col ON ic.object_id = col.object_id and ic.column_id = col.column_id\nINNER JOIN\n    sys.tables t ON ind.object_id = t.object_id\nLEFT OUTER JOIN\n    sys.schemas s ON t.schema_id = s.schema_id\nWHERE\n    s.name = '{OWNER}' and t.name = '{OBJECT_NAME}'\n    ", 
       u'\u7ea6\u675f':"\n            SELECT\n  CONSTRAINT_NAME,\n  CONSTRAINT_TYPE\nFROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS\nwhere TABLE_SCHEMA = '{OWNER}' and table_name = '{OBJECT_NAME}'"}}}
DDL_Query = {'oracle':{'DDL': "\nselect\n    dbms_metadata.get_ddl( case when object_type like 'PACKAGE%' then 'PACKAGE'\n\t\t\t    when object_type like 'DATABASE LINK' then 'DB_LINK'\n\t\t\t    when object_type like 'MATERIALIZED VIEW' then 'MATERIALIZED_VIEW'\n\t\t\t    when object_type in ('JOB','SCHEDULE') then 'PROCOBJ'\n\t\t\t    else object_type end, object_name, owner ) DDL\nfrom\n\tdba_objects\nwhere\n    OWNER = '{OWNER}' and OBJECT_NAME = '{OBJECT_NAME}'\nAND object_type not like '%PARTITION'"}, 
 'mysql':{'DDL': '\n        show create {OBJECT_TYPE} {OWNER}.{OBJECT_NAME}\n        '}, 
 'sqlserver':{'DDL': "\n        SELECT OBJECT_DEFINITION (OBJECT_ID(N'{OWNER}.{OBJECT_NAME}')) AS [DDL];\n"}}
Type_TO_CN = {'oracle':{'SEQUENCE':'', 
  'PACKAGE':'', 
  'FUNCTION':'', 
  'PROCEDURE':'', 
  'DATABASE LINK':'', 
  'TRIGGER':'', 
  'DIRECTORY':'', 
  'MATERIALIZED VIEW':'', 
  'TABLE':'', 
  'INDEX':'', 
  'VIEW':'', 
  'TYPE':'', 
  'JOB':'', 
  'SCHEDULE':''}, 
 'db2':{'DB2 PACKAGE':'', 
  'FUNCTION':'', 
  'INDEX':'', 
  'MATERIALIZED QUERY TABLE':'', 
  'PROCEDURE':'', 
  'SEQUENCE':'', 
  'TABLE':'', 
  'TRIGGER':'', 
  'VIEW':''}, 
 'mysql':{'FUNCTION':'', 
  'INDEX':'', 
  'PROCEDURE':'', 
  'TABLE':'', 
  'TRIGGER':'', 
  'VIEW':''}, 
 'sqlserver':{'CHECK_CONSTRAINT':'CHECK', 
  'DEFAULT_CONSTRAINT':'', 
  'SQL_STORED_PROCEDURE':'', 
  'SQL_SCALAR_FUNCTION':'', 
  'RULE':'', 
  'REPLICATION_FILTER_PROCEDURE':'', 
  'SQL_TRIGGER':'', 
  'SQL_INLINE_TABLE_VALUED_FUNCTION':'', 
  'SQL_TABLE_VALUED_FUNCTION':'SQL', 
  'VIEW':'', 
  'USER_TABLE':''}}
CN_TO_Type = {'oracle':{u'\u5e8f\u5217':'SEQUENCE', 
  u'\u5305':'PACKAGE', 
  u'\u51fd\u6570':'FUNCTION', 
  u'\u8fc7\u7a0b':'PROCEDURE', 
  u'\u6570\u636e\u5e93\u94fe\u63a5':'DATABASE LINK', 
  u'\u89e6\u53d1\u5668':'TRIGGER', 
  u'\u76ee\u5f55':'DIRECTORY', 
  u'\u7269\u5316\u89c6\u56fe':'MATERIALIZED VIEW', 
  u'\u8868':'TABLE', 
  u'\u7d22\u5f15':'INDEX', 
  u'\u89c6\u56fe':'VIEW', 
  u'\u7c7b\u578b':'TYPE', 
  u'\u4efb\u52a1':'JOB', 
  u'\u8c03\u5ea6\u5668':'SCHEDULE'}, 
 'mysql':{u'\u51fd\u6570':'FUNCTION', 
  u'\u7d22\u5f15':'INDEX', 
  u'\u8fc7\u7a0b':'PROCEDURE', 
  u'\u8868':'TABLE', 
  u'\u89e6\u53d1\u5668':'TRIGGER', 
  u'\u89c6\u56fe':'VIEW'}, 
 'db2':{u'\u7a0b\u5e8f\u5305':'DB2 PACKAGE', 
  u'\u51fd\u6570':'FUNCTION', 
  u'\u7d22\u5f15':'INDEX', 
  u'\u7269\u5316\u89c6\u56fe':'MATERIALIZED QUERY TABLE', 
  u'\u8fc7\u7a0b':'PROCEDURE', 
  u'\u5e8f\u5217':'SEQUENCE', 
  u'\u8868':'TABLE', 
  u'\u89e6\u53d1\u5668':'TRIGGER', 
  u'\u89c6\u56fe':'VIEW'}, 
 'sqlserver':{u'CHECK\u7ea6\u675f':'CHECK_CONSTRAINT', 
  u'\u9ed8\u8ba4\u7ea6\u675f':'DEFAULT_CONSTRAINT', 
  u'\u5b58\u50a8\u8fc7\u7a0b':'SQL_STORED_PROCEDURE', 
  u'\u51fd\u6570':'SQL_SCALAR_FUNCTION', 
  u'\u89c4\u5219':'RULE', 
  u'\u590d\u5236\u8fc7\u6ee4\u8fc7\u7a0b':'REPLICATION_FILTER_PROCEDURE', 
  u'\u89e6\u53d1\u5668':'SQL_TRIGGER', 
  u'\u5185\u5d4c\u8868\u51fd\u6570':'SQL_INLINE_TABLE_VALUED_FUNCTION', 
  u'SQL\u8868\u503c\u51fd\u6570':'SQL_TABLE_VALUED_FUNCTION', 
  u'\u89c6\u56fe':'VIEW', 
  u'\u8868':'USER_TABLE'}}
Object_Type_Query = {'oracle':"\n    select object_type\n    from dba_objects\n    where OWNER = '{OWNER}' and OBJECT_NAME = '{OBJECT_NAME}'\n    AND object_type not like '%PARTITION'", 
 'db2':"\nselect\n    OBJECTTYPE as OBJECT_TYPE\nfrom SYSIBMADM.OBJECTOWNERS\nwhere rtrim(OWNER) = '{OWNER}' and OBJECTNAME = '{OBJECT_NAME}'\nand OBJECTTYPE in (\n'DB2 PACKAGE',\n'INDEX',\n'MATERIALIZED QUERY TABLE',\n'SEQUENCE',\n'TABLE',\n'TRIGGER',\n'VIEW')\nunion\nselect case when ROUTINETYPE = 'F' then 'FUNCTION' when ROUTINETYPE = 'P' then 'PROCEDURE' end as OBJECT_TYPE\nfrom syscat.ROUTINES\n  where rtrim(routineschema) = '{OWNER}' and routinename = '{OBJECT_NAME}'", 
 'mysql':"\nSELECT OBJECT_TYPE\nFROM (\n\tSELECT 'TABLE' AS OBJECT_TYPE\n\t\t,TABLE_NAME AS OBJECT_NAME\n\t\t,TABLE_SCHEMA AS OBJECT_SCHEMA\n\tFROM information_schema.TABLES\n\tUNION\n\tSELECT 'VIEW' AS OBJECT_TYPE\n\t\t,TABLE_NAME AS OBJECT_NAME\n\t\t,TABLE_SCHEMA AS OBJECT_SCHEMA\n\tFROM information_schema.VIEWS\n\tUNION\n\tSELECT ROUTINE_TYPE AS OBJECT_TYPE\n\t\t,ROUTINE_NAME AS OBJECT_NAME\n\t\t,ROUTINE_SCHEMA AS OBJECT_SCHEMA\n\tFROM information_schema.ROUTINES\n\tUNION\n\tSELECT 'TRIGGER' AS OBJECT_TYPE\n\t\t,TRIGGER_NAME AS OBJECT_NAME\n\t\t,TRIGGER_SCHEMA AS OBJECT_SCHEMA\n\tFROM information_schema.triggers\n\t) R\nWHERE R.OBJECT_SCHEMA = '{OWNER}' and R.OBJECT_NAME = '{OBJECT_NAME}'\n    ", 
 'sqlserver':"\n        select TYPE_DESC as [OBJECT_TYPE] from sys.objects\nWHERE name = '{OBJECT_NAME}' and schema_name(schema_id) = '{OWNER}'"}

def get_object_type(database, owner, object_name, options, db_name=None):
    query = Object_Type_Query.get(database.db_type).format(**options)
    flag, type_data = run_sql(database, query, db_name)
    if not flag:
        raise build_exception_from_java(type_data)
    if type_data:
        return type_data[0].get('OBJECT_TYPE')
    else:
        return type_data


def sqlserver_schema_data(database):
    query = "\n    SELECT NAME FROM master.dbo.sysdatabases where name not in ('master','model','tempdb', 'msdb')"
    flag, json_data = run_sql(database, query)
    if not flag:
        raise build_exception_from_java(json_data)
    db_list = [x.get('NAME') for x in json_data]
    schema_data = []
    query = Schema_Query.get(database.db_type)
    for db in db_list:
        flag, json_data = run_sql(database, query, db)
        if not flag:
            raise build_exception_from_java(json_data)
        else:
            schema_data = schema_data + json_data

    return schema_data


Rows_Query = {'oracle':'\n    select\n  OWNER,\n  TABLE_NAME,\n  num_rows as "ROWS"\nfrom dba_tables\n where\n owner not in (\'MGMT_VIEW\',\'MDDATA\',\'MDSYS\',\'SI_INFORMTN_SCHEMA\',\'ORDPLUGINS\',\'ORDSYS\',\'OLAPSYS\',\'SYSMAN\',\'ANONYMOUS\',\'XDB\',\'CTXSYS\',\'EXFSYS\',\'WMSYS\',\'ORACLE_OCM\',\'DBSNMP\',\'TSMSYS\',\'DMSYS\',\'DIP\',\'OUTLN\',\'SYSTEM\',\'SYS\',\'APPQOSSYS\', \'FLOWS_FILES\', \'JWT\', \'ORDDATA\', \'OWBSYS\', \'OWBSYS_AUDIT\', \'SCOTT\', \'SPATIAL_CSW_ADMIN_USR\', \'SPATIAL_WFS_ADMIN_USR\', \'XS$NULL\', \'YUNQU\') and owner not like \'APEX%\'\n and num_rows >= 0\n    ', 
 'db2':"\n    select\n  rtrim(TABSCHEMA) as OWNER,\n  TABNAME as TABLE_NAME,\n  card as ROWS\nfrom syscat.tables\nwhere rtrim(TABSCHEMA) not in ('DB2INST1', 'SYSCAT', 'SYSIBM', 'SYSIBMADM', 'SYSPUBLIC', 'SYSSTAT', 'SYSTOOLS')\nand card >= 0", 
 'sqlserver':"\n    SELECT\n    DB_NAME() + '.' + schema_name(t.schema_id) AS [OWNER],\n    t.NAME AS TABLE_NAME,\n    sum(p.rows) AS ROWS\nFROM\n    sys.tables t\nINNER JOIN\n    sys.partitions p ON t.object_id = p.OBJECT_ID\nwhere p.index_id = 0 and p.rows >=0\ngroup by t.schema_id, t.name", 
 'mysql':"\n    select TABLE_SCHEMA OWNER, TABLE_NAME, TABLE_ROWS as ROWS from information_schema.tables\n    where\n    TABLE_SCHEMA not in ('information_schema', 'mysql', 'performance_schema', 'sys', 'test')\n    and TABLE_ROWS >=0"}

def sqlserver_rows_data(database):
    query = "\n    SELECT NAME FROM master.dbo.sysdatabases where name not in ('master', 'tempdb', 'model', 'msdb')"
    flag, json_data = run_sql(database, query)
    if not flag:
        raise build_exception_from_java(json_data)
    db_list = [x.get('NAME') for x in json_data]
    schema_data = []
    query = Rows_Query.get(database.db_type)
    for db in db_list:
        flag, json_data = run_sql(database, query, db)
        if not flag:
            raise build_exception_from_java(json_data)
        else:
            schema_data = schema_data + json_data

    return schema_data
# okay decompiling ./restful/hawkeye/api/enum/schema_enum.pyc
