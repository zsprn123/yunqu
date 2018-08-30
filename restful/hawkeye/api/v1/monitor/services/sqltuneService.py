# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/monitor/services/sqltuneService.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 16072 bytes
from monitor.models import Database, SQLMON
from api.v1.monitor.services.runsqlService import run_plsql, run_batch_sql, run_sql
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from common.util import build_exception_from_java
from api.enum.sql_audit_enum import get_oracle_sql_audit, get_db2_sql_audit

def get_sqlmon_report(pk, sql_id, inst_id, sql_exec_id, report_type, time_span):
    try:
        database = Database.objects.get(pk=pk)
        sqlmon = None
        sqlmon_data = ((((SQLMON.objects.filter(database=database)).filter(sql_id=sql_id)).filter(inst_id=inst_id)).filter(sql_exec_id=sql_exec_id)).first()
        if sqlmon_data:
            sqlmon = sqlmon_data.sqlmon
        else:
            query_json = {'alter_session':"ALTER SESSION SET EVENTS '31156 trace name context forever, level 0x400'", 
             'sqlmon':f'''
            select
                dbms_sqltune.report_sql_monitor(
                type=>'{report_type}',
                inst_id=>{inst_id},
                sql_id=>'{sql_id}',
                sql_exec_id=>{sql_exec_id},
                report_level=>'ALL')
                MONITOR_REPORT
            from dual'''}
            flag, sqlmon_data = run_batch_sql(database, query_json)
            sqlmon = sqlmon_data.get('sqlmon')[0].get('MONITOR_REPORT') if sqlmon_data.get('sqlmon') else ''
        sqlmon = sqlmon.replace('http://download.oracle.com', '/static') if sqlmon else ''
        return {'report_html': sqlmon}
    except ObjectDoesNotExist:
        return {'error_message': ''}
    except Exception as err:
        return {'error_message': str(err)}


def execute_sqltuning_task(pk, sql_id, timeout):
    try:
        database = Database.objects.get(pk=pk)
        import re
        dt_postfix = datetime.now().strftime('%Y-%m-%d_%H:%M')
        taskname = sql_id + '_' + dt_postfix
        query_submit_job = f'''
        declare
        a varchar2(100);
        begin
            BEGIN
            dbms_sqltune.execute_tuning_task('%s');
            EXCEPTION when others then
                null;
            end;
            a := dbms_sqltune.create_tuning_task(
                 task_name=>'{taskname}',
                 description=>'{taskname}',
                 scope=>dbms_sqltune.scope_comprehensive,
                 time_limit=>{timeout},
                 sql_id=>'{sql_id}'
             );
             dbms_sqltune.execute_tuning_task('{taskname}');
        end;'''
        query_report = {'report':f'''select dbms_sqltune.report_tuning_task('{taskname}') report FROM dual''',  'benefit':f'''
            select hint, benefit from (
            select case when attr5 like 'OPT_ESTIMATE%' then cast(attr5 as varchar2(4000)) when attr1 like 'OPT_ESTIMATE%' then attr1 end hint,benefit
            from dba_advisor_recommendations t join dba_advisor_rationale r using (task_id,rec_id)
            where t.task_name = '{taskname}' and t.type='SQL PROFILE'
            --and r.message='This attribute adjusts optimizer estimates.'
        ) where hint is not null order by to_number(regexp_replace(hint,'^.*=([0-9.]+)[^0-9]*$','\1'))'''}
        flag, result = run_plsql(database, query_submit_job)
        if not flag:
            raise build_exception_from_java(result)
        flag, sqltune_data = run_batch_sql(database, query_report)
        accept_sql_profile = False
        sql_list = None
        report_data = sqltune_data.get('report')
        sqltune_report = report_data[0].get('REPORT') if report_data else ''
        if re.search('accept_sql_profile', sqltune_report, re.IGNORECASE):
            sql_list = re.findall('execute dbms_sqltune.accept_sql_profile[^;]+;', sqltune_report, re.IGNORECASE)
            for idx, val in enumerate(sql_list):
                sql_list[idx] = re.sub('$', '\n end;', re.sub('execute', 'begin \n', val))

            accept_sql_profile = True
        sqltune_result = {'report':report_data, 
         'action':sql_list, 
         'accept_sql_profile':accept_sql_profile}
        return sqltune_result
    except ObjectDoesNotExist:
        return {'error_message': ''}
    except Exception as err:
        return {'error_message': str(err)}


def get_sql_audit(pk, sql_id, sql_text=None, plan=[], only_tune=False):
    try:
        database = Database.objects.get(pk=pk)
        db_type = database.db_type
        audit_result = {}
        if db_type == 'oracle':
            audit_result = get_oracle_sql_audit(database, sql_id, only_tune)
        else:
            if db_type == 'db2':
                audit_result = get_db2_sql_audit(database, sql_id, sql_text, plan)
        return audit_result
    except ObjectDoesNotExist:
        return {'error_message': ''}
    except Exception as err:
        return {'error_message': str(err)}


def get_sql_tune(database, audit_result, full_plan=None):
    from collections import defaultdict
    sql_tune_rules = [
     (u'\u5168\u8868\u626b\u63cf', 'create_index_fts'), (u'\u4f18\u5316\u5668\u4f30\u7b97\u503c\u548c\u5b9e\u9645\u503c\u7684\u76f8\u5dee\u8fc7\u5927',
 'gather_stats'), (u'\u5b9e\u9645\u6570\u636e\u91cf\u5728\u76f8\u90bb\u64cd\u4f5c\u7684\u76f8\u5dee\u8fc7\u5927',
 'create_index_gap')]
    tune_result = []
    for x in sql_tune_rules:
        plans = audit_result.get(x[0])
        if plans:
            template = x[1]
            func_str = f'''{template}(database, plans, full_plan)'''
            result = eval(func_str)
            tune_result = tune_result + result

    tune_result = list(set(tune_result))
    result = defaultdict(list)
    for x in tune_result:
        if 'CREATE INDEX' in x:
            result[''].append(x)
        else:
            result[''].append(x)

    return result


def create_index_fts(database, plans, full_plan=None):
    result = []
    for x in plans:
        filter = x.get('FILTER_PREDICATES')
        access = x.get('ACCESS_PREDICATES')
        card = x.get('CARDINALITY')
        owner = x.get('OBJECT_OWNER')
        name = x.get('OBJECT_NAME')
        num_rows = 0
        query = f'''select NUM_ROWS from dba_tables where owner = '{owner}' and table_name = '{name}''''
        flag, table_data = run_sql(database, query)
        if flag:
            if table_data:
                num_rows = table_data[0].get('NUM_ROWS')
        if card == 1 or card <= num_rows * 0.05:
            col_str = ''
            if filter or access:
                if filter:
                    col_str = col_str + filter
                if access:
                    col_str = col_str + access
                owner = x.get('OBJECT_OWNER')
                name = x.get('OBJECT_NAME')
                create_index_stmt = gen_create_index_stmt(database, owner, name, col_str)
                if create_index_stmt:
                    result.append(create_index_stmt)

    return list(set(result))


def gather_stats(database, plans, full_plan=None):
    result = []
    for x in plans:
        owner = x.get('OBJECT_OWNER')
        name = x.get('OBJECT_NAME')
        object_type = x.get('OBJECT_TYPE')
        table_name = ''
        if object_type == 'TABLE':
            table_name = name
        if object_type == 'INDEX':
            query = f'''select TABLE_OWNER, TABLE_NAME from dba_indexes where owner = '{owner}' and index_name = '{name}''''
            flag, table_data = run_sql(database, query)
            if flag:
                if table_data:
                    row = table_data[0]
                    owner, table_name = row.get('TABLE_OWNER'), row.get('TABLE_NAME')
        if table_name:
            gather_stats_stmt = f'''EXEC DBMS_STATS.GATHER_TABLE_STATS('{owner}', '{table_name}');'''
            result.append(gather_stats_stmt)

    return list(set(result))


def create_index_gap(database, plans, full_plan=None):
    result = []
    for x in plans:
        sql_plan_hash_value = x.get('SQL_PLAN_HASH_VALUE')
        plan_line_id = x.get('PLAN_LINE_ID')
        plan_operation = x.get('PLAN_OPERATION')
        object_name = x.get('OBJECT_NAME')
        object_owner = x.get('OBJECT_OWNER')
        plan_cardinality = x.get('PLAN_CARDINALITY')
        starts = x.get('STARTS')
        output_rows = x.get('OUTPUT_ROWS')
        parent_plan_operation = x.get('PARENT_PLAN_OPERATION')
        parent_plan_options = x.get('PARENT_PLAN_OPTIONS')
        parent_output_rows = x.get('PARENT_OUTPUT_ROWS')
        plan_parent_id = x.get('PLAN_PARENT_ID')
        object_type = x.get('OBJECT_TYPE')
        parent_object_object_type = x.get('PARENT_PLAN_OBJECT_TYPE')
        parent_object_object_name = x.get('PARENT_PLAN_OBJECT_NAME')
        parent_object_object_owner = x.get('PARENT_PLAN_OBJECT_OWNER')
        owner = ''
        table_name = ''
        query = object_type == 'INDEX' and parent_object_object_type == 'TABLE' and parent_plan_operation == 'TABLE ACCESS' and parent_plan_options == 'BY INDEX ROWID' and "select TABLE_OWNER, TABLE_NAME from dba_indexes where owner = '{object_owner}' and index_name = '{object_name}'"
        flag, table_data = run_sql(database, query)
        row = flag and table_data and table_data[0]
        owner, table_name = row.get('TABLE_OWNER'), row.get('TABLE_NAME')
        if owner != parent_object_object_owner:
            if parent_object_object_name != table_name:
                continue
            else:
                if object_type == 'TABLE':
                    if plan_operation == 'TABLE ACCESS':
                        if parent_plan_options == 'HASH JOIN':
                            owner, table_name = object_owner, object_name
                        else:
                            continue
                        plan = full_plan.get(str(sql_plan_hash_value))
                        if plan:
                            line = plan[plan_line_id]
                            parent_line = plan[plan_parent_id]
                            filter = line.get('FILTER_PREDICATES')
                            access = line.get('ACCESS_PREDICATES')
                            parent_filter = parent_line.get('FILTER_PREDICATES')
                            parent_access = parent_line.get('ACCESS_PREDICATES')
                            col_str = ''
                            if filter:
                                col_str = col_str + ' ' + filter
                            if access:
                                col_str = col_str + ' ' + access
                            if parent_filter:
                                col_str = col_str + ' ' + parent_filter
                            if parent_access:
                                col_str = col_str + ' ' + parent_access
                            create_index_stmt = gen_create_index_stmt(database, owner, table_name, col_str)
                            if create_index_stmt:
                                result.append(create_index_stmt)

    return list(set(result))


def gen_create_index_stmt(database, owner, table_name, col_str):
    import re
    col_with_alias = re.compile('"."([\\w]+)"(.)')
    col_without_alias = re.compile('"([\\w]+)"(.)')
    m = col_with_alias.findall(col_str)
    if not m:
        m = col_without_alias.findall(col_str)
    if m:
        col_list_pre = list(set([e[0] for e in m if e[1] == '=' or e[1] == ')']))
        col_list_post = list(set([e[0] for e in m if e[1] != ')']))
        col_list = col_list_pre + col_list_post
        col_list = verify_columns(database, owner, table_name, col_list)
        if col_list:
            col_list = (',').join(col_list)
            create_index_stmt = f'''CREATE INDEX {owner}.IDX_{table_name} ON {owner}.{table_name}({col_list});'''
        else:
            create_index_stmt = None
        return create_index_stmt
    else:
        return


def verify_columns(database, owner, table_name, col_list):
    query = f'''
    select
    COLUMN_NAME
FROM
    dba_tab_cols
where OWNER = '{owner}' and TABLE_NAME = '{table_name}''''
    flag, table_data = run_sql(database, query)
    if flag:
        if table_data:
            table_colums = [x.get('COLUMN_NAME') for x in table_data]
            return [c for c in col_list if c in table_colums]
        return []


def accept_sql_profile(pk, action):
    try:
        database = Database.objects.get(pk=pk)
        flag, result = run_plsql(database, action)
        if not flag:
            raise build_exception_from_java(result)
        return {'OK': True}
    except ObjectDoesNotExist:
        return {'error_message': ''}
    except Exception as err:
        return {'error_message': str(err)}


def apply_sql_profile(pk, sql_id, plan_hash_value):
    import re
    try:
        database = Database.objects.get(pk=pk)
        instance_id_list = database.instance_id_list
        query_json = {'SQLTEXT':f'''select * from (select REPLACE(sql_fulltext, CHR(00), ' ') SQLTEXT from gv$sql where inst_id in ({instance_id_list}) and sql_id='{sql_id}' and rownum = 1 union all
        select REPLACE(SQL_TEXT, CHR(00), ' ') from DBA_HIST_SQLTEXT where sql_id='{sql_id}' and rownum = 1) where rownum=1''',  'HINT':f'''
        select /*+ opt_param('parallel_execution_enabled', 'false') */ 'q''[' || SUBSTR(EXTRACTVALUE(VALUE(h), '/hint'), 1, 4000) || ']'',' HINT
        from
        (
            select other_xml from
            (
                SELECT other_xml
                FROM gv$sql_plan
                WHERE sql_id = '{sql_id}'
                and inst_id in ({instance_id_list})
                AND plan_hash_value = {plan_hash_value}
                AND other_xml IS NOT NULL
                and rownum = 1
                union all
                SELECT other_xml
                FROM dba_hist_sql_plan
                WHERE sql_id = '{sql_id}'
                AND plan_hash_value = {plan_hash_value}
                AND other_xml IS NOT NULL
                and rownum = 1
            ) where rownum = 1
        ) p, table(xmlsequence(extract(xmltype(p.other_xml),'/*/outline_data/hint'))) h'''}
        flag, result = run_batch_sql(database, query_json)
        if not flag:
            raise build_exception_from_java(result)
        sqltext = ''
        if result.get('SQLTEXT'):
            sqltext = result.get('SQLTEXT')[0].get('SQLTEXT') if result.get('SQLTEXT') else ''
        sqltext = ('\n').join((line.strip() for line in re.findall('.{1,160}(?:\\s+|$)', sqltext)))
        profile_name = 'coe_' + sql_id + '_' + plan_hash_value
        outlines = []
        outlines.append('DECLARE')
        outlines.append('sql_txt CLOB;')
        outlines.append('h       SYS.SQLPROF_ATTR;')
        outlines.append('BEGIN')
        outlines.append("sql_txt := q'[")
        outlines.append(sqltext)
        outlines.append("]';")
        outlines.append('h := SYS.SQLPROF_ATTR(')
        outlines.append("q'[BEGIN_OUTLINE_DATA]',")
        for hint in result.get('HINT'):
            tmp = ''
            if len(hint.get('HINT')) > 500:
                tmp = ("]',\nq'[").join((line.strip() for line in re.findall('.{1,160}(?:\\s+|$)', hint.get('HINT'))))
            else:
                tmp = hint.get('HINT')
            outlines.append(tmp)

        outlines.append("q'[END_OUTLINE_DATA]');")
        outlines.append('DBMS_SQLTUNE.IMPORT_SQL_PROFILE (')
        outlines.append('sql_text    => sql_txt,')
        outlines.append('profile     => h,')
        outlines.append("name        => '" + profile_name + "',")
        outlines.append("description => '" + profile_name + "',")
        outlines.append("category    => 'DEFAULT',")
        outlines.append('validate    => FALSE,')
        outlines.append('replace     => TRUE,')
        outlines.append('force_match => FALSE /* TRUE:FORCE (match even when different literals in SQL). FALSE:EXACT (similar to CURSOR_SHARING) */ );')
        outlines.append('END;')
        import_sql_profile = ('\n').join(outlines)
        flag, result = run_plsql(database, import_sql_profile)
        if not flag:
            raise build_exception_from_java(result)
        return {'OK': True}
    except ObjectDoesNotExist:
        return {'error_message': ''}
    except Exception as err:
        return {'error_message': str(err)}
# okay decompiling ./restful/hawkeye/api/v1/monitor/services/sqltuneService.pyc
