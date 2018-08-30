function msg() {
local type="$1"
local msg="$2"
local now=$(date +"%Y.%m.%d-%H:%M:%S")

echo "${type} : ${now} : ${msg}"
}


msg INFO "Hawkeye Stop Begin"

ps -ef | egrep "daphn|manage.py|java|celery|gunicorn" | grep -v grep | awk '{print "kill -9 " $2}' | sh
ps -ef | egrep "daphn|manage.py|java|celery|gunicorn" | grep -v grep

msg INFO "Hawkeye Stop Completed"
