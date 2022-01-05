from rest_framework import routers, serializers, viewsets
from .models import Book


#
# class BookInfoSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Book
#         fields = '__all__'

class BookInfoSerializers(serializers.Serializer):
    book_id = serializers.IntegerField(label='ID', read_only=True)
    name = serializers.CharField(max_length=128, label="书名")
    desc = serializers.CharField(max_length=500, label="书描述")
    read = serializers.IntegerField(label="阅读量", required=False)
    isSell = serializers.BooleanField(label="是否可卖", required=False)

    # createTime = serializers.DateTimeField(required=False, label="创建时间")
    # hello = serializers.CharField(label="临时变量",)
    def create(self, validated_data):

        pass

    def update(self, instance, validated_data):
        pass