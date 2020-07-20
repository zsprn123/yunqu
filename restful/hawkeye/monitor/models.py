# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./monitor/models.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 23181 bytes
from django.db import models
from alarm.models import Warn_Result
from api.enum.database_enum import Driver
from api.v1.alarm.services.warnService import performance_warn_scanner
from authx.models import User
from common.models import CoreModel, PerformanceModel
from common.aes import aes_decode
import re
from django.db.models import signals
from django.contrib.postgres.fields import JSONField
from common.util import get_java_response, get_performance_name_id

class Database(CoreModel):
    db_name = models.CharField(max_length=100, null=True, blank=True)
    db_type = models.CharField(max_length=100, null=True)
    username = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=100, null=True)
    hostname = models.CharField(max_length=100, null=True)
    port = models.IntegerField(null=True)
    alias = models.CharField(max_length=100, default='', null=True)
    encoding = models.CharField(max_length=1000, default='', null=True, blank=True)
    role = models.CharField(max_length=100, default='PRIMARY')
    version = models.CharField(max_length=320, blank=True, null=True)
    disabled = models.BooleanField(default=False)
    is_switch_off = models.BooleanField(default=False)
    retention_days = models.IntegerField(default=30)
    last_archived_date = models.DateField(null=True)
    num_sqlmon_per_minute = models.IntegerField(default=10, null=True)
    instance_list = models.CharField(max_length=1000, default='1')
    instance_id_list = models.CharField(max_length=1000, default='1')
    instance_count = models.IntegerField(default=1)
    sqlmon_format = models.CharField(max_length=100, default='HTML')
    dg_stats = models.BooleanField(default=False)
    hist_sqlmon = models.BooleanField(default=False)
    main_db = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    def get_password(self):
        return aes_decode(self.password)

    def get_encoding(self):
        if self.db_type == 'informix':
            return self.encoding
        else:
            if self.db_type == 'mysql':
                if self.encoding:
                    return '?' + self.encoding
            return ''

    def is_v95_base(self):
        return float(self.version[:3]) < 9.7

    def is_v97(self):
        return re.search(re.compile('9.7'), self.version)

    def get_ora_version(self):
        return int(self.version)

    def is_alive(self):
        url = type2jdbcurl(self.db_type, self.hostname, self.port, db_name=self.db_name)
        jsonobj = {'user':self.username, 
         'password':aes_decode(self.password), 
         'jdbc_url':url, 
         'driver':Driver[self.db_type].value}
        r = get_java_response('test-conn/', jsonobj)
        result = r.json()
        if result.get('message') == True:
            return True
        else:
            r = get_java_response('test-conn/', jsonobj)
            result = r.json()
            if result.get('message') == True:
                return True
            return False
            return False

    def jdbc_url(self, encoding=''):
        _type, host, port, database_name, encoding = (self.db_type, self.hostname, self.port, self.db_name, encoding)
        if _type == 'mysql':
            return 'jdbc:mysql://%s:%s/%s%s' % (host, port, database_name, encoding)
        elif _type == 'oracle':
            return 'jdbc:oracle:thin:@%s:%s/%s' % (host, port, database_name)
        elif _type == 'db2':
            return 'jdbc:db2://%s:%s/%s' % (host, port, database_name)
        elif _type == 'informix':
            return 'jdbc:informix-sqli://%s:%s/%s:%s' % (host, port, database_name, encoding)
        elif _type == 'postgres':
            return 'jdbc:postgresql://%s:%s/%s' % (host, port, database_name)
        elif _type == 'sqlserver':
            return 'jdbc:sqlserver://%s:%s;databaseName=%s' % (host, port, database_name)
        else:
            return ''

    def subordinate_ids(self):
        subordinate_ids = Database.objects.only('id').filter(main_db=self.id)
        return subordinate_ids

    def __str__(self):
        return self.alias

    class Meta:
        unique_together = ('hostname', 'db_name', 'port', 'username')
        permissions = (('view_database', 'Can view database'), )


def type2jdbcurl(_type, host, port, db_name='', encoding=''):
    if _type == 'mysql':
        return 'jdbc:mysql://%s:%s/' % (host, port)
    elif _type == 'oracle':
        return 'jdbc:oracle:thin:@%s:%s/%s' % (host, port, db_name)
    elif _type == 'db2':
        return 'jdbc:db2://%s:%s/%s' % (host, port, db_name)
    elif _type == 'informix':
        return 'jdbc:informix-sqli://%s:%s/:%s' % (host, port, encoding)
    elif _type == 'postgres':
        return 'jdbc:postgresql://%s:%s/' % (host, port)
    elif _type == 'sqlserver':
        return 'jdbc:sqlserver://%s:%s;' % (host, port)
    else:
        return ''


class ASH(PerformanceModel):
    database = models.ForeignKey(Database, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created_at', )
        abstract = True


class Performance(PerformanceModel):
    inst_id = models.IntegerField(null=True, blank=True)
    name_id = models.IntegerField(null=True, blank=True)
    value = models.FloatField()
    database = models.ForeignKey(Database, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        name = self.name
        if isinstance(name, str):
            name_id = get_performance_name_id(name.upper().strip())
            if name_id:
                self.name_id = name_id
            else:
                return
            self.name = None
        else:
            return
        super(Performance, self).save(*args, **kwargs)

    class Meta:
        index_together = [
         'database', 'name_id', 'created_at']


class DB_ASH(ASH):
    session_id = models.CharField(max_length=100, null=True)
    sql_elapsed_time = models.BigIntegerField(null=True)
    username = models.CharField(max_length=100, null=True)
    machine = models.CharField(max_length=100, null=True)
    program = models.CharField(max_length=100, null=True)
    command = models.CharField(max_length=100, null=True)
    sql_id = models.CharField(max_length=100, null=True)
    sql_text = models.TextField(max_length=100000, null=True)
    db_name = models.CharField(max_length=100, null=True)

    class Meta:
        index_together = [
         [
          'database', 'created_at'],
         [
          'sql_id', 'created_at'],
         [
          'session_id', 'created_at']]
        ordering = ('-created_at', )
        abstract = True


class Oracle_ASH(DB_ASH):
    inst_id = models.IntegerField(null=True)
    sid = models.IntegerField(null=True)
    serial = models.IntegerField(null=True)
    status = models.CharField(max_length=100, null=True)
    sql_hash_value = models.BigIntegerField(null=True)
    sql_plan_hash_value = models.BigIntegerField(null=True)
    event = models.CharField(max_length=100, default='f', null=True)
    p1 = models.BigIntegerField(null=True)
    p2 = models.BigIntegerField(null=True)
    p3 = models.BigIntegerField(null=True)
    wait_class = models.CharField(max_length=100, null=True)
    module = models.CharField(max_length=1000, null=True)
    action = models.CharField(max_length=1000, null=True)
    service_name = models.CharField(max_length=1000, null=True)
    plsql_object_name = models.CharField(max_length=1000, null=True)
    plsql_entry_object_name = models.CharField(max_length=1000, null=True)
    blocking_session = models.IntegerField(null=True)
    blocking_session_serial = models.IntegerField(null=True)
    sql_plan_line_id = models.IntegerField(null=True)
    sql_plan_operation = models.CharField(max_length=200, null=True)
    session_type = models.CharField(max_length=128, null=True)


class DB2_Summary(ASH):
    summary = models.TextField(max_length=10000000, null=True)

    class Meta:
        index_together = [
         [
          'database', 'created_at']]


class SQL_Detail(ASH):
    sql_id = models.CharField(max_length=1000, null=True)
    sql_detail = JSONField(null=True, blank=True, default={})

    class Meta:
        index_together = [
         [
          'database', 'created_at'],
         [
          'database', 'sql_id']]


class DB2_ASH(DB_ASH):
    appl_status = models.CharField(max_length=100, null=True)
    activity_state = models.CharField(max_length=100, null=True)
    total_cpu_time = models.BigIntegerField(null=True)
    rows_read = models.BigIntegerField(null=True)
    rows_returned = models.BigIntegerField(null=True)
    query_cost_estimate = models.BigIntegerField(null=True)
    direct_reads = models.BigIntegerField(null=True)
    direct_writes = models.BigIntegerField(null=True)


class MSSQL_ASH(DB_ASH):
    start_time = models.DateTimeField(null=True)
    status = models.CharField(max_length=30, null=True)
    b_blocker = models.IntegerField(null=True)
    wait_type = models.CharField(max_length=60, null=True)
    wait_time = models.IntegerField(null=True)
    wait_resource = models.CharField(max_length=256, null=True)
    total_elapsed_time = models.IntegerField(null=True)
    row_count = models.BigIntegerField(null=True)
    client_net_address = models.CharField(max_length=128, null=True)
    linked_ip = models.CharField(max_length=128, null=True)
    linked_spid = models.BigIntegerField(null=True)

    class Meta:
        index_together = [
         [
          'linked_ip', 'linked_spid']]


class MySQL_ASH(DB_ASH):
    state = models.CharField(max_length=100, null=True)
    wait_class = models.CharField(max_length=100, default='Others')


class Postgres_ASH(ASH):
    pid = models.IntegerField(null=True)
    user = models.CharField(max_length=100, null=True)
    host = models.CharField(max_length=100, null=True)
    port = models.IntegerField(null=True)
    db = models.CharField(max_length=100, null=True)
    waiting = models.CharField(max_length=100, default='f', null=True)
    query = models.TextField(max_length=100000, null=True)

    class Meta:
        index_together = [
         [
          'database', 'created_at'],
         [
          'pid', 'created_at'],
         [
          'query', 'created_at']]


class Oracle_Lock_History(ASH):
    b_res = models.CharField(max_length=100, blank=True, null=True)
    b_blocker = models.CharField(max_length=100, blank=True, null=True)
    b_blocked_cnt = models.IntegerField(null=True)
    b_request = models.IntegerField(null=True)
    b_lmode = models.IntegerField(null=True)
    b_username = models.CharField(max_length=100, blank=True, null=True)
    b_sql_id = models.CharField(max_length=100, blank=True, null=True)
    b_sqltext = models.TextField(max_length=100000, null=True)
    b_prev_sql_id = models.CharField(max_length=100, blank=True, null=True)
    b_prev_sqltext = models.TextField(max_length=100000, null=True)
    b_ctime = models.IntegerField(null=True)
    w_waiter = models.CharField(max_length=100, blank=True, null=True)
    w_request = models.IntegerField(null=True)
    w_lmode = models.IntegerField(null=True)
    w_username = models.CharField(max_length=100, blank=True, null=True)
    w_sql_id = models.CharField(max_length=100, blank=True, null=True)
    w_sqltext = models.TextField(max_length=100000, null=True)
    w_prev_sql_id = models.CharField(max_length=100, blank=True, null=True)
    w_prev_sqltext = models.TextField(max_length=100000, null=True)
    w_ctime = models.IntegerField(null=True)

    class Meta:
        index_together = [
         'database', 'created_at']


class MySQL_Lock_History(ASH):
    b_res = models.CharField(max_length=100, blank=True, null=True)
    w_trx_id = models.CharField(max_length=100, blank=True, null=True)
    w_waiter = models.CharField(max_length=100, blank=True, null=True)
    w_wait_time = models.IntegerField(null=True)
    w_waiting_query = models.CharField(max_length=4000, blank=True, null=True)
    w_waiting_table_lock = models.CharField(max_length=100, blank=True, null=True)
    b_trx_id = models.CharField(max_length=100, blank=True, null=True)
    b_blocker = models.CharField(max_length=100, blank=True, null=True)
    b_host = models.CharField(max_length=100, blank=True, null=True)
    b_port = models.CharField(max_length=100, blank=True, null=True)
    b_idle_in_trx = models.IntegerField(null=True)
    b_trx_query = models.CharField(max_length=4000, blank=True, null=True)

    class Meta:
        index_together = [
         'database', 'created_at']


class MSSQL_Lock_History(ASH):
    b_blocker = models.CharField(max_length=100, blank=True, null=True)
    b_login_name = models.CharField(max_length=1000, null=True)
    b_status = models.CharField(max_length=1000, null=True)
    b_text = models.TextField(max_length=100000, null=True)
    b_sql_handle = models.CharField(max_length=1000, null=True)
    w_waiter = models.CharField(max_length=100, blank=True, null=True)
    w_login_name = models.CharField(max_length=1000, null=True)
    w_status = models.CharField(max_length=1000, null=True)
    w_waitduration = models.IntegerField()
    w_waittype = models.CharField(max_length=1000, null=True)
    w_waitrequestmode = models.CharField(max_length=1000, null=True)
    b_res = models.CharField(max_length=1000, null=True)
    w_waitresourcetype = models.CharField(max_length=1000, null=True)
    w_waitresourcedatabasename = models.CharField(max_length=1000, null=True)
    w_text = models.TextField(max_length=100000, null=True)
    w_sql_handle = models.CharField(max_length=1000, null=True)

    class Meta:
        index_together = [
         'database', 'created_at']


class DB2_Lock_History(ASH):
    b_res = models.CharField(max_length=1000, null=True)
    lock_object_type = models.CharField(max_length=1000, null=True)
    lock_wait_elapsed_time = models.IntegerField(null=True)
    tabschema = models.CharField(max_length=1000, null=True)
    tabname = models.CharField(max_length=1000, null=True)
    data_partition_id = models.IntegerField(null=True)
    lock_mode = models.CharField(max_length=1000, null=True)
    lock_current_mode = models.CharField(max_length=1000, null=True)
    lock_mode_requested = models.CharField(max_length=1000, null=True)
    w_waiter = models.CharField(max_length=1000, null=True)
    req_agent_tid = models.IntegerField(null=True)
    req_member = models.IntegerField(null=True)
    req_application_name = models.CharField(max_length=1000, null=True)
    req_userid = models.CharField(max_length=1000, null=True)
    req_executable_id = models.CharField(max_length=100, null=True)
    req_stmt_text = models.TextField(max_length=100000, null=True)
    hld_application_handle = models.IntegerField(null=True)
    hld_member = models.IntegerField(null=True)
    b_blocker = models.CharField(max_length=1000, null=True)
    hld_userid = models.CharField(max_length=1000, null=True)
    hld_current_stmt_text = models.TextField(max_length=100000, null=True)
    hld_executable_id = models.CharField(max_length=100, null=True)

    class Meta:
        index_together = [
         'database', 'created_at']


class Transaction(ASH):
    transactions = JSONField(null=True, blank=True, default={})

    class Meta:
        index_together = [
         'database', 'created_at']


class Session(ASH):
    session_id = models.CharField(max_length=100, null=True)
    detail = JSONField(null=True, blank=True, default={})

    class Meta:
        index_together = [
         'database', 'created_at']


class SQLMON(ASH):
    status = models.CharField(max_length=100, null=True)
    sql_id = models.CharField(max_length=100, null=True)
    elapsed_time = models.BigIntegerField(null=True)
    db_time = models.BigIntegerField(null=True)
    db_cpu = models.BigIntegerField(null=True)
    sql_exec_id = models.BigIntegerField(null=True)
    sql_exec_start = models.CharField(max_length=100, null=True)
    sql_plan_hash_value = models.BigIntegerField(null=True)
    inst_id = models.IntegerField(null=True)
    username = models.CharField(max_length=100, null=True)
    sql_text = models.TextField(max_length=100000, null=True)
    sqlmon = models.TextField(max_length=100000, null=True)

    class Meta:
        index_together = [
         [
          'database', 'created_at'],
         [
          'database', 'sql_id', 'sql_exec_id']]


class Oracle_SQL(ASH):
    inst_id = models.IntegerField(null=True)
    sql_id = models.CharField(max_length=100, null=True)
    plan_hash_value = models.IntegerField(null=True)
    optimizer_cost = models.IntegerField(null=True)
    optimizer_mode = models.CharField(max_length=100, null=True)
    module = models.CharField(max_length=100, null=True)
    action = models.CharField(max_length=100, null=True)
    sql_profile = models.CharField(max_length=100, null=True)
    force_matching_signature = models.IntegerField(null=True)
    parsing_schema_name = models.CharField(max_length=100, null=True)
    fetches_delta = models.IntegerField(null=True)
    end_of_fetch_count_delta = models.IntegerField(null=True)
    sorts_delta = models.IntegerField(null=True)
    executions_delta = models.IntegerField(null=True)
    px_servers_execs_delta = models.IntegerField(null=True)
    disk_reads_delta = models.IntegerField(null=True)
    buffer_gets_delta = models.IntegerField(null=True)
    rows_processed_delta = models.IntegerField(null=True)
    cpu_time_delta = models.IntegerField(null=True)
    elapsed_time_delta = models.IntegerField(null=True)

    class Meta:
        index_together = [
         [
          'database', 'created_at'],
         [
          'database', 'sql_id']]


class Oracle_SQL_Plan(ASH):
    inst_id = models.IntegerField(null=True)
    sql_id = models.CharField(max_length=100, null=True)
    plan_hash_value = models.IntegerField(null=True)
    operation = models.CharField(max_length=100, null=True)
    options = models.CharField(max_length=100, null=True)
    object_owner = models.CharField(max_length=100, null=True)
    object_name = models.CharField(max_length=100, null=True)
    object_type = models.CharField(max_length=100, null=True)
    plan_line_id = models.IntegerField(null=True)
    parent_id = models.IntegerField(null=True)
    depth = models.IntegerField(null=True)
    position = models.IntegerField(null=True)
    cost = models.IntegerField(null=True)
    cardinality = models.IntegerField(null=True)
    partition_id = models.IntegerField(null=True)
    access_predicates = models.CharField(max_length=100, null=True)
    filter_predicates = models.CharField(max_length=100, null=True)

    class Meta:
        index_together = [
         [
          'database', 'created_at'],
         [
          'database', 'sql_id']]


class SQLMON_Plan(ASH):
    inst_id = models.IntegerField(null=True)
    status = models.CharField(max_length=100, null=True)
    first_refresh_time = models.CharField(max_length=100, null=True)
    last_refresh_time = models.CharField(max_length=100, null=True)
    sid = models.IntegerField(null=True)
    sql_id = models.CharField(max_length=100, null=True)
    sql_exec_start = models.CharField(max_length=100, null=True)
    sql_exec_id = models.BigIntegerField(null=True)
    sql_plan_hash_value = models.BigIntegerField(null=True)
    plan_parent_id = models.IntegerField(null=True)
    plan_line_id = models.IntegerField(null=True)
    plan_operation = models.CharField(max_length=100, null=True)
    plan_options = models.CharField(max_length=100, null=True)
    plan_object_owner = models.CharField(max_length=100, null=True)
    plan_object_name = models.CharField(max_length=100, null=True)
    plan_object_type = models.CharField(max_length=100, null=True)
    plan_depth = models.IntegerField(null=True)
    plan_position = models.IntegerField(null=True)
    plan_cost = models.BigIntegerField(null=True)
    plan_cardinality = models.BigIntegerField(null=True)
    plan_temp_space = models.BigIntegerField(null=True)
    starts = models.BigIntegerField(null=True)
    output_rows = models.BigIntegerField(null=True)
    physical_read_requests = models.BigIntegerField(null=True)
    physical_read_bytes = models.BigIntegerField(null=True)
    physical_write_requests = models.BigIntegerField(null=True)
    physical_write_bytes = models.BigIntegerField(null=True)

    class Meta:
        index_together = [
         [
          'database', 'created_at'],
         [
          'database', 'sql_id', 'sql_exec_id']]


class Space(ASH):
    name = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=100, null=True)
    total_mb = models.FloatField(null=True)
    free = models.FloatField(null=True)
    used = models.FloatField(null=True)
    used_pct = models.FloatField(null=True, blank=True)

    class Meta:
        index_together = [
         [
          'database', 'created_at']]


class Space_Detail(ASH):
    detail = JSONField(null=True, blank=True, default={})

    class Meta:
        index_together = [
         [
          'database', 'created_at']]


class DB_SCHEMA(ASH):
    detail = JSONField(null=True, blank=True, default={})


class Table_Rows(PerformanceModel):
    owner = models.CharField(max_length=100, blank=True, null=True)
    table_name = models.CharField(max_length=100, blank=True, null=True)
    rows = models.IntegerField(blank=True, null=True)
    database = models.ForeignKey(Database, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        index_together = [
         [
          'database', 'owner', 'table_name'],
         [
          'database', 'created_at']]


signals.pre_save.connect(performance_warn_scanner, sender=Performance)
# okay decompiling ./restful/hawkeye/monitor/models.pyc
