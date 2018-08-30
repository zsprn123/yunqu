tar zxvf prometheus.tar.gz
cd prometheus
./start.sh
cd ~
sh ./deploy.sh
mkdir -p /home/hawkeye/hawkeye_logs/
echo "from authx.models import User; u = User(username='admin', email='admin@example.com', password='Qwer1234', is_superuser=True,is_staff=True); u.set_password('Qwer1234'); u.save();" | python -u /home/hawkeye/hawkeye-v2/restful/hawkeye/manage.py shell --settings hawkeye.settings.default