from rest_framework import routers, serializers, viewsets
from rest_framework.mixins import CreateModelMixin

from user.models import UserModel, FileModel
from common import common
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler


class UserModelSerializers(serializers.ModelSerializer):
    createTime = serializers.DateTimeField(format="%Y-%m-%d %H-%M-%S", read_only=True)

    def validate(self, attrs):
        """检验用的"""
        if not attrs['name']:
            raise serializers.ValidationError('用户名不能为空')

        return attrs

    class Meta:
        model = UserModel
        fields = ['id', 'name', 'password', 'createTime']  # 全部


class LoginSerializers(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="密码", write_only=True, label='密码'
    )
    token = serializers.CharField(max_length=256, read_only=True)

    class Meta:
        model = UserModel
        fields = ['name', 'password', 'token']  # 全部

    def create(self, validated_data):

        name = validated_data['name']
        password = validated_data['password']
        user = UserModel.objects.filter(name=name).first()
        if user:
            if user.password == password:
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                user.token = token
                return user
        else:
            raise common.ValidationErrorFailed('账户密码错误')


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileModel
        fields = '__all__'
