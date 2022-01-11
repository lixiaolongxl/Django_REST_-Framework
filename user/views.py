from datetime import datetime, timedelta

from django.views import View
import uuid
from django.http import HttpResponse, JsonResponse
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.views import APIView

# Create your views here.
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from Util.auth import JwtAuthentication
from Util.custom_page_size import CustomPageSize
from common import common
from user.models import UserModel
from user.serializers import UserModelSerializers, LoginSerializers
from rest_framework.response import Response


class UserViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin,
                  GenericViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserModelSerializers
    # authentication_classes = [JwtAuthentication,]
    # 添加查询
    # filter_backends = (DjangoFilterBackend,) #单个执行过滤
    filter_fields = ['id', 'name', 'createTime']

    # 分页 可以改变page_size的大小
    pagination_class = CustomPageSize


class LoginUserView(APIView):


    def post(self, request):
        name = request.data.get('name')
        password = request.data.get('password')

        user_object = UserModel.objects.filter(name=name, password=password).first()
        if not user_object:
            return Response({'msg': '用户名或密码错误'})

        randomstring = str(uuid.uuid4())
        user_object.token = randomstring;
        user_object.save()
        request.session['token'] = randomstring;
        request.session.set_expiry(10)
        return Response({'msg': '登录成功', 'data': randomstring})
        # res = Response({'msg': '登录成功', 'data': randomstring})
        # res.set_cookie('token1', randomstring, expires=datetime.now() + timedelta(14))
        # return res;
        # return res.set_cookie('token', randomstring, expires=datetime.now() + timedelta(14))


class LoginViewSet(GenericViewSet):
    queryset = UserModel.objects.all()
    serializer_class = LoginSerializers
    authentication_classes = []
    def create(self, request):
        name = request.data.get('name')
        password = request.data.get('password')
        user_object = UserModel.objects.filter(name=name, password=password).first()

        if not user_object:
            return Response({'msg': '用户名或密码错误'})
        user_object.username = name;
        payload = jwt_payload_handler(user_object)
        token = jwt_encode_handler(payload)
        return Response({'msg': '登录成功', 'data': {
            'token': token,
            'name': user_object.username,
            'id': user_object.id
        }})
