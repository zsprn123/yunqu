# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/monitor/services/backupService.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 3143 bytes
from api.v1.monitor.services.runsqlService import run_batch_sql
from common.util import build_exception_from_java
from monitor.models import Database
from django.core.exceptions import ObjectDoesNotExist

def get_backup(pk):
    days = 7
    query = {'config':'select * from v$rman_configuration', 
     'history':f'''select
  j.session_recid, --j.session_stamp,
  to_char(j.start_time, 'yyyy-mm-dd hh24:mi:ss') start_time,
  to_char(j.end_time, 'yyyy-mm-dd hh24:mi:ss') end_time,
  round((j.output_bytes/1024/1024),2) output_mbytes, j.status, j.input_type,
  decode(to_char(j.start_time, 'd'), 1, 'Sunday', 2, 'Monday',
                                     3, 'Tuesday', 4, 'Wednesday',
                                     5, 'Thursday', 6, 'Friday',
                                     7, 'Saturday') WEEK,
  round(j.elapsed_seconds,-1) ELAPSED_TIME_SEC, j.TIME_TAKEN_DISPLAY,
  x.cf, x.df, x.i0, x.i1, x.l,
  ro.inst_id output_instance,x.device_type
from V$RMAN_BACKUP_JOB_DETAILS j
  left outer join (select
                     d.session_recid, d.session_stamp,
                     sum(case when d.controlfile_included = 'YES' then d.pieces else 0 end) CF,
                     sum(case when d.controlfile_included = 'NO'
                               and d.backup_type||d.incremental_level = 'D' then d.pieces else 0 end) DF,
                     sum(case when d.backup_type||d.incremental_level = 'D0' then d.pieces else 0 end) I0,
                     sum(case when d.backup_type||d.incremental_level = 'I1' then d.pieces else 0 end) I1,
                     sum(case when d.backup_type = 'L' then d.pieces else 0 end) L,d.device_type
                   from
                     V$BACKUP_SET_DETAILS d
                     join V$BACKUP_SET s on s.set_stamp = d.set_stamp and s.set_count = d.set_count
                   where s.input_file_scan_only = 'NO'
                   group by d.session_recid, d.session_stamp,d.device_type) x
    on x.session_recid = j.session_recid and x.session_stamp = j.session_stamp
  left outer join (select o.session_recid, o.session_stamp, min(inst_id) inst_id
                   from GV$RMAN_OUTPUT o
                   group by o.session_recid, o.session_stamp)
    ro on ro.session_recid = j.session_recid and ro.session_stamp = j.session_stamp
where j.start_time > trunc(sysdate)-{days}
order by j.start_time''',  'long':'select sid || \',\'|| serial# || \'@\' || inst_id as SESSION_ID,to_char(start_time, \'yyyy-mm-dd hh24:mi:ss\') start_time,ELAPSED_SECONDS,sofar,totalwork,\nopname,           round(sofar/totalwork*100,-1) "PCT"\n           from gv$session_longops\n            where opname like \'RMAN:%\'\n           and opname not like \'RMAN: aggregate%\'\n           and totalwork!=0'}
    try:
        database = Database.objects.get(pk=pk)
        flag, json_data = run_batch_sql(database, query)
        if not flag:
            raise build_exception_from_java(json_data)
        else:
            return json_data
    except ObjectDoesNotExist:
        return {'error_message': ''}
    except Exception as err:
        return {'error_message': str(err)}
# okay decompiling ./restful/hawkeye/api/v1/monitor/services/backupService.pyc
