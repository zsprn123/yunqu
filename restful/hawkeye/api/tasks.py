# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/tasks.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 13063 bytes
from datetime import datetime, timedelta
import json
from celery import shared_task, Task
from celery.utils.log import get_task_logger
from channels import Group
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import transaction
from django.db.models import Q, Avg
from guardian.shortcuts import get_objects_for_user
from alarm.enum.alarm_warn_enum import WARN_ENUM
from alarm.models import Warn_Result, Warn_Config, Receiver
from api.celery.common.space import get_space
from api.celery.common.sql_detail import get_top_sql_detail
from api.celery.dashboard.activity import update_dashboard_data
from api.celery.db2.summary import get_dbsummary
from api.celery.oracle.sqlmon import get_sqlmon
from api.celery.oracle.warn import diskgroup_warn, oracle_standby_warn, plan_change_warn, object_change_warn, job_failure_warn
from api.celery.mysql.warn import mysql_standby_warn
from api.celery.sqlserver.perf_activity import get_sqlserver_activity
from api.db_tasks import get_performance, get_activity, get_lock_history
from api.v1.alarm.services.sendWarnService import send_warn_message_email
from api.v1.alarm.services.warnJudgerService import alarm_judger
from api.v1.sqlaudit.services.oracleAnalysisService import oracle_analysis, oracle_static_analysis
from api.v1.sqlaudit.services.db2AnalysisService import db2_analysis, db2_static_analysis
from api.v1.sqlaudit.services.sqlserverAnalysisService import sqlserver_analysis
from api.v1.monitor.services.schemaService import get_table_rows
from common.util import send_alarm
from monitor.models import Database, Performance
from sqlaudit.models import Audit_Job, Audit_Result
logger = get_task_logger(__name__)

class SingletonTask(Task):

    def __call__(self, *args, **kwargs):
        lock = cache.lock(self.name)
        if not (lock.acquire(blocking=False)):
            print(('{} failed to lock').format(self.name))
            return
        try:
            super(SingletonTask, self).__call__(*args, **kwargs)
        except Exception as e:
            raise e
        finally:
            lock.release()


@shared_task(bind=True, time_limit=settings.CELERY_TIME_LIMIT)
def performance(self):
    db_filter_set = Database.objects.all().filter((Q(disabled=False)) & (Q(is_switch_off=False)))
    for db in db_filter_set:
        try:
            get_performance(db)
        except Exception as e:
            logger.error(str(e))


@shared_task(bind=True, time_limit=settings.CELERY_TIME_LIMIT)
def activity(self):
    db_filter_set = Database.objects.all().filter((Q(disabled=False)) & (Q(is_switch_off=False))).exclude(db_type='sqlserver')
    for db in db_filter_set:
        try:
            get_activity(db)
        except Exception as e:
            logger.error(str(e))

    db_filter_set_sqlserver = Database.objects.all().filter((Q(disabled=False)) & (Q(is_switch_off=False))).filter(db_type='sqlserver')
    get_sqlserver_activity(db_filter_set_sqlserver)


@shared_task(bind=True, time_limit=settings.CELERY_TIME_LIMIT)
def lock_history(self):
    db_filter_set = Database.objects.all().filter((Q(disabled=False)) & (Q(is_switch_off=False)))
    for db in db_filter_set:
        try:
            get_lock_history(db)
        except Exception as e:
            logger.error(str(e))


@shared_task(bind=True, time_limit=settings.CELERY_TIME_LIMIT)
def table_rows(self):
    db_filter_set = Database.objects.all().filter((Q(disabled=False)) & (Q(is_switch_off=False)))
    for db in db_filter_set:
        try:
            get_table_rows(db)
        except Exception as e:
            logger.error(str(e))


@shared_task(bind=True, time_limit=settings.CELERY_TIME_LIMIT)
def dbsummary(self):
    db_filter_set = Database.objects.all().filter((Q(disabled=False)) & (Q(is_switch_off=False))).filter(db_type='db2')
    for db in db_filter_set:
        get_dbsummary(str(db.id))


@shared_task(bind=True, time_limit=settings.CELERY_TIME_LIMIT)
def sqlmon(self):
    db_filter_set = Database.objects.all().filter((Q(disabled=False)) & (Q(is_switch_off=False))).filter(db_type='oracle')
    for db in db_filter_set:
        if db.get_ora_version() > 10:
            if db.hist_sqlmon:
                try:
                    get_sqlmon(db)
                except Exception as e:
                    logger.error(str(e))


@shared_task(bind=True, time_limit=settings.CELERY_TIME_LIMIT)
def space(self):
    db_filter_set = Database.objects.all().filter((Q(disabled=False)) & (Q(is_switch_off=False)))
    for db in db_filter_set:
        try:
            get_space(db)
        except Exception as e:
            logger.error(str(e))

        if db.db_type == 'oracle':
            if db.instance_count > 1:
                try:
                    diskgroup_warn(db)
                except Exception as e:
                    logger.error(str(e))


@shared_task(bind=True, time_limit=settings.CELERY_TIME_LIMIT)
def top_sql_detail(self):
    db_filter_set = Database.objects.all().filter((Q(disabled=False)) & (Q(is_switch_off=False))).filter(Q(db_type='db2'))
    for db in db_filter_set:
        get_top_sql_detail(db)


@shared_task(bind=True, time_limit=settings.CELERY_TIME_LIMIT)
def standby(self):
    db_filter_set = Database.objects.all().filter((Q(disabled=False)) & (Q(is_switch_off=False)))
    for db in db_filter_set:
        if db.db_type == 'oracle':
            oracle_standby_warn(db)
        elif db.db_type == 'mysql':
            mysql_standby_warn(db)


@shared_task(bind=True, time_limit=settings.CELERY_TIME_LIMIT)
def plan_change(self):
    db_filter_set = Database.objects.all().filter((Q(disabled=False)) & (Q(is_switch_off=False))).filter(db_type='oracle')
    for db in db_filter_set:
        plan_change_warn(db)


@shared_task(bind=True, time_limit=settings.CELERY_TIME_LIMIT)
def object_change(self):
    db_filter_set = Database.objects.all().filter((Q(disabled=False)) & (Q(is_switch_off=False))).filter(db_type='oracle')
    for db in db_filter_set:
        object_change_warn(db)
        job_failure_warn(db)


@shared_task(bind=True, time_limit=settings.CELERY_TIME_LIMIT)
def send_warn_message(self):
    now = datetime.now()
    d1 = now - (timedelta(hours=1))
    warn_message = ''
    warn_result_list = Warn_Result.objects.filter((Q(send_status=None)) & (Q(created_at__gt=d1)))
    default_receiver = Receiver.objects.filter(is_default=True)
    warn_set = set(warn_result_list.values_list('warn', flat=True))
    for warn_config_id in warn_set:
        warn_config = Warn_Config.objects.get(pk=warn_config_id)
        receiver_list = default_receiver | warn_config.receivers.filter(~(Q(email=None)))
        email_list = set(receiver_list.values_list('email', flat=True))
        warn_message = (warn_result_list.filter(warn=warn_config)).values_list('warn_message', flat=True)
        warn_message = ('\n').join(warn_message)
        send_warn_message_email(email_list, warn_config.description, warn_message)
        ((Warn_Result.objects.filter(send_status=None)).filter(warn__id=str(warn_config_id))).update(send_status='success')


@shared_task(bind=True)
def sql_audit_analysis(self, arg):
    logger.error('sql_audit_analysis task is start')
    try:
        audit_job = Audit_Job.objects.get(pk=arg)
    except Exception as e:
        return

    if audit_job.status == 3:
        return
    audit_job.begin_time = datetime.now()
    audit_job.status = 2
    audit_job.save()
    database = audit_job.database
    logger.error('sql_audit_analysis task is start analysis')
    if not audit_job.is_static_job:
        if database.db_type == 'oracle':
            oracle_analysis(audit_job)
        elif database.db_type == 'db2':
            db2_analysis(audit_job)
        else:
            if database.db_type == 'sqlserver':
                sqlserver_analysis(audit_job)
            else:
                if database.db_type == 'oracle':
                    oracle_static_analysis(audit_job)
                else:
                    if database.db_type == 'db2':
                        db2_static_analysis(audit_job)
                logger.error('sql_audit_analysis task is finish analysis')
                audit_job.finish_at = datetime.now()
                audit_job.status = 3
                task = audit_job.task
                task.enabled = False
                task.save()
                audit_job.total_score = calculate_report_score(Audit_Result.objects.filter(job=audit_job))
                audit_job.save()


def calculate_report_score(queryset):
    score_weight_set = queryset.values_list('score', 'rule_weight')
    if not score_weight_set:
        return 0
    else:
        score_sum = 0
        weight_sum = 0
        for score_weight in score_weight_set:
            score_sum += score_weight[0] * score_weight[1]
            weight_sum += score_weight[1]

        return round(score_sum / weight_sum, 2)


@shared_task(bind=True, time_limit=settings.CELERY_TIME_LIMIT)
def now(self):
    """Return the current time and date as a datetime."""
    from datetime import datetime
    print(datetime.now())
    return datetime.now()


@shared_task(bind=True)
def check_database_alive(self):
    disabled_database_list = []
    for database in Database.objects.exclude(is_switch_off=True):
        if not database.is_alive():
            if not database.disabled:
                database.disabled = True
                if not database._state.adding:
                    database.save()
                warn = WARN_ENUM.get(database.db_type).Database_Access_Warn
                warn_level, warn_config = alarm_judger(database, warn.name,
                  None, data=1)
                options = {'warn_level':warn_level, 
                 'created_at':datetime.now().replace(microsecond=0), 
                 'alias':database.alias}
                warn_message = warn.value.get('message_template').format(**options)
                warn_result = Warn_Result(database=database, warn_message=warn_message, warn=warn_config)
                warn_result.save()
                warn_alert = {'warn_message':warn_message, 
                 'link':{}}
                send_alarm(database.id, json.dumps(warn_alert))
            else:
                if database.disabled:
                    database.disabled = False
                    database.save()


@shared_task(bind=True, time_limit=settings.CELERY_TIME_LIMIT)
def update_index_data(self):
    user_list = get_user_model().objects.all()
    for user in user_list:
        database_list = (get_objects_for_user(user, 'monitor.view_database').exclude(is_switch_off=True)).exclude(disabled=True)
        text2 = update_dashboard_data(database_list)
        Group('index-' + str(user.id)).send({'text': json.dumps(text2)}, immediately=True)


@shared_task(bind=True, time_limit=settings.CELERY_TIME_LIMIT)
def clean_history_data(self):
    logger.error('start clean history performance data')
    for db in Database.objects.all():
        begin_date = db.last_archived_date if db.last_archived_date else datetime.fromtimestamp(0)
        end_date = datetime.today() - (timedelta(days=db.retention_days))
        performance_minute_list = ((Performance.objects.filter(database=db)).filter(created_at__range=(
         begin_date, end_date))).datetimes('created_at', 'minute')
        for idx, _time in enumerate(performance_minute_list):
            performance_query_list = ((Performance.objects.filter(database=db)).filter(created_at__range=(
             _time, _time + (timedelta(minutes=1))))).values('inst_id', 'database_id', 'name').annotate(Avg('value'))
            performance_bulk_save_list = []
            for performance in performance_query_list:
                performance['value'] = performance['value__avg']
                performance.pop('value__avg')
                performance_bulk_save_list.append(Performance(created_at=_time, **performance))

            ((Performance.objects.filter(database=db)).filter(created_at__range=(
             _time, _time + (timedelta(minutes=1))))).delete()
            Performance.objects.bulk_create(performance_bulk_save_list)

        db.last_archived_date = end_date
        db.save()

    from django.db import connection
    cursor = connection.cursor()
    cursor.execute('VACUUM')
# okay decompiling ./restful/hawkeye/api/tasks.pyc
