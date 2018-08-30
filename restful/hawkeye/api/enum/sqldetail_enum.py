# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/enum/sqldetail_enum.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 9619 bytes
from api.v1.monitor.services.runsqlService import run_batch_sql
from monitor.models import SQLMON
from datetime import datetime

def get_realtime_sql(sql_id, inst_id):
    return {'stats':f'''
            select
                INST_ID,
                CHILD_NUMBER,
                PLAN_HASH_VALUE,
                PARSING_SCHEMA_NAME,
                LAST_LOAD_TIME,
                MODULE,
                ACTION,
                SERVICE,
                ROUND(CPU_TIME/1E3) "ON CPU",
                ROUND(APPLICATION_WAIT_TIME/1E3) "Application",
                ROUND(CONCURRENCY_WAIT_TIME/1E3) "Concurrency",
                ROUND(CLUSTER_WAIT_TIME/1E3) "Cluster",
                ROUND(USER_IO_WAIT_TIME/1E3) "User I/O",
                EXECUTIONS,
                ROUND(ELAPSED_TIME/1E3) ELAPSED_TIME,
                ROUND(CPU_TIME/1E3) CPU_TIME,
                BUFFER_GETS,
                DISK_READS,
                DIRECT_WRITES,
                ROWS_PROCESSED,
                FETCHES
            from
                gv$sql
            where
                inst_id in ({inst_id}) and
                sql_id = '{sql_id}'
            order by elapsed_time desc''',  'plans':f'''
            select /*+ opt_param('parallel_execution_enabled','false') */
                INST_ID,
                CHILD_NUMBER,
                PLAN_HASH_VALUE,
                lpad(case when access_predicates is not null or filter_predicates is not null then '*' else '' end || id, 5, ' ') ID,
                lpad(' ',depth*2,' ')||operation || ' ' || options PLAN_STEP,
                OBJECT_NAME,
                OBJECT_TYPE,
                OBJECT_OWNER,
                cardinality,
                cost        COST,
                substr(access_predicates,1,3989) access_predicates,
                substr(filter_predicates,1,3989) filter_predicates
            from
                gv$sql_plan p
            where
                inst_id in ({inst_id})
            and sql_id  = '{sql_id}'
            order by child_number, p.id''',  'sqlmon':f'''
            select *
            from (select  STATUS,SQL_ID,round((LAST_REFRESH_TIME-SQL_EXEC_START)*24*3600) ELAPSED_TIME,
                           round(ELAPSED_TIME/1e6) DB_TIME,round(CPU_TIME/1e6) DB_CPU,
                           SQL_EXEC_ID,to_char(sql_exec_start,'YYYY-MM-DD HH24:MI:SS') SQL_EXEC_START,
                           SQL_PLAN_HASH_VALUE,INST_ID, USERNAME
                         from gv$sql_monitor
                   where sql_id = '{sql_id}'
                   and sql_text is not null
                   order by SQL_EXEC_START desc)''',  'binds':f'''
        select
            CHILD_NUMBER,
            NAME,
            POSITION,
            DATATYPE_STRING,
            case when datatype_string like 'TIMESTAMP%' then to_char(anydata.accesstimestamp(value_anydata),'YYYY-MM-DD HH24:MI:SS')
            else VALUE_STRING end VALUE_STRING,
            to_char(LAST_CAPTURED,'yyyy-mm-dd hh24:mi:ss') LAST_CAPTURED
        From gv$sql_bind_capture
        where sql_id = '{sql_id}'
        and inst_id in ({inst_id})
        order by CHILD_NUMBER, POSITION'''}


def get_hist_sql(sql_id, inst_id, begin_time, end_time):
    return {'stats':f'''with sqlstat as (select
            instance_number,
            snap_id,
            sql_id,
            plan_hash_value phv,
            executions_delta exec_delta,
            trunc(ELAPSED_TIME_DELTA/decode(executions_delta,0,1,executions_delta)/1e6) avg_elapse_time,
            trunc(CPU_TIME_DELTA/decode(executions_delta,0,1,executions_delta)/1e6) avg_cpu_time,
            trunc(rows_processed_delta/decode(executions_delta,0,1,executions_delta)) avg_rows,
            trunc(buffer_gets_delta/decode(executions_delta,0,1,executions_delta)) avg_cr,
            trunc(disk_reads_delta/decode(executions_delta,0,1,executions_delta)) avg_reads
        from
            dba_hist_sqlstat x
        where
            x.sql_id = '{sql_id}'
        and x.instance_number in ({inst_id})
        and x.snap_id in (select snap_id
            from dba_hist_snapshot
            where
                begin_interval_time between
                    (TO_DATE('1970-01-01','YYYY-MM-DD') + {begin_time} / 86400)
                and (TO_DATE('1970-01-01','YYYY-MM-DD') + {end_time} / 86400)
        ))
        select
            a.phv PLAN_HASH_VALUE,
            a.SNAP_TIME,
            nvl(b.exec_delta,0) EXEC_DELTA,
            nvl(b.avg_elapse_time,0) AVG_ELAPSE_TIME,
            nvl(b.avg_cpu_time,0) AVG_CPU_TIME,
            nvl(b.avg_cr,0) AVG_CRS,
            nvl(b.avg_reads,0) AVG_READS
        from
            (select x.snap_id, floor((to_date(to_char(x.begin_interval_time, 'yyyymmddhh24:mi:ss'),'yyyymmddhh24:mi:ss') - to_date('19700101', 'YYYYMMDD'))*24*3600*1000) SNAP_TIME, y.phv
            from
                (select snap_id, begin_interval_time from dba_hist_snapshot
                where
                begin_interval_time between
                    (TO_DATE('1970-01-01','YYYY-MM-DD') + {begin_time} / 86400)
                and (TO_DATE('1970-01-01','YYYY-MM-DD') + {end_time} / 86400)
                and instance_number in ({inst_id})) x,
                (select distinct phv phv from sqlstat) y) a
        left outer join sqlstat b on a.snap_id = b.snap_id and a.phv = b.phv order by a.snap_id''',  'plans':f'''
                select /*+ opt_param('parallel_execution_enabled','false') */
                    PLAN_HASH_VALUE,
                    lpad(case when access_predicates is not null or filter_predicates is not null then '*' else '' end || id, 5, ' ') ID,
                    lpad(' ',depth*2,' ')||operation || ' ' || options PLAN_STEP,
                    OBJECT_NAME,
                    OBJECT_TYPE,
                    OBJECT_OWNER,
                    cardinality,
                    cost        COST,
                    substr(access_predicates,1,3989) access_predicates,
                    substr(filter_predicates,1,3989) filter_predicates
                from
                    dba_hist_sql_plan p
                where
                    sql_id  = '{sql_id}'
                order by PLAN_HASH_VALUE,p.id''',  'binds':f'''
select
        SQL_ID,
        NAME,
        POSITION,
        DATATYPE_STRING,
        case when datatype_string like 'TIMESTAMP%' then to_char(anydata.accesstimestamp(value_anydata),'YYYY-MM-DD HH24:MI:SS')
        else VALUE_STRING end VALUE_STRING,
        to_char(LAST_CAPTURED,'yyyy-mm-dd hh24:mi:ss') LAST_CAPTURED
from dba_hist_sqlbind
where sql_id = '{sql_id}'
and INSTANCE_NUMBER in ({inst_id})
and snap_id in (select snap_id from dba_hist_snapshot
                where
                begin_interval_time between
                    (TO_DATE('1970-01-01','YYYY-MM-DD') + {begin_time} / 86400)
                and (TO_DATE('1970-01-01','YYYY-MM-DD') + {end_time} / 86400)
                and instance_number in ({inst_id}))
order by snap_id, position
        '''}


def gen_sql_mononitor_and_binds(database, sqlmon_list):
    sqlmon_filter_list = (',').join([("({},'{}',{})").format(x.get('INST_ID'), x.get('SQL_ID'), x.get('SQL_EXEC_ID')) for x in sqlmon_list])
    query = {'binds': f'''
        SELECT xt.*, (select child_number from gv$sql sql where sql.inst_id = x.inst_id and sql.address = x.SQL_CHILD_ADDRESS) CHILD_NUMBER, to_char(x.SQL_EXEC_START, 'yyyy-mm-dd hh24:mi:ss')LAST_CAPTURED, null REAL_DATA
FROM   (select xmltype(binds_xml) xml_data, SQL_EXEC_START, inst_id, SQL_CHILD_ADDRESS, sql_id from gv$sql_monitor
where binds_xml is not null and (inst_id, sql_id, sql_exec_id) in ({sqlmon_filter_list})) x,
       XMLTABLE('/binds/bind'
         PASSING x.xml_data
         COLUMNS
           name     VARCHAR2(100)  PATH '@name',
           pos     number PATH '@pos',
           DATATYPE_STRING       VARCHAR2(100)  PATH '@dtystr',
           VALUE_STRING  VARCHAR2(100) PATH '/'
         ) xt
        '''}
    flag, sqlmon_data = run_batch_sql(database, query)
    if not flag:
        return sqlmon_data
    else:
        if sqlmon_data.get('sqlmon'):
            for x in sqlmon_data.get('sqlmon'):
                m = SQLMON()
                m.inst_id = x.get('INST_ID')
                m.sql_id = x.get('SQL_ID')
                m.status = x.get('STATUS')
                m.username = x.get('USERNAME')
                m.elapsed_time = x.get('ELAPSED_TIME')
                m.db_time = x.get('DB_TIME')
                m.db_cpu = x.get('DB_CPU')
                m.sql_exec_id = x.get('SQL_EXEC_ID')
                m.sql_exec_start = x.get('SQL_EXEC_START')
                m.sql_plan_hash_value = x.get('SQL_PLAN_HASH_VALUE')
                m.sql_text = x.get('SQL_TEXT')
                m.sqlmon = x.get('SQLMON')
                m.database = database
                m.created_at = datetime.now().replace(microsecond=0)
                m.save()

        return sqlmon_data.get('binds')
# okay decompiling ./restful/hawkeye/api/enum/sqldetail_enum.pyc
