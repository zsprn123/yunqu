# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./housekeep_hawkeye.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 3005 bytes
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hawkeye.settings.prod')
import django
django.setup()
import sys
from django.db import connection
from datetime import timedelta, datetime
batch_size = 10000
HAWKEYE_BACKUP_PATH = os.environ.get('HAWKEYE_BACKUP_PATH', None)
PGPASSWORD = os.environ.get('PGPASSWORD', 'yunqu')

def delete_performance(retention_days):
    retention_datetime = datetime.today() + timedelta(-retention_days)
    retention_date = retention_datetime.strftime('%Y-%m-%d %H:%M:%S')
    deleted_row_count = 0
    try:
        with connection.cursor() as (cursor):
            print('Analyzing the row count to be archived')
            sys.stdout.flush()
            cursor.execute('select id from monitor_database')
            database_list = cursor.fetchall()
            database_list_str = (',').join([("'{}'").format(x[0]) for x in database_list])
            cursor.execute(f'''select count(*) from monitor_performance WHERE database_id in ({database_list_str}) and created_at <= '{retention_date}'''')
            count = cursor.fetchall()[0][0] or 0
            print('Number of rows to be deleted:' + str(count))
            if count > 0:
                if type(HAWKEYE_BACKUP_PATH) == str and os.path.isdir(HAWKEYE_BACKUP_PATH):
                    print('Start backuping the archived records')
                    backup_file_name = f'''{HAWKEYE_BACKUP_PATH}/hawkeye_performance_backup_{(retention_datetime.strftime('%Y-%m-%d_%H-%M-%S'))}.csv.gz'''
                    command = f'''PGPASSWORD={PGPASSWORD} psql -h 127.0.0.1 -U yunqu hawkeye -c "COPY (select * from monitor_performance WHERE database_id in ({database_list_str}) and created_at <= '{retention_date}') TO stdout DELIMITER ',' CSV HEADER" | gzip > {backup_file_name}'''
                    print(command)
                    os.system(command)
                    print('Backup completed')
                i = count / batch_size + 1
                _i = i
                while i > 0:
                    cursor.execute(f'''delete from monitor_performance WHERE id in
                                (select id from monitor_performance WHERE database_id in ({database_list_str}) and created_at <= '{retention_date}' limit {batch_size})''')
                    deleted_row_count = deleted_row_count + cursor.rowcount
                    cursor.execute('COMMIT')
                    i = i - 1
                    pct = round((_i - i) / _i * 100, 1) if i > 0 else 100
                    print(f'''Number of records deleted: {deleted_row_count},  Percent: {pct}%''')

            sys.stdout.flush()
            print('Reclaiming the space')
            cursor.execute('VACUUM')
        print('Finish the archive job')
    except Exception as e:
        print('Exception: ' + str(e))


if len(sys.argv) == 2:
    if isinstance(int(sys.argv[1]), int):
        delete_performance(int(sys.argv[1]))
    print('Usage: %s <int>' % sys.argv[0])
    sys.exit(1)
# okay decompiling ./restful/hawkeye/housekeep_hawkeye.pyc
