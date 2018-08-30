# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./hawkeye/routing.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 3133 bytes
import json
from channels import Group
from channels.sessions import channel_session
from channels.routing import route
from django.contrib.auth import get_user_model
from guardian.shortcuts import get_objects_for_user
from api.celery.dashboard.activity import update_dashboard_data
from api.v1.monitor.services.activityService import get_database_activity
from api.v1.monitor.services.performance.performanceService import PERFORMANCE_FUNCTION
from hosts.models import Host
from monitor.models import Database

@channel_session
def ws_connect(message):
    ws, prefix, label = message['path'].strip('/').split('/')
    message.reply_channel.send({'accept': True}, immediately=True)
    if prefix == 'performance':
        database = Database.objects.get(pk=label)
        Performance = PERFORMANCE_FUNCTION.get(database.db_type)
        result = Performance(database).get_history_data()
        message.reply_channel.send({'text': json.dumps(result)})
        Group(prefix + '-' + label).add(message.reply_channel)
    else:
        if prefix == 'activity':
            result = get_database_activity(label, time_span='realtime')
            message.reply_channel.send({'text': json.dumps(result)})
            Group(prefix + '-' + label).add(message.reply_channel)
        else:
            if prefix == 'alarm':
                user = get_user_model().objects.get(pk=label)
                database_list = get_objects_for_user(user, 'monitor.view_database')
                for database in database_list:
                    Group(prefix + '-' + str(database.id)).add(message.reply_channel)

                for host in Host.objects.all():
                    Group(prefix + '-' + str(host.id)).add(message.reply_channel)

            else:
                if prefix == 'index':
                    user = get_user_model().objects.get(pk=label)
                    if user.is_superuser:
                        database_list = (Database.objects.all().exclude(is_switch_off=True)).exclude(disabled=True)
                    else:
                        database_list = (get_objects_for_user(user, 'monitor.view_database').exclude(is_switch_off=True)).exclude(disabled=True)
                    text2 = update_dashboard_data(database_list)
                    Group(prefix + '-' + str(user.id)).add(message.reply_channel)
                    Group(prefix + '-' + str(user.id)).send({'text': json.dumps(text2)}, immediately=True)


@channel_session
def ws_receive(message):
    message.reply_channel.send({'text': message.content['text']})


@channel_session
def ws_disconnect(message):
    Group('chat').discard(message.reply_channel)


channel_routing = [
 route('websocket.connect', ws_connect),
 route('websocket.receive', ws_receive),
 route('websocket.disconnect', ws_disconnect)]
# okay decompiling ./restful/hawkeye/hawkeye/routing.pyc
