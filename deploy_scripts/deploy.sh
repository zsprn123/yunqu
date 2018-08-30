mkdir -p /home/hawkeye/hawkeye-logs

date_postfix=`date +%Y%m%d`

echo ${date_postfix}

DIRECTORY=hawkeye-v2

if [ -d "$DIRECTORY" ]; then
  cp -rf $DIRECTORY ${DIRECTORY}.${date_postfix}
fi

tar -xzpvf hawkeye.tgz 

# ipaddr=$(/sbin/ifconfig|awk -F ':' 'NR==2 {print $2}'|grep -oP '\d+\.\d+\.\d+\.\d+'|grep -v "127.0.0.1")
# sed -i -e "s#proxy:#host:'${ipaddr}',\n    proxy:#" hawkeye/fed/webpack.config.js

python /home/hawkeye/hawkeye-v2/restful/hawkeye/manage.py migrate --settings=hawkeye.settings.default

cd hawkeye-v2
rm -rf /usr/share/nginx/hawkeye/*
mv static /usr/share/nginx/hawkeye/

echo "from api.v1.monitor.services.createdbService import init_all; init_all();" | python -u /home/hawkeye/hawkeye-v2/restful/hawkeye/manage.py shell --settings hawkeye.settings.default

cd restful/hawkeye
python ./delete_history_tasks.pyc