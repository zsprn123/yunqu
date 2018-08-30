# hawkeye-v2

clone 代码之后, 如何把 quicksilver 跑起来

## 1. 前端

```
brew install node 8
cd fed
npm i
npm run dev
```

## 2 ORM 数据库

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "hawkeye",
        'USER': "yunqu",
        'PASSWORD': "yunqu",
        'HOST': "127.0.0.1",
        },
    }

su - postgres -c psql << EOF
CREATE ROLE yunqu LOGIN password 'yunqu';
CREATE DATABASE hawkeye ENCODING 'UTF8' OWNER yunqu;
EOF
```

## 3 redis

注意事项:
需要本机 redis, 密码和鹰眼一样

## 4 django

```
cd rest/hawkdyd

pip install -r requirements.txt

python ./manage.py migrate --settings=hawkeye.settings.default

python ./manage.py createsuperuser --settings=hawkeye.settings.default

python ./manage.py runserver --settings=hawkeye.settings.default
```

## 5 Celery

cd 至 hawkeye 目录，切换到项目的 pyenv, 环境分别在两个 terminal 里面跑下面两句 celery 命令
```
celery -A hawkeye beat -l info
celery -A hawkeye worker --loglevel=info --concurrency=4 --autoscale=4,4
```

## 6 Java后台

```
用IntelleJ打开runner2 文件夹
第一次需要会自动安装 maven 依赖
用 IntelleJ 跑 newapplication.java里面的 main
```

## 7 安装 sysbeach 然后触发负载

```
brew install sysbench

mysql> create database dbtest;
Query OK, 1 row affected (0.04 sec)

sysbench --test=./local/Cellar/sysbench/1.0.9/share/sysbench/oltp_read_only.lua  --mysql-db=dbtest --mysql-user=root --mysql-password=Password1 prepare


sysbench --test=./local/Cellar/sysbench/1.0.9/share/sysbench/oltp_read_only.lua  --mysql-db=dbtest --mysql-user=root --mysql-password=Password1 --num-threads=2 --max-time=120 --max-requests=0 run

mysql> show processlist;
+----+-------+-----------------+--------+---------+------+--------------+--------------------------------------------------------------------+
| Id | User  | Host            | db     | Command | Time | State        | Info                                                               |
+----+-------+-----------------+--------+---------+------+--------------+--------------------------------------------------------------------+
|  5 | wujie | localhost:62994 | wujie  | Sleep   | 1478 |              | NULL                                                               |
|  6 | root  | localhost       | NULL   | Query   |    0 | starting     | show processlist                                                   |
|  8 | root  | localhost       | dbtest | Sleep   |    0 |              | NULL                                                               |
|  9 | root  | localhost       | dbtest | Execute |    0 | Sending data | SELECT DISTINCT c FROM sbtest1 WHERE id BETWEEN ? AND ? ORDER BY c |
| 10 | root  | localhost       | dbtest | Sleep   |    0 |              | NULL                                                               |
| 11 | root  | localhost       | dbtest | Execute |    0 | Sending data | SELECT DISTINCT c FROM sbtest1 WHERE id BETWEEN ? AND ? ORDER BY c |
+----+-------+-----------------+--------+---------+------+--------------+--------------------------------------------------------------------+
6 rows in set (0.00 sec)
```

## 重建 hawkeye 数据库

```
# 备份现有 database 中的数据
pg_dump --data-only --table=monitor_database hawkeye > onetable.pg

drop database hawkeye
CREATE DATABASE hawkeye ENCODING 'UTF8' OWNER yunqu; 


python ./manage.py migrate --settings=hawkeye.settings.default
python ./manage.py createsuperuser --settings=hawkeye.settings.default

# 恢复 database 数据
psql hawkeye < onetable.pg
```

## celery

使用django-celery-beat

```
//celery -A hawkeye beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

celery -A hawkeye beat -l info
celery -A hawkeye worker -B --loglevel=info
```

## oracle 执行一个死循环的 SQL, 使顶级活动有数据可以进行测试

1 创建一个表
```
create table kill_cpu (n, primary key(n)) organization index
as
select rownum n
from all_objects
where rownum <= 23
;
```

2. 执行死循环 SQL
```
select count(*) X
from kill_cpu
connect by n > prior n
start with n = 1
;
```