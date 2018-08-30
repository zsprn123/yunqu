# uncompyle6 version 3.2.3
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.5 (default, Jul 13 2018, 13:06:57) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-28)]
# Embedded file name: ./api/v1/auth/views.py
# Compiled at: 2018-08-23 19:33:14
# Size of source mod 2**32: 9067 bytes
import base64, os
from datetime import datetime
from django.contrib.auth import get_user_model, get_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.transaction import atomic
from django.utils.encoding import smart_text, smart_bytes
from guardian.models import UserObjectPermission
from rest_condition import Or
from rest_framework import status
from rest_framework.decorators import api_view, list_route
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
import json
from api.v1.auth.filtersets import UserFilterSet, PermissionFilterSet, UserObjectPermissionFilterSet
from api.v1.auth.serializers import UserSerializer, UserGroupSerializer, PermissionSerializer, UserObjectPermissionSerializer
from api.v1.monitor.services.activity.oracleActivtyService import get_oracle_activity_ws, get_oracle_activity
from authx.permissions import IsAdminUser, IsSuperUser
from authx.models import User
from common.yunquAuthorization import verify, prepare_mac_str
from common.yunquAuthorizationUtil import LICENSE_FILE, get_lisence_info
import time
from django.conf import settings
from monitor.models import Database
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

@api_view(['GET'])
def test(request):
    return Response({'msg': 'v1 test'})


def jwt_response_special_handling(response, user=None):
    if user is None:
        token = response.data.get('token')
        user = __resolve_user(token)
    return response


def __resolve_user(token):
    serializer = VerifyJSONWebTokenSerializer(data={'token': token})
    serializer.is_valid(raise_exception=True)
    return serializer.object.get('user')


@api_view(['POST'])
def register(request):
    composed_profile = {'phone_num':request.data.get('phone_num'), 
     'city':request.data.get('city')}
    request.data['profile'] = composed_profile
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        response_data = jwt_response_payload_handler(token, user, request)
        return jwt_response_special_handling(Response(response_data, status.HTTP_201_CREATED),
          user=user)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    request = request._request
    response = obtain_jwt_token(request)
    if status.is_success(response.status_code):
        response = jwt_response_special_handling(response)
    return response


class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    filter_class = UserFilterSet
    permission_classes = (Or(IsAdminUser, IsAuthenticated),)

    def create(self, request, *args, **kwargs):
        if not request.user:
            return Response({'detail': 'Error decoding signature.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            request.data['owner'] = request.user.id
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @list_route(methods=[
     'get'],
      url_path='user-info')
    def current_user_info(self, request):
        serializer = UserGroupSerializer(request.user)
        return Response(serializer.data)


class PermissionViewSet(ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    filter_class = PermissionFilterSet
    permission_classes = (Or(IsAdminUser, IsSuperUser),)


class UserObjectPermissionViewSet(ModelViewSet):
    queryset = UserObjectPermission.objects.all()
    serializer_class = UserObjectPermissionSerializer
    filter_class = UserObjectPermissionFilterSet
    permission_classes = (Or(IsAdminUser, IsSuperUser),)

    @list_route(methods=[
     'post'],
      url_path='grant',
      permission_classes=(
     Or(IsAdminUser, IsSuperUser),))
    @atomic
    def grant_permissions(self, request):
        user_id = request.data.get('user') or request.data.get('user_id') or ''
        content_type_id = request.data.get('content_type') or request.data.get('content_type_id') or ''
        permission_id = request.data.get('permission') or request.data.get('permission_id') or ''
        user = get_object_or_404(get_user_model(), id=user_id)
        content_type = get_object_or_404(ContentType, id=content_type_id)
        permission = get_object_or_404(Permission, id=permission_id)
        (UserObjectPermission.objects.filter(user=user, content_type=content_type,
          permission=permission)).delete()
        object_pks = request.data.get('object_pks') or []
        objs = content_type.get_all_objects_for_this_type(id__in=object_pks)
        items = []
        for obj in objs:
            items.append(UserObjectPermission(user=user, content_type=content_type,
              permission=permission,
              object_pk=obj.id))

        UserObjectPermission.objects.bulk_create(items)
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def grantYunquAuthorization(request):
    if request.method == 'GET':
        try:
            with open(LICENSE_FILE) as (data_file):
                data = json.load(data_file)
        except Exception as e:
            data = {}

        product_key = data.get('product_key', '')
        json_data = {'client_token':smart_text(base64.b64encode(smart_bytes(prepare_mac_str()))), 
         'product_key':product_key}
        return Response(json_data, status=status.HTTP_200_OK)
    else:
        data = request.data
        if 'product_code' not in data:
            return Response({'error_message': 'product_code is required'}, status=status.HTTP_400_BAD_REQUEST)
        product_code = data['product_code']
        data['signature'] = product_code[:172]
        json_obj = json.loads(smart_text(base64.b64decode(product_code[172:])))
        expiry_date = datetime.strptime(json_obj['expiry_date'], '%Y%m%d')
        if expiry_date < datetime.today():
            return Response({'error_message': 'Product code expired.'}, status=status.HTTP_400_BAD_REQUEST)
        issue_date = datetime.strptime(json_obj['issue_date'], '%Y%m%d')
        if datetime.today() < issue_date:
            return Response({'error_message': 'System time invalid.'}, status=status.HTTP_400_BAD_REQUEST)
        data.update(json_obj)
        if not (verify(**data)):
            return Response({'error_message': 'Product code is invalid'}, status=status.HTTP_400_BAD_REQUEST)
        with open(LICENSE_FILE, 'w') as (outfile):
            json.dump(data, outfile)
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def license_info(request):
    json_data = get_lisence_info()
    json_data['issue_date'] = datetime.strptime(json_data['issue_date'], '%Y%m%d').strftime('%Y-%m-%d') if json_data['issue_date'] else ''
    json_data['expiry_date'] = datetime.strptime(json_data['expiry_date'], '%Y%m%d').strftime('%Y-%m-%d') if json_data['expiry_date'] else ''
    return Response(json_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def version(request):
    VERSION_FILE = os.path.join(settings.BASE_DIR, '.version')
    data = 'none|none'
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE) as (data_file):
            data = data_file.readline().split('|')
    return Response({'version':data[1][:7],  'update_data':data[0]}, status=status.HTTP_200_OK)
# okay decompiling ./restful/hawkeye/api/v1/auth/views.pyc
