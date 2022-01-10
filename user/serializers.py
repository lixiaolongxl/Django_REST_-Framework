from rest_framework import routers, serializers, viewsets
from user.models import UserModel


class UserModelSerializers(serializers.ModelSerializer):
    createTime = serializers.DateTimeField(format="%Y-%m-%d %H-%M-%S", read_only=True)

    def validate(self, attrs):
        """检验用的"""
        if not attrs['name']:
            raise serializers.ValidationError('用户名不能为空')

        return attrs

    class Meta:
        model = UserModel
        fields = ['id', 'name', 'createTime']  # 全部



