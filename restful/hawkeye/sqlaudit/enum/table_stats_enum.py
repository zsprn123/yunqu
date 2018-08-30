# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./sqlaudit/enum/table_stats_enum.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 2771 bytes
TABLE_STATS_JSON = {'TABLE_OLD_STATS':' {} ',  'INDEX_OLD_STATS':' {} ', 
 'TMP_TABLE_STATS':'', 
 'TABLE_STALE_STATS':'(stale)', 
 'TABLE_LOCKED_STATS':'', 
 'TABLE_MISSING_STATS':': {}', 
 'TABLE_EMPTY_STATS':' (:0, :0)', 
 'TABLE_INCONSISTENT_STATS':'(:{}) ', 
 'TABLE_PARTITIONS':' {}', 
 'TABLE_SUBPARTITIONS':' {}', 
 'PARTITION_STALE_STATS':'(stale)', 
 'PARTITION_LOCKED_STATS':'', 
 'PARTITION_MISSING_STATS':': {}', 
 'PARTITION_INCONSISTENT_STATS':'(blocks = {})  num_rows = 0', 
 'PARTITION_EMPTY_STATS':' (0 rows and 0 blocks)', 
 'TABLE_DEGREE':'{}', 
 'TABLE_SMALL_DEGREE':'(GB), {}', 
 'TABLE_INDEX_INCONSISTENT_DEGREE':'{}', 
 'HAS_RAW':'{}LONG, RAW, LONG RAW', 
 'BASEFILE_LOB':'{}LOB BASEFILE ', 
 'MISSING_PK':'', 
 'REDUNDANT_INDEX':': {}', 
 'SINGLE_TABLE_INDEXES':'{}', 
 'INDEX_COLUMNS':'{}', 
 'INDEX_MISSING_STATS':': {}', 
 'SEQUENCE_CACHE':': {}', 
 'SEQUENCE_INCREMENT_BY':'(INCREMENT_BY): {}', 
 'TABLE_NOPARTITION':': {} GB', 
 'MULTI_RANGE_KEY':': {}', 
 'SKEW_PARTITION':': {}', 
 'GLOBAL_INDEX':'global: {}', 
 'SKEW_COLUMN':': {}%', 
 'OBJECT_CREATED':': {}', 
 'OBJECT_DDL':' DDL : {}', 
 'JOIN_NULL':': {}', 
 'CHAR_COL':'{}CHAR', 
 'INDEX_EMPTY_LEAFS':': {}', 
 'INDEX_RIDS_DELETED':': {}', 
 'INDEX_NLEVELS':'(NLEVELS): {}', 
 'TABLE_EMPTY_PAGES':': {}'}

def format_table_stats(template, detail_result):
    new_result = []
    print(template)
    for x in detail_result:
        item = x
        if 'MESSAGE' in x:
            if TABLE_STATS_JSON.get(template):
                item['MESSAGE'] = TABLE_STATS_JSON.get(template).format(x.get('MESSAGE'))
        new_result.append(item)

    return new_result
# okay decompiling ./restful/hawkeye/sqlaudit/enum/table_stats_enum.pyc
