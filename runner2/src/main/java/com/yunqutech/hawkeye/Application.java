package com.yunqutech.hawkeye;

import org.springframework.boot.autoconfigure.jdbc.DataSourceBuilder;
import org.springframework.boot.web.servlet.FilterRegistrationBean;
import org.springframework.context.annotation.Bean;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.filter.CharacterEncodingFilter;

import java.util.*;

/**
 * Created by sid on 03/01/2018.
 */
@RestController
public class Application {
    private static final Map<String,JdbcTemplate> jdbcTemplatePool = new HashMap<>();

    @Bean
    public FilterRegistrationBean filterRegistrationBean() {
        FilterRegistrationBean registrationBean = new FilterRegistrationBean();
        CharacterEncodingFilter characterEncodingFilter = new CharacterEncodingFilter();
        characterEncodingFilter.setForceEncoding(true);
        characterEncodingFilter.setEncoding("UTF-8");
        registrationBean.setFilter(characterEncodingFilter);
        return registrationBean;
    }

    @RequestMapping(value = "/gettablelist")
    @ResponseBody
    List<List<String>> gettablelist(@RequestBody Map<String, Object> payload) {
        if(payload.isEmpty()){
            return Collections.emptyList();
        }
        JdbcTemplate jdbcTemplate = new JdbcTemplate(DataSourceBuilder
                .create()
                .username((String)payload.get("username"))
                .password((String)payload.get("password"))
                .url((String)payload.get("url"))
                .driverClassName((String)payload.get("driver_name"))
                .build());

        List<List<String>> resultSet = new ArrayList<>();
        List<String> queryList = getTableListQuery((String)payload.get("type"));

        for (int i=0; i<queryList.size(); i++) {
            List<String> result = jdbcTemplate.queryForList(queryList.get(i), String.class);
            resultSet.add(result);
        }

        return resultSet;
    }

    @RequestMapping(value = "/getschema")
    @ResponseBody
    List<List<Map<String, Object>>> getschema(@RequestBody Map<String, Object> payload) {
        if(payload.isEmpty()){
            return Collections.emptyList();
        }
        JdbcTemplate jdbcTemplate = new JdbcTemplate(DataSourceBuilder
                .create()
                .username((String)payload.get("username"))
                .password((String)payload.get("password"))
                .url((String)payload.get("url"))
                .driverClassName((String)payload.get("driver_name"))
                .build());

        List<List<Map<String, Object>>> resultSet = new  ArrayList<List<Map<String, Object>>>();
        List<String> queryList = getSchemaQuery((String)payload.get("type"));

        for (int i=0; i<queryList.size(); i++) {
            List<Map<String, Object>> result = jdbcTemplate.queryForList(queryList.get(i));
            resultSet.add(result);
        }

        return resultSet;
    }

    List<String> getTableListQuery(String type){
        ArrayList<String> list = new ArrayList<String>();

        if("mysql".equals(type)){
            list.add("select distinct TABLE_NAME from `INFORMATION_SCHEMA`.`TABLES` order by TABLE_NAME");
            list.add("SELECT distinct `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` order by 1");
            list.add("SELECT distinct `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`statistics` order by 1");
        }else if("oracle".equals(type)){
            list.add("SELECT distinct TABLE_NAME FROM ALL_TABLES where owner not in ('SYS','SYSTEM') order by TABLE_NAME");
            list.add("SELECT distinct COLUMN_NAME FROM ALL_TAB_COLUMNS where owner not in ('SYS','SYSTEM') order by 1");
            list.add("select distinct column_name from all_ind_columns c where c.table_owner not in ('SYS','SYSTEM') order by column_name");
        }else if("db2".equals(type)){
            list.add("SELECT distinct TABNAME TABLE_NAME FROM SYSCAT.TABLES order by TABNAME");
            list.add("SELECT distinct COLNAME FROM SYSCAT.COLUMNS order by 1");
            list.add("select distinct key.colname from SYSIBM.SYSINDEXCOLUSE KEY order by 1");
        }else if("sqlserver".equals(type)){
            list.add("select distinct name from sys.tables order by 1");
            list.add("select distinct COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS order by 1");
            list.add(" SELECT  " +
                    "     distinct col.name " +
                    " FROM  " +
                    "     sys.indexes ind  " +
                    " INNER JOIN  " +
                    "     sys.index_columns ic ON  ind.object_id = ic.object_id and ind.index_id = ic.index_id  " +
                    " INNER JOIN  " +
                    "     sys.columns col ON ic.object_id = col.object_id and ic.column_id = col.column_id  " +
                    " INNER JOIN  " +
                    "     sys.tables t ON ind.object_id = t.object_id " +
                    " LEFT OUTER JOIN  " +
                    "     sys.schemas s ON t.schema_id = s.schema_id " +
                    " ORDER BY 1 ");
        }else if("informix".equals(type)){
            list.add(" SELECT distinct t.tabname" +
                    "  FROM informix.systables AS t, informix.syscolumns AS c" +
                    " WHERE t.tabid = c.tabid" +
                    "   AND t.tabtype = 'T'" +
                    "   AND t.tabid >= 100 order by 1");
            list.add(" SELECT distinct c.colname" +
                    "  FROM informix.systables AS t, informix.syscolumns AS c" +
                    " WHERE t.tabid = c.tabid" +
                    "   AND t.tabtype = 'T'" +
                    "   AND t.tabid >= 100 order by 1");
            list.add("SELECT 'TODAY' FROM systables WHERE tabid = 1 and 1 > 2");
        }else if ("postgres".equals(type)) {
            list.add("SELECT distinct table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE' order by 1");
            list.add("select distinct attname" +
                    "  from pg_attribute order by 1");
            list.add(" select " +
                    "     distinct a.attname as column_name " +
                    " from " +
                    "     pg_class t, " +
                    "     pg_class i, " +
                    "     pg_index ix, " +
                    "     pg_attribute a " +
                    " where " +
                    "     t.oid = ix.indrelid " +
                    "     and i.oid = ix.indexrelid " +
                    "     and a.attrelid = t.oid " +
                    "     and a.attnum = ANY(ix.indkey) " +
                    "     and t.relkind = 'r' " +
                    " order by 1");
        }
        return list;
    }

    List<String> getSchemaQuery(String type){
        ArrayList<String> list = new ArrayList<String>();
        if("mysql".equals(type)){
            list.add("  select"
                    + "  `TABLE_SCHEMA` as TABLE_OWNER,"
                    + "  `TABLE_NAME`,"
                    + "  `COLUMN_NAME`,"
                    + "  `ORDINAL_POSITION`,"
                    + "  `COLUMN_DEFAULT`,"
                    + "  `IS_NULLABLE`,"
                    + "  `DATA_TYPE`"
                    + "  from information_schema.columns"
                    + " order by 2");

            list.add("  SELECT TABLE_SCHEMA  as TABLE_OWNER,"
                    + "    TABLE_NAME,"
                    + "    INDEX_SCHEMA,"
                    + "    INDEX_NAME,"
                    + "  GROUP_CONCAT(column_name ORDER BY seq_in_index) AS Columns"
                    + "  FROM information_schema.statistics"
                    + "  GROUP BY 1,2,3,4"
                    + " order by 2");


            list.add("  SELECT"
                    + "    TABLE_SCHEMA as TABLE_OWNER,"
                    + "    TABLE_NAME,"
                    + "    NON_UNIQUE,"
                    + "    INDEX_SCHEMA,"
                    + "    INDEX_NAME,"
                    + "    SEQ_IN_INDEX,"
                    + "    COLUMN_NAME,"
                    + "    COLLATION,"
                    + "    CARDINALITY,"
                    + "    NULLABLE,"
                    + "    INDEX_TYPE "
                    + "  FROM information_schema.statistics"
                    + " order by 2");

            list.add("  select"
                    + "    TABLE_SCHEMA as TABLE_OWNER,"
                    + "    TABLE_NAME,"
                    + "    CONSTRAINT_NAME,"
                    + "    COLUMN_NAME,"
                    + "    ORDINAL_POSITION,"
                    + "    POSITION_IN_UNIQUE_CONSTRAINT"
                    + "    REFERENCED_TABLE_SCHEMA,"
                    + "    REFERENCED_TABLE_NAME,"
                    + "    REFERENCED_COLUMN_NAME"
                    + "  from information_schema.KEY_COLUMN_USAGE"
                    + " order by 2");

        }else if("oracle".equals(type)){

            list.add("select"
                    + "  OWNER TABLE_OWNER,"
                    + "  TABLE_NAME,"
                    + "  NUM_ROWS,"
                    + "  BLOCKS,"
                    + "  AVG_ROW_LEN,"
                    + "  GLOBAL_STATS,"
                    + "  SAMPLE_SIZE,"
                    + "  to_char(last_analyzed,'YYYY-MM-DD HH24') last_analyzed "
                    + "from all_tables"
                    + " where owner not in ('MGMT_VIEW','MDDATA','MDSYS','SI_INFORMTN_SCHEMA','ORDPLUGINS','ORDSYS','OLAPSYS','SYSMAN','ANONYMOUS','XDB','CTXSYS','EXFSYS','WMSYS','ORACLE_OCM','DBSNMP','TSMSYS','DMSYS','DIP','OUTLN','SYSTEM','SYS') and owner not like 'APEX%'"
                    + " order by 2");


            list.add("select"
                    + "    owner TABLE_OWNER,"
                    + "    TABLE_NAME,"
                    + "    column_id,"
                    + "    column_name,"
                    + "    data_type||CASE"
                    + "                    WHEN data_type = 'NUMBER' THEN '('||data_precision||','||data_scale||')'"
                    + "                    ELSE '('||data_length||')'"
                    + "                END AS data_type,"
                    + "    to_char(last_analyzed,'YYYY-MM-DD HH24') last_analyzed,"
                    + "    nullable,"
                    + "    num_distinct,"
                    + "    num_nulls,"
                    + "    histogram,"
                    + "    num_buckets "
                    + "FROM"
                    + "    all_tab_cols"
                    + " where owner not in ('MGMT_VIEW','MDDATA','MDSYS','SI_INFORMTN_SCHEMA','ORDPLUGINS','ORDSYS','OLAPSYS','SYSMAN','ANONYMOUS','XDB','CTXSYS','EXFSYS','WMSYS','ORACLE_OCM','DBSNMP','TSMSYS','DMSYS','DIP','OUTLN','SYSTEM','SYS') and owner not like 'APEX%'"
                    + " order by 2");


            list.add("select"
                    + "    TABLE_OWNER,"
                    + "    TABLE_NAME,"
                    + "    owner ind_owner,"
                    + "    index_name,"
                    + "    index_type,"
                    + "    uniqueness,"
                    + "    status,"
                    + "    partitioned,"
                    + "    temporary,"
                    + "    blevel+1,"
                    + "    leaf_blocks,"
                    + "    distinct_keys,"
                    + "    num_rows,"
                    + "    clustering_factor ,"
                    + "    to_char(last_analyzed,'YYYY-MM-DD HH24') last_analyzed "
                    + "from"
                    + "    all_indexes"
                    + " where table_owner not in ('MGMT_VIEW','MDDATA','MDSYS','SI_INFORMTN_SCHEMA','ORDPLUGINS','ORDSYS','OLAPSYS','SYSMAN','ANONYMOUS','XDB','CTXSYS','EXFSYS','WMSYS','ORACLE_OCM','DBSNMP','TSMSYS','DMSYS','DIP','OUTLN','SYSTEM','SYS') and table_owner not like 'APEX%'"
                    + " order by 2");


            list.add("select"
                    + "    c.TABLE_OWNER,"
                    + "    c.TABLE_NAME,"
                    + "    c.index_name,"
                    + "    c.column_position,"
                    + "    c.column_name,"
                    + "    c.descend "
                    + "from"
                    + "    all_ind_columns c"
                    + " where c.table_owner not in ('MGMT_VIEW','MDDATA','MDSYS','SI_INFORMTN_SCHEMA','ORDPLUGINS','ORDSYS','OLAPSYS','SYSMAN','ANONYMOUS','XDB','CTXSYS','EXFSYS','WMSYS','ORACLE_OCM','DBSNMP','TSMSYS','DMSYS','DIP','OUTLN','SYSTEM','SYS') and c.table_owner not like 'APEX%'"
                    + " order by 2");


            list.add("select"
                    + "  TABLE_OWNER"
                    + "  , TABLE_NAME"
                    + "  , partition_position "
                    + "  , partition_name"
                    + "  , composite"
                    + "  , num_rows"
                    + "  , blocks"
                    + "  , subpartition_count"
                    + "  , high_value"
                    + "  , compression "
                    + "from"
                    + "    all_tab_partitions"
                    + " where table_owner not in ('MGMT_VIEW','MDDATA','MDSYS','SI_INFORMTN_SCHEMA','ORDPLUGINS','ORDSYS','OLAPSYS','SYSMAN','ANONYMOUS','XDB','CTXSYS','EXFSYS','WMSYS','ORACLE_OCM','DBSNMP','TSMSYS','DMSYS','DIP','OUTLN','SYSTEM','SYS') and table_owner not like 'APEX%'"
                    + " order by 2");

            list.add("select"
                    + "  TABLE_OWNER"
                    + "  ,TABLE_NAME"
                    + "  , partition_name"
                    + "  , subpartition_position"
                    + "  , subpartition_name"
                    + "  , num_rows"
                    + "  , blocks"
                    + "  , high_value"
                    + "  , compression "
                    + "From"
                    + "    all_tab_subpartitions"
                    + " where table_owner not in ('MGMT_VIEW','MDDATA','MDSYS','SI_INFORMTN_SCHEMA','ORDPLUGINS','ORDSYS','OLAPSYS','SYSMAN','ANONYMOUS','XDB','CTXSYS','EXFSYS','WMSYS','ORACLE_OCM','DBSNMP','TSMSYS','DMSYS','DIP','OUTLN','SYSTEM','SYS') and table_owner not like 'APEX%'"
                    + " order by 2");


            list.add("select"
                    + "     co.owner TABLE_OWNER,"
                    + "     co.TABLE_NAME,"
                    + "     co.constraint_name,"
                    + "     co.constraint_type,"
                    + "     co.r_constraint_name,"
                    + "     cc.column_name,"
                    + "     cc.position,"
                    + "     co.status,"
                    + "     co.validated "
                    + "from"
                    + "     all_constraints co,"
                    + "     all_cons_columns cc "
                    + "where"
                    + "    co.owner              = cc.owner "
                    + "and co.table_name         = cc.table_name "
                    + "and co.constraint_name    = cc.constraint_name "
                    + "and co.owner not in ('MGMT_VIEW','MDDATA','MDSYS','SI_INFORMTN_SCHEMA','ORDPLUGINS','ORDSYS','OLAPSYS','SYSMAN','ANONYMOUS','XDB','CTXSYS','EXFSYS','WMSYS','ORACLE_OCM','DBSNMP','TSMSYS','DMSYS','DIP','OUTLN','SYSTEM','SYS') and co.owner not like 'APEX%'"
                    + " order by 2");
        }else if("db2".equals(type)){
            list.add(" select " +
                    "   TABSCHEMA as TABLE_OWNER, " +
                    "   TABNAME as TABLE_NAME, " +
                    "   card as card, " +
                    "   tbspace, " +
                    "   to_char(stats_time,'yyyy-mm-dd hh24:mi:ss') as stats_time " +
                    " from syscat.tables");

            list.add("  select "
                    + "    RTRIM(TABSCHEMA) as TABLE_OWNER,"
                    + "    TABNAME as TABLE_NAME,"
                    + "    COLNO,"
                    + "    colname,"
                    + "    typename,"
                    + "    length,"
                    + "    scale,"
                    + "    default,"
                    + "    nulls,"
                    + "    identity,"
                    + "    generated,"
                    + "    remarks,"
                    + "    keyseq "
                    + "  from "
                    + "    syscat.columns"
                    + " order by 2");

            list.add("  SELECT"
                    + "      RTRIM(c.TABSCHEMA) as TABLE_OWNER,"
                    + "      c.TABNAME as TABLE_NAME,"
                    + "      c.indname as indname,"
                    + "      c.indextype,"
                    + "      c.uniquerule,"
                    + "      c.colnames,"
                    + "      c.NLEVELS,"
                    + "      to_char(c.stats_time,'yyyy-mm-dd hh24:mi:ss') as stats_time"
                    + "  FROM syscat.indexes c"
                    + " order by 2");

            list.add("SELECT "
                    + "       RTRIM(IX.TBCREATOR) as TABLE_OWNER, "
                    + "       IX.TBNAME as TABLE_NAME, "
                    + "       key.indname, "
                    + "       key.colname, "
                    + "       key.colseq, "
                    + "       key.colorder "
                    + "FROM   SYSIBM.SYSINDEXCOLUSE KEY "
                    + "       JOIN sysibm.sysindexes IX "
                    + "ON KEY.INDNAME = IX.name "
                    + " order by 2");

            list.add("  select"
                    + "    a.TABSCHEMA as TABLE_OWNER,"
                    + "    a.TABNAME as TABLE_NAME,"
                    + "    a.CONSTNAME,"
                    + "    a.TYPE,"
                    + "    b.COLNAME,"
                    + "    b.COLSEQ"
                    + "  from syscat.tabconst a, syscat.keycoluse b"
                    + "  where a.TABSCHEMA = b.TABSCHEMA"
                    + "  and a.TABNAME = b.TABNAME"
                    + "  and a.CONSTNAME = b.CONSTNAME"
                    + " order by 2");
        }else if("sqlserver".equals(type)){
            list.add("  SELECT " +
                    "      s.Name AS TABLE_OWNER," +
                    "      t.NAME AS TABLE_NAME," +
                    "      p.rows AS RowCounts," +
                    "      SUM(a.total_pages) * 8 AS TotalSpaceKB, " +
                    "      SUM(a.used_pages) * 8 AS UsedSpaceKB, " +
                    "      (SUM(a.total_pages) - SUM(a.used_pages)) * 8 AS UnusedSpaceKB" +
                    "  FROM " +
                    "      sys.tables t" +
                    "  INNER JOIN      " +
                    "      sys.indexes i ON t.OBJECT_ID = i.object_id" +
                    "  INNER JOIN " +
                    "      sys.partitions p ON i.object_id = p.OBJECT_ID AND i.index_id = p.index_id" +
                    "  INNER JOIN " +
                    "      sys.allocation_units a ON p.partition_id = a.container_id" +
                    "  LEFT OUTER JOIN " +
                    "      sys.schemas s ON t.schema_id = s.schema_id" +
                    "  WHERE " +
                    "      t.is_ms_shipped = 0" +
                    "  GROUP BY " +
                    "      t.Name, s.Name, p.Rows" +
                    "  ORDER BY " +
                    "      t.Name");


            list.add("  SELECT TABLE_SCHEMA TABLE_OWNER, TABLE_NAME, ORDINAL_POSITION,COLUMN_NAME,DATA_TYPE,IS_NULLABLE,COLUMN_DEFAULT" +
                    "  FROM INFORMATION_SCHEMA.COLUMNS order by 2");

            list.add("  SELECT " +
                    "      TABLE_OWNER = s.name," +
                    "      TABLE_NAME = t.name," +
                    "      IndexName = ind.name," +
                    "      IndexId = ind.index_id," +
                    "      Type_Desc = ind.type_desc," +
                    "      IS_Unique = ind.is_unique," +
                    "      ColumnId = ic.index_column_id," +
                    "      ColumnName = col.name" +
                    "  FROM " +
                    "      sys.indexes ind " +
                    "  INNER JOIN " +
                    "      sys.index_columns ic ON  ind.object_id = ic.object_id and ind.index_id = ic.index_id " +
                    "  INNER JOIN " +
                    "      sys.columns col ON ic.object_id = col.object_id and ic.column_id = col.column_id " +
                    "  INNER JOIN " +
                    "      sys.tables t ON ind.object_id = t.object_id" +
                    "  LEFT OUTER JOIN " +
                    "      sys.schemas s ON t.schema_id = s.schema_id" +
                    "  ORDER BY " +
                    "      t.name, ind.name, ind.index_id, ic.index_column_id");

            list.add("  SELECT" +
                    "    TABLE_SCHEMA TABLE_OWNER," +
                    "    TABLE_NAME," +
                    "    CONSTRAINT_NAME," +
                    "    CONSTRAINT_TYPE" +
                    "  FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS order by 2");
        }else if("informix".equals(type)){
            list.add(" select"
                    + "  rtrim(owner) as TABLE_OWNER,"
                    + "  rtrim(tabname) as TABLE_NAME,"
                    + "  nindexes,"
                    + "  rowsize,"
                    + "  ncols,"
                    + "  nrows,"
                    + "  created,"
                    + "  ustlowts"
                    + " FROM informix.systables AS t"
                    + " WHERE t.tabtype = 'T'"
                    + " AND t.tabid >= 100 and rtrim(t.owner) != ''"
                    + " order by 2");


            list.add(" SELECT "
                    + "   rtrim(t.owner) as TABLE_OWNER,"
                    + "   rtrim(t.tabname) as TABLE_NAME,"
                    + "   c.colno,"
                    + "   c.colname,                            "
                    + "    CASE coltype                                                                "
                    + "        WHEN 0 THEN 'char(' || TRIM(CAST (c.collength AS CHAR(5))) || ')'       "
                    + "        WHEN 1 THEN 'smallint'                                                  "
                    + "        WHEN 2 THEN 'integer'                                                   "
                    + "        WHEN 3 THEN 'float'                                                     "
                    + "        WHEN 4 THEN 'smallfloat'                                                "
                    + "        WHEN 5 THEN 'decimal(' ||                                               "
                    + "            TRIM(CAST(TRUNC(c.collength/256) AS VARCHAR(8)) || ',' ||           "
                    + "            CAST(c.collength - TRUNC(c.collength/256)*256 AS VARCHAR(8))) || ')'"
                    + "        WHEN 6 THEN 'serial'                                                    "
                    + "        WHEN 7 THEN 'date'                                                      "
                    + "        WHEN 8 THEN 'money(' ||                                                 "
                    + "            TRIM(CAST(TRUNC(c.collength/256) AS VARCHAR(8)) || ',' ||           "
                    + "            CAST(c.collength - TRUNC(c.collength/256)*256 AS VARCHAR(8))) || ')'"
                    + "        WHEN 9 THEN 'null'                                                      "
                    + "        WHEN 10 THEN 'datetime'                                                 "
                    + "        WHEN 11 THEN 'byte'                                                     "
                    + "        WHEN 12 THEN 'text'                                                     "
                    + "        WHEN 13 THEN 'varchar(' || TRIM(CAST(c.collength AS CHAR(5))) || ')'    "
                    + "        WHEN 14 THEN 'interval'                                                 "
                    + "        WHEN 15 THEN 'nchar(' || TRIM(CAST(c.collength AS CHAR(5))) || ')'      "
                    + "        WHEN 16 THEN 'nvarchar(' || TRIM(CAST(c.collength AS CHAR(5))) || ')'   "
                    + "        WHEN 17 THEN 'int8'                                                     "
                    + "        WHEN 18 THEN 'serial8'                                                  "
                    + "        WHEN 19 THEN 'set'                                                      "
                    + "        WHEN 20 THEN 'multiset'                                                 "
                    + "        WHEN 21 THEN 'list'                                                     "
                    + "        WHEN 22 THEN 'row'                                                      "
                    + "        WHEN 23 THEN 'collection'                                               "
                    + "        WHEN 24 THEN 'rowdef'                                                   "
                    + "        WHEN 256 THEN 'char(' || TRIM(CAST(c.collength AS CHAR(5))) ||          "
                    + "            ') not null'                                                        "
                    + "        WHEN 257 THEN 'smallint not null'                                       "
                    + "        WHEN 258 THEN 'integer not null'                                        "
                    + "        WHEN 259 THEN 'float not null'                                          "
                    + "        WHEN 260 THEN 'smallfloat not null'                                     "
                    + "        WHEN 261 THEN 'decimal('||                                              "
                    + "            TRIM(CAST(TRUNC(c.collength/256) AS VARCHAR(8)) || ',' ||           "
                    + "            CAST(c.collength - TRUNC(c.collength/256)*256 AS VARCHAR(8))) ||    "
                    + "            ') not null'                                                        "
                    + "        WHEN 262 THEN 'serial not null'                                         "
                    + "        WHEN 263 THEN 'date not null'                                           "
                    + "        WHEN 264 THEN 'money(' ||                                               "
                    + "            TRIM(CAST(TRUNC(c.collength/256) AS VARCHAR(8)) || ',' ||           "
                    + "            CAST(c.collength - TRUNC(c.collength/256)*256 AS VARCHAR(8))) ||    "
                    + "            ') not null'                                                        "
                    + "        WHEN 265 THEN 'null not null'                                           "
                    + "        WHEN 266 THEN 'datetime not null'                                       "
                    + "        WHEN 267 THEN 'byte not null'                                           "
                    + "        WHEN 268 THEN 'text not null'                                           "
                    + "        WHEN 269 THEN 'varchar(' || TRIM(CAST(c.collength AS CHAR(5))) ||       "
                    + "            ') not null'                                                        "
                    + "        WHEN 270 THEN 'interval not null'                                       "
                    + "        WHEN 271 THEN 'nchar(' || TRIM(CAST(c.collength AS CHAR(5))) ||         "
                    + "            ') not null'                                                        "
                    + "        WHEN 272 THEN 'nvarchar(' || TRIM(CAST(c.collength AS CHAR(5))) ||      "
                    + "            ') not null'                                                        "
                    + "        WHEN 273 THEN 'int8 not null'                                           "
                    + "        WHEN 274 THEN 'serial8 not null'                                        "
                    + "        WHEN 275 THEN 'set not null'                                            "
                    + "        WHEN 276 THEN 'multiset not null'                                       "
                    + "        WHEN 277 THEN 'list not null'                                           "
                    + "        WHEN 278 THEN 'row not null'                                            "
                    + "        WHEN 279 THEN 'collection not null'                                     "
                    + "        WHEN 280 THEN 'rowdef not null'                                         "
                    + "        ELSE 'Unknown'                                                          "
                    + "    END datatype"
                    + " FROM informix.systables AS t, informix.syscolumns AS c"
                    + " WHERE t.tabid = c.tabid"
                    + "  AND t.tabtype = 'T'"
                    + "  AND t.tabid >= 100 AND rtrim(t.owner) != ''"
                    + " order by 2");

            list.add("    select"
                    + "      rtrim(t.owner) as TABLE_OWNER,"
                    + "      rtrim(t.tabname) as TABLE_NAME,"
                    + "      i.idxname,"
                    + "      i.levels,"
                    + "      i.idxtype,"
//                    + "      i.indexkeys,"
                    + "      i.ustlowts"
                    + "    from systables t , sysindices i"
                    + "    where t.tabid = i.tabid"
                    + "    and t.tabid > 99 and rtrim(t.owner) != ''"
                    + " order by 2");


            list.add("  select"
                    + "    rtrim(tab.owner) as TABLE_OWNER,"
                    + "    rtrim(tab.tabname) as TABLE_NAME,"
                    + "    constr.*, "
                    + "    chk.*,"
                    + "    c1.colname col1,"
                    + "    c2.colname col2,"
                    + "    c3.colname col3,"
                    + "    c4.colname col4,"
                    + "    c5.colname col5"
                    + "  from sysconstraints constr"
                    + "    join systables tab on tab.tabid = constr.tabid"
                    + "    left outer join syschecks chk on chk.constrid = constr.constrid and chk.type = 'T'"
                    + "    left outer join sysindexes i on i.idxname = constr.idxname"
                    + "    left outer join syscolumns c1 on c1.tabid = tab.tabid and c1.colno = abs(i.part1)"
                    + "    left outer join syscolumns c2 on c2.tabid = tab.tabid and c2.colno = abs(i.part2)"
                    + "    left outer join syscolumns c3 on c3.tabid = tab.tabid and c3.colno = abs(i.part3)"
                    + "    left outer join syscolumns c4 on c4.tabid = tab.tabid and c4.colno = abs(i.part4)"
                    + "    left outer join syscolumns c5 on c5.tabid = tab.tabid and c5.colno = abs(i.part5)"
                    + "  where rtrim(tab.owner) != ''"
                    + " order by 2");
        } else if ("postgres".equals(type)) {
            list.add("  SELECT" +
                    "    nspname as TABLE_OWNER," +
                    "    relname AS TABLE_NAME," +
                    "    round(pg_total_relation_size(C.oid)/1024/1024) AS \"total_size(MB)\"," +
                    "    round(pg_relation_size(C.oid)/1024/1024) as \"table_size(MB)\"," +
                    "    round((pg_total_relation_size(C.oid)-pg_relation_size(C.oid))/1024/1024) as \"index_size(MB)\"," +
                    "    reltuples" +
                    "  FROM pg_class C" +
                    "  LEFT JOIN pg_namespace N ON (N.oid = C.relnamespace)" +
                    "  WHERE C.relkind <> 'i'" +
                    "  AND nspname !~ '^pg_toast'" +
                    "  order by 2");

            list.add("  SELECT" +
                    "      n.nspname as TABLE_OWNER," +
                    "      c.relname as TABLE_NAME," +
                    "      f.attnum AS number,  " +
                    "      cast(f.attname as varchar) AS name,  " +
                    "      f.attnotnull AS notnull,  " +
                    "      pg_catalog.format_type(f.atttypid,f.atttypmod) AS type,  " +
                    "      CASE  " +
                    "          WHEN p.contype = 'p' THEN 't'  " +
                    "          ELSE 'f'  " +
                    "      END AS primarykey,  " +
                    "      CASE  " +
                    "          WHEN p.contype = 'u' THEN 't'  " +
                    "          ELSE 'f'" +
                    "      END AS uniquekey, " +
                    "      CASE" +
                    "          WHEN p.contype = 'f' THEN cast(g.relname as varchar)" +
                    "      END AS foreignkey, " +
                    "      CASE" +
                    "          WHEN p.contype = 'f' THEN cast(p.confkey as varchar)" +
                    "      END AS foreignkey_fieldnum," +
                    "      CASE" +
                    "          WHEN f.atthasdef = 't' THEN d.adsrc" +
                    "      END AS default" +
                    "  FROM pg_attribute f  " +
                    "      JOIN pg_class c ON c.oid = f.attrelid  " +
                    "      JOIN pg_type t ON t.oid = f.atttypid  " +
                    "      LEFT JOIN pg_attrdef d ON d.adrelid = c.oid AND d.adnum = f.attnum  " +
                    "      LEFT JOIN pg_namespace n ON n.oid = c.relnamespace  " +
                    "      LEFT JOIN pg_constraint p ON p.conrelid = c.oid AND f.attnum = ANY (p.conkey)  " +
                    "      LEFT JOIN pg_class AS g ON p.confrelid = g.oid  " +
                    "  WHERE c.relkind = 'r'::char  " +
                    "      AND f.attnum > 0 ORDER BY 2");

            list.add("  SELECT" +
                    "        ns.nspname as TABLE_OWNER," +
                    "        ti.relname as TABLE_NAME," +
                    "       cast(i.relname as varchar) as indname," +
                    "       cast(am.amname as varchar) as indam," +
                    "       cast(idx.indkey as varchar) indkey," +
                    "       cast(ARRAY(" +
                    "       SELECT pg_get_indexdef(idx.indexrelid, k + 1, true)" +
                    "       FROM generate_subscripts(idx.indkey, 1) as k" +
                    "       ORDER BY k" +
                    "       ) as varchar) as indkey_names," +
                    "       cast(idx.indexprs IS NOT NULL as varchar) as indexprs," +
                    "       cast(idx.indpred IS NOT NULL as varchar) as indpred" +
                    "  FROM   pg_index as idx" +
                    "  JOIN   pg_class as i" +
                    "  ON     i.oid = idx.indexrelid" +
                    "  JOIN   pg_am as am" +
                    "  ON     i.relam = am.oid" +
                    "  JOIN   pg_namespace as ns" +
                    "  ON     ns.oid = i.relnamespace" +
                    "  AND    ns.nspname = ANY(current_schemas(false))" +
                    "  JOIN   pg_class as ti" +
                    "  ON     ti.oid = idx.indrelid" +
                    "  order by 2");
        }
        return list;
    }

    @RequestMapping(value = "/testconn")
    @ResponseBody
    String exetestconnc(@RequestBody Map<String, Object> payload) {
        if(payload.isEmpty()){
            return "error";
        }

        JdbcTemplate jdbcTemplate = new JdbcTemplate(DataSourceBuilder
                .create()
                .username((String)payload.get("username"))
                .password((String)payload.get("password"))
                .url((String)payload.get("url"))
                .driverClassName((String)payload.get("drivername"))
                .build());
        try {
            jdbcTemplate.getDataSource().getConnection().isValid(300);
        }catch (Exception e){
            return e.toString();
        }
        return "success";
    }
}
