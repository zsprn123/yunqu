# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./sqlaudit/models.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 7425 bytes
from django.db import models
from common.aes import aes_decode
from common.models import CoreModel
from django.contrib.postgres.fields import JSONField
from django.contrib.auth import get_user_model

class Audit_Job(CoreModel):
    name = models.CharField(max_length=100, null=True)
    database = models.ForeignKey('monitor.Database', blank=True, null=True, on_delete=models.CASCADE)
    strategy = JSONField(null=True, blank=True, default={})
    schema = models.CharField(max_length=5000, null=True, blank=True)
    plan_time = models.DateTimeField(null=True)
    begin_time = models.DateTimeField(null=True)
    finish_at = models.DateTimeField(null=True)
    time_span = models.BooleanField(default=True)
    snapshot_begin_time = models.DateTimeField(null=True)
    snapshot_end_time = models.DateTimeField(null=True)
    compare_audit = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    timeout = models.IntegerField(null=True)
    max_rows = models.IntegerField(null=True)
    order_by = models.CharField(max_length=100, null=True, blank=True)
    total_score = models.FloatField(null=True, blank=True)
    status = models.IntegerField(default=1)
    task = models.ForeignKey('django_celery_beat.PeriodicTask', blank=True, null=True, on_delete=models.CASCADE)
    is_static_job = models.BooleanField(default=False)


class Audit_Result(CoreModel):
    audit_type = models.CharField(max_length=100, null=True)
    target = models.CharField(max_length=100, null=True)
    rule_weight = models.IntegerField(null=True, default=4)
    name = models.CharField(max_length=100, null=True)
    score = models.FloatField(null=True, blank=True)
    problem = models.IntegerField(null=True)
    total = models.IntegerField(null=True)
    problem_rate = models.FloatField(null=True, blank=True)
    result = JSONField(null=True, blank=True, default={})
    job = models.ForeignKey('Audit_Job', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        index_together = [
         'job']


class Audit_SQL_Text(CoreModel):
    sql_id = models.CharField(max_length=100, null=True)
    sql_text = models.TextField(max_length=3000000, null=True)
    force_matching_signature = models.CharField(max_length=100, null=True)
    job = models.ForeignKey('Audit_Job', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        index_together = [
         'job', 'force_matching_signature']
        index_together = ['sql_id']
        index_together = ['force_matching_signature']


class Audit_SQL_Result(CoreModel):
    sql_id = models.CharField(max_length=100, null=True)
    detail = JSONField(null=True, blank=True, default={})
    job = models.ForeignKey('Audit_Job', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        index_together = [
         'job']


class Optimization_Job(CoreModel):
    name = models.CharField(max_length=100, null=True)
    status = models.IntegerField(null=True, default=1)
    schema = models.CharField(max_length=5000, null=True, blank=True)
    database = models.ForeignKey('monitor.Database', blank=True, null=True, on_delete=models.CASCADE)
    strategy = JSONField(null=True, blank=True, default={})
    deadline = models.DateTimeField(null=True)
    closed_at = models.DateTimeField(null=True)
    optimize_description = models.CharField(max_length=5000, null=True, blank=True)
    audit_job = models.ForeignKey('Audit_Job', blank=True, null=True, on_delete=models.CASCADE)
    target = models.CharField(max_length=100, null=True)
    detail_name = models.CharField(max_length=1000, null=True, blank=True)
    detail_id = models.CharField(max_length=1000, null=True, blank=True)
    optimized_detail_id = models.CharField(max_length=1000, null=True, blank=True)
    optimized_detail_name = models.CharField(max_length=1000, null=True, blank=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)


class Audit_Strategy(CoreModel):
    """
     Audit_Rule audit_type  target  Model
    """
    audit_type = models.CharField(max_length=100, null=True)
    target = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=100, null=True)
    enabled = models.BooleanField(default=True)
    remarks = models.CharField(max_length=1000, null=True)
    database = models.ForeignKey('monitor.Database', blank=True, null=True, on_delete=models.CASCADE)
    is_static_rule = models.CharField(max_length=100, null=True)

    class Meta:
        index_together = [
         'database']


class Audit_Rule(models.Model):
    """
     rule
    """
    audit_type = models.CharField(max_length=100, null=True)
    target = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=100, null=True)
    predicate = models.CharField(max_length=1000, null=True)
    predicate_template = models.CharField(max_length=1000, null=True, default=None)
    template = models.CharField(max_length=1000, null=True)
    weight = models.IntegerField(null=True, default=4)
    risky = models.CharField(max_length=1000, null=True, default='')
    enabled = models.BooleanField(default=True)
    single = models.BooleanField(default=True)
    modifiable = models.BooleanField(default=False)
    remarks = models.CharField(max_length=1000, null=True)
    is_static_rule = models.BooleanField(default=False)
    database = models.ForeignKey('monitor.Database', blank=True, null=True, on_delete=models.CASCADE)
    audit_strategy = models.ForeignKey('Audit_Strategy', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        index_together = [
         'database']


class Audit_Static_Content(CoreModel):
    content = models.TextField(max_length=1000000000, null=True)
    job = models.ForeignKey('Audit_Job', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        index_together = [
         'job']


class Audit_Schema(CoreModel):
    username = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=100, null=True)
    database = models.ForeignKey('monitor.Database', blank=True, null=True, on_delete=models.CASCADE)

    def get_password(self):
        return aes_decode(self.password)


class SQL_Perf_Diff(CoreModel):
    name = models.CharField(max_length=10000000, null=True)
    sql_id_list = models.CharField(max_length=10000000, null=True)
    database = models.ForeignKey('monitor.Database', blank=True, null=True, on_delete=models.CASCADE)
    snapshot_begin_time = models.DateTimeField(null=True)
    snapshot_end_time = models.DateTimeField(null=True)
    begin_result = JSONField(null=True, blank=True, default={})
    end_result = JSONField(null=True, blank=True, default={})
    summary_result = JSONField(null=True, blank=True, default={})
# okay decompiling ./restful/hawkeye/sqlaudit/models.pyc
