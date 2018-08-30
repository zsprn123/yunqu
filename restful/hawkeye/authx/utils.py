# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./authx/utils.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 1489 bytes
from rest_framework import serializers
from authx.models import User
from rest_framework_jwt.utils import jwt_payload_handler as drf_jwt_payload_handler

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('password', )


def jwt_response_payload_handler(token, user=None, request=None):
    """
    Returns the response data for both the login and refresh views.
    Override to return a custom response such as including the
    serialized representation of the User.
    
    Deprecated: as some info can be within token xxx.yyy.zzz
    payload => yyy (base64 encoded)
    
    """
    return {'token':token, 
     'user':UserSerializer(user).data}


def jwt_payload_handler(user):
    payload = drf_jwt_payload_handler(user)
    return payload
# okay decompiling ./restful/hawkeye/authx/utils.pyc
