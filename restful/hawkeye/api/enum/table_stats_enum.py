# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/enum/table_stats_enum.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 5527 bytes
from django.db.models import Q
from sqlaudit.models import Audit_Rule, Audit_Strategy

def get_table_stats_query(database, with_redundent_index_query=False):
    audit_rule_queryset = Audit_Rule.objects.filter((Q(database=database)) & (Q(enabled=True)))
    table_old_stats_rows = audit_rule_queryset.filter((Q(audit_type='TABLE_STATS')) & (Q(target='TABLE_OLD_STATS'))).values_list('predicate', flat=True)
    table_small_degree_rows = audit_rule_queryset.filter((Q(audit_type='TABLE_DOP')) & (Q(target='TABLE_SMALL_DEGREE'))).values_list('predicate', flat=True)
    table_old_stats_pred = table_old_stats_rows[0] if table_old_stats_rows else 1
    table_small_degree_pred = table_small_degree_rows[0] if table_small_degree_rows else 1
    TABLE_STATS_SQL_JSON = {'TABLE_OLD_STATS':"SELECT 'TABLE_OLD_STATS' SCOPE, OWNER, TABLE_NAME, to_char(TRUNC(SYSDATE-last_analyzed)) MESSAGE\n              FROM tables\n             WHERE last_analyzed < ADD_MONTHS(TRUNC(SYSDATE),-", 
     'TMP_TABLE_STATS':{table_old_stats_pred},  'TABLE_STALE_STATS':f''')''',  'TABLE_LOCKED_STATS':"\n                select 'TMP_TABLE_STATS', owner, table_name,  ''\n                  FROM tmp_tables\n                 WHERE num_rows IS NOT NULL", 
     'TABLE_MISSING_STATS':"\n                SELECT 'TABLE_STALE_STATS', owner, table_name,  ''\n                  FROM table_and_part_stats\n                 WHERE stale_stats = 'YES'\n                   AND partition_name IS NULL", 
     'PARTITION_STALE_STATS':"\n                SELECT 'TABLE_LOCKED_STATS', owner, table_name,  ''\n                  FROM table_and_part_stats\n                 WHERE stattype_locked IN ('ALL','DATA')\n                   AND partition_name IS NULL", 
     'PARTITION_LOCKED_STATS':"\n                SELECT 'TABLE_MISSING_STATS', owner, table_name,  ''\n                  FROM tables\n                 WHERE num_rows IS NULL", 
     'PARTITION_MISSING_STATS':"\n                SELECT 'PARTITION_STALE_STATS', owner, table_name,  partition_name\n                  FROM table_and_part_stats\n                 WHERE stale_stats = 'YES'\n                   AND partition_name IS NOT NULL", 
     'TABLE_INCONSISTENT_STATS':"\n                SELECT 'PARTITION_LOCKED_STATS', owner, table_name,  partition_name\n                  FROM table_and_part_stats\n                 WHERE stattype_locked IN ('ALL','DATA')\n                   AND partition_name IS NOT NULL", 
     'PARTITION_INCONSISTENT_STATS':"\n                SELECT 'PARTITION_MISSING_STATS', table_owner, table_name, partition_name\n                  FROM partitions\n                 WHERE num_rows IS NULL", 
     'TABLE_EMPTY_STATS':"\n                SELECT 'TABLE_INCONSISTENT_STATS', owner, table_name, ''\n                  FROM tables\n                 WHERE num_rows = 0 and blocks > 0", 
     'PARTITION_EMPTY_STATS':"\n                SELECT 'PARTITION_INCONSISTENT_STATS', table_owner, table_name,  partition_name\n                  FROM partitions\n                 WHERE num_rows = 0 and blocks > 0", 
     'TABLE_DEGREE':"\n                SELECT 'TABLE_EMPTY_STATS', owner, table_name,  ''\n                  FROM tables\n                 WHERE num_rows = 0 and blocks = 0", 
     'TABLE_SMALL_DEGREE':f'''
                SELECT 'PARTITION_EMPTY_STATS', table_owner, table_name, partition_name
                  FROM partitions
                 WHERE num_rows = 0 and blocks = 0
                SELECT 'TABLE_DEGREE', owner, table_name,  TRIM(degree)
                  FROM tables
                 WHERE TRIM(degree) <> '1'
                SELECT 'TABLE_SMALL_DEGREE', owner, table_name,  TRIM(degree)
                  FROM tables t, tablespaces tbs
                 WHERE t.tablespace_name = tbs.tablespace_name
                   AND TRIM(degree) <> '1'
                   AND (tbs.block_size * t.blocks)/POWER(10,9) <= {table_small_degree_pred}''',  'TABLE_INDEX_INCONSISTENT_DEGREE':"\n                SELECT 'TABLE_INDEX_INCONSISTENT_DEGREE', tables.owner, tables.table_name, to_char(COUNT(*))\n                  FROM tables,\n                       indexes\n                 WHERE tables.owner = indexes.table_owner\n                   AND tables.table_name = indexes.table_name\n                   AND tables.degree <> indexes.degree\n                 GROUP BY tables.owner, tables.table_name\n                 HAVING COUNT(*) > 0"}
    table_stats_target_list = audit_rule_queryset.filter(Q(audit_type='TABLE_STATS')).values_list('target', flat=True)
    sql_list = []
    for x in table_stats_target_list:
        sql_list.append(TABLE_STATS_SQL_JSON.get(x))

    if with_redundent_index_query:
        sql_list.append("SELECT 'REDUNDANT_INDEX', r.table_owner, r.table_name, r.index_name||' ('||r.indexed_columns||') '||i.index_name||' ('||i.indexed_columns||')'\n          FROM ind_cols r,\n               ind_cols i\n         WHERE i.table_owner = r.table_owner\n           AND i.table_name = r.table_name\n           AND i.index_type = r.index_type\n           AND i.index_name != r.index_name\n           AND i.indexed_columns LIKE r.indexed_columns||':%'\n           AND r.uniqueness = 'NONUNIQUE'")
    return (' UNION ALL ').join(sql_list)
# okay decompiling ./restful/hawkeye/api/enum/table_stats_enum.pyc
