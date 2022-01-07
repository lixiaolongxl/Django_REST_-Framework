from rest_framework import routers, serializers, viewsets
from rest_framework.exceptions import APIException
from .models import Book


# 自动生产模型中的字段 实现create update 代码实现了
class BookInfoModelSerializers(serializers.ModelSerializer):
    def validate(self, attrs):
        """检验用的"""
        if not attrs['name']:
            # APIException('请输入书名')
            raise serializers.ValidationError('书名不能为空')

        if not attrs.get('desc'):
            raise serializers.ValidationError('书名描述不能为空')

        return attrs

    class Meta:
        model = Book
        fields = '__all__'  # 全部
        # fields=['name','desc'] #指定几个
        # exclude =['createTime'] # 除了createTime 其他都映射
        extra_kwargs: {
            "read": {"min_value": 0, "required": True}
        }
        read_only_fields: ['book_id']  # 标记自读


class BookInfoSerializers(serializers.Serializer):
    book_id = serializers.IntegerField(label='ID', read_only=True)
    name = serializers.CharField(max_length=128, label="书名")
    desc = serializers.CharField(max_length=500, label="书描述")
    read = serializers.IntegerField(label="阅读量", required=False)
    isSell = serializers.BooleanField(label="是否可卖", required=False)

    # createTime = serializers.DateTimeField(required=False, label="创建时间")
    # hello = serializers.CharField(label="临时变量",)
    def validate(self, attrs):
        """检验用的"""
        pass

    def create(self, validated_data):
        return Book.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.desc = validated_data.get('desc', instance.desc)
        instance.read = validated_data.get('read', instance.read)
        instance.isSell = validated_data.get('isSell', instance.isSell)
        instance.save()
        return instance
