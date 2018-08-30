# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/alarm/services/sendWarnService.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 808 bytes
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.core.mail.backends.smtp import EmailBackend
from alarm.models import Mail_Config

def send_warn_message_email(receiver_list, header, warn_message):
    config_list = Mail_Config.objects.all()
    if not config_list:
        return
    config = config_list[0]
    backend = EmailBackend(host=config.host, port=config.port, username=config.username, password=config.password,
      use_ssl=config.use_ssl,
      fail_silently=False)
    email = EmailMessage(subject=f'''[]{header}''', body=f''':
{warn_message}''', from_email=config.address, to=receiver_list,
      connection=backend)
    email.send()
# okay decompiling ./restful/hawkeye/api/v1/alarm/services/sendWarnService.pyc
