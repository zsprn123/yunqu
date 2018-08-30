# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/enum/report_enum.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 1817 bytes
Snapshot_Query = "\nselect\n    SNAP_ID, SNAP_TIME\nfrom\n(select SNAP_ID, to_char(min(END_INTERVAL_TIME),'yyyy-mm-dd hh24:mi:ss') SNAP_TIME\nfrom dba_hist_snapshot\ngroup by snap_id order by snap_id desc)\nwhere rownum <= {}"
Max_Snapshot_Query = "\nselect max(SNAP_ID) SNAP_ID, to_char(max(END_INTERVAL_TIME),'yyyy-mm-dd hh24:mi:ss') SNAP_TIME\nfrom dba_hist_snapshot\n"
DBID_Query = 'select DBID from v$database'
AWR_Query = {'global':{'alter':"alter session set nls_language='AMERICAN'", 
  'report':"select output from table(DBMS_WORKLOAD_REPOSITORY.AWR_GLOBAL_REPORT_HTML({db_id}, '{inst_str}', {begin_id}, {end_id}))"}, 
 'single':{'alter':"alter session set nls_language='AMERICAN'", 
  'report':'select output from table(DBMS_WORKLOAD_REPOSITORY.AWR_REPORT_HTML({db_id}, {inst_str}, {begin_id}, {end_id}))'}}
ASH_Query = {'global':{'alter':"alter session set nls_language='AMERICAN'", 
  'report':"select output from table(DBMS_WORKLOAD_REPOSITORY.ASH_GLOBAL_REPORT_HTML(\n        {db_id}, '{inst_str}', to_date('{begin_time}','yyyymmddhh24miss'), to_date('{end_time}','yyyymmddhh24miss')))"}, 
 'single':{'alter':"alter session set nls_language='AMERICAN'", 
  'report':"select output from table(DBMS_WORKLOAD_REPOSITORY.ASH_REPORT_HTML(\n        {db_id}, {inst_str}, to_date('{begin_time}','yyyymmddhh24miss'), to_date('{end_time}','yyyymmddhh24miss')))"}}

def get_key_inst_str(database, instance_id):
    key, inst_str = 'single', database.instance_id_list
    if database.instance_count > 1:
        if instance_id == database.db_name:
            key, inst_str = 'global', database.instance_id_list
        else:
            key, inst_str = 'single', instance_id
        return (key, inst_str)
# okay decompiling ./restful/hawkeye/api/enum/report_enum.pyc
