function msg() {
local type="$1"
local msg="$2"
local now=$(date +"%Y.%m.%d-%H:%M:%S")

echo "${type} : ${now} : ${msg}"
}

msg INFO "Hawkeye start Begin"

min_celery_workers=8
max_celery_workers=32

export DJANGO_PORT=8000
export SPRING_PORT=8080
export GUNICORN_PORT=8001
cd hawkeye-v2
nohup java -jar hawkeye-1.0-SNAPSHOT.jar --server.port=${SPRING_PORT} &
cd restful/hawkeye
celery -A hawkeye purge --force
nohup python ./manage.py runworker --exclude-channels http.request --settings=hawkeye.settings.prod --threads 100 2>&1 &
nohup celery -A hawkeye beat -l WARNING -f hawkeye-logs/celery-beat.log 2>&1 &
nohup celery multi start 2 -A hawkeye --concurrency=8 --logfile=hawkeye-logs/celery-worker.log --loglevel=INFO 2>&1 &
nohup daphne -p ${DJANGO_PORT} hawkeye.asgi:channel_layer --http-timeout 1200 --access-log /home/hawkeye/hawkeye-logs/daphne.log 2>&1 &

nohup gunicorn --env DJANGO_SETTINGS_MODULE=hawkeye.settings.prod -b 127.0.0.1:${GUNICORN_PORT} -k gevent hawkeye.wsgi -t 1200 -w 12 --threads 5 --access-logfile /home/hawkeye/hawkeye-logs/gunicorn.log 2>&1 &

msg INFO "Hawkeye start Completed"