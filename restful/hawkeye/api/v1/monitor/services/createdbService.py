# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/monitor/services/createdbService.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 6983 bytes
from alarm.enum.alarm_warn_enum import WARN_ENUM
from alarm.models import Warn_Config, Warn_Config_Template
from api.v1.monitor.services.runsqlService import run_sql_with_dict
from api.enum.database_enum import DatabaseType
from monitor.models import Database
from api.v1.sqlaudit.services.initialService import sqlaudit_init
from collections import defaultdict
from hosts.models import Host

def createdb(request):
    conn = request.data
    if request.data.get('db_type') == DatabaseType.ORACLE.value:
        query1 = 'select count(*) INSTANCE_COUNT from gv$instance'
        query2 = 'select INSTANCE_NAME from gv$instance order by instance_name'
        query3 = 'select to_char(INSTANCE_NUMBER) INSTANCE_NUMBER from gv$instance order by INSTANCE_NUMBER'
        query4 = "select SUBSTR(version,1,INSTR(version,'.')-1) VERSION from PRODUCT_COMPONENT_VERSION where rownum = 1"
        query5 = "select decode(database_role,'PRIMARY','PRIMARY','STANDBY') ROLE from v$database"
        flag, json_data = run_sql_with_dict(conn, query1)
        request.data['instance_count'] = json_data[0].get('INSTANCE_COUNT')
        flag, json_data = run_sql_with_dict(conn, query2)
        request.data['instance_list'] = (',').join([x.get('INSTANCE_NAME') for x in json_data])
        flag, json_data = run_sql_with_dict(conn, query3)
        request.data['instance_id_list'] = (',').join([x.get('INSTANCE_NUMBER') for x in json_data])
        flag, json_data = run_sql_with_dict(conn, query4)
        request.data['version'] = json_data[0].get('VERSION')
        flag, json_data = run_sql_with_dict(conn, query5)
        request.data['role'] = json_data[0].get('ROLE')
    else:
        if request.data.get('db_type') == DatabaseType.MYSQL.value:
            query1 = 'select @@VERSION'
            query2 = 'show slave status'
            flag, json_data = run_sql_with_dict(conn, query1)
            request.data['version'] = json_data[0].get('@@VERSION')
            flag, json_data = run_sql_with_dict(conn, query2)
            request.data['role'] = 'STANDBY' if json_data else 'PRIMARY'
        else:
            if request.data.get('db_type') == DatabaseType.DB2.value:
                query = 'SELECT substr(service_level,6) VERSION FROM TABLE (sysproc.env_get_inst_info()) as INSTANCEINFO'
                flag, json_data = run_sql_with_dict(conn, query)
                request.data['version'] = json_data[0].get('VERSION')
        return request


def init_warnconfig(database, original_warn_dict={}, original_critical_dict={}):
    warn_config_list = []
    if isinstance(database, Database):
        (Warn_Config.objects.filter(database=database)).delete()
        global_warn_config_list = Warn_Config_Template.objects.filter(db_type=database.db_type)
    else:
        (Warn_Config.objects.filter(host=database)).delete()
        global_warn_config_list = Warn_Config_Template.objects.filter(db_type='host')
    for global_warn_config in global_warn_config_list:
        category = global_warn_config.category
        warn = original_warn_dict.get(category) if original_warn_dict.get(category) else global_warn_config.warn_threshold
        critical = original_critical_dict.get(category) if original_critical_dict.get(category) else global_warn_config.critical_threshold
        warn_config = Warn_Config(category=category, description=global_warn_config.description,
          warn_threshold=warn,
          critical_threshold=critical,
          template=global_warn_config,
          status=global_warn_config.status,
          optional=global_warn_config.optional)
        if isinstance(database, Database):
            warn_config.database = database
        else:
            warn_config.host = database
        warn_config_list.append(warn_config)

    Warn_Config.objects.bulk_create(warn_config_list)


def init_global_warnconfig():
    warnCategory_dict = WARN_ENUM
    global_warn_config_list_by_type = defaultdict(list)
    global_warn_config_list = []
    for db_type, warn_category in warnCategory_dict.items():
        for e in warn_category:
            if not ((Warn_Config_Template.objects.filter(db_type=db_type)).filter(category=e.name)).exists():
                value = e.value
                description = value.get('description', '')
                warn = value.get('warn_threshold')
                critical = value.get('critical_threshold')
                warn_config = Warn_Config_Template(category=e.name, description=description,
                  db_type=db_type,
                  warn_threshold=warn,
                  critical_threshold=critical,
                  optional=value.get('optional', {}))
                global_warn_config_list.append(warn_config)
                global_warn_config_list_by_type[db_type].append(warn_config)

    Warn_Config_Template.objects.bulk_create(global_warn_config_list)
    warn_config_list = []
    for db in Database.objects.all():
        if global_warn_config_list_by_type.get(db.db_type):
            for warn in global_warn_config_list_by_type.get(db.db_type):
                warn_config = Warn_Config(category=warn.category, description=warn.description,
                  warn_threshold=warn.warn_threshold,
                  critical_threshold=warn.critical_threshold,
                  database=db,
                  template=warn,
                  status=warn.status,
                  optional=warn.optional)
                warn_config_list.append(warn_config)

    for host in Host.objects.all():
        for warn in global_warn_config_list_by_type.get('host', []):
            warn_config = Warn_Config(category=warn.category, description=warn.description,
              warn_threshold=warn.warn_threshold,
              critical_threshold=warn.critical_threshold,
              host=host,
              template=warn,
              status=warn.status,
              optional=warn.optional)
            warn_config_list.append(warn_config)

    Warn_Config.objects.bulk_create(warn_config_list)


def init_all():
    init_global_warnconfig()
    for db in Database.objects.all():
        sqlaudit_init(db)
# okay decompiling ./restful/hawkeye/api/v1/monitor/services/createdbService.pyc
