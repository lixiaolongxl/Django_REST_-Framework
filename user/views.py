from django.views import View
from django.http import HttpResponse, JsonResponse
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.views import APIView

# Create your views here.
from rest_framework.viewsets import GenericViewSet

from Util.custom_page_size import CustomPageSize
from user.models import UserModel
from user.serializers import UserModelSerializers


class UserViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin,
                  GenericViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserModelSerializers

    # 添加查询
    # filter_backends = (DjangoFilterBackend,) #单个执行过滤
    filter_fields = ['id', 'name', 'createTime']

    # 分页 可以改变page_size的大小
    pagination_class = CustomPageSize


class LoginUserView(APIView):
    def get(self, request):
        return JsonResponse({
            'code': 200,
        })
