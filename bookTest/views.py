# Create your views here.
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from django.views import View

from Util.custom_page_size import CustomPageSize
from .models import Book
from rest_framework import serializers, viewsets
from django.http import QueryDict
from .serializers import BookInfoSerializers, BookInfoModelSerializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView, ListCreateAPIView, UpdateAPIView, \
    DestroyAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin, \
    RetrieveModelMixin
from rest_framework.renderers import JSONRenderer
from rest_framework.viewsets import ViewSet, GenericViewSet, ReadOnlyModelViewSet, ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

import json


class BookListView(View):
    def get(self, request):

        books = Book.objects.all().values()
        # print(books);
        return JsonResponse({
            'code': 200,
            'data': list(books)
        })

    def post(self, request):

        # print(bool(request.POST['isSell']))

        if request.POST['isSell'] == 'true':
            isSell = True
        else:
            isSell = False
        books = Book.objects.create(
            name=request.POST['name'],
            desc=request.POST['desc'],
            read=request.POST['read'],
            isSell=isSell,
        )
        books.save()
        return JsonResponse({
            'code': 200,
            'msg': '创建成功',
            'data': books.name
        })


def object_to_json(obj):
    return dict([(kk, obj.__dict__[kk]) for kk in obj.__dict__.keys() if kk != "_state"])


class BookDetailView(View):
    def get(self, request, pk):
        books = Book.objects.get(pk=pk)
        print(books)
        return JsonResponse({
            'code': 200,
            'msg': '创建成功',
            'data': object_to_json(books)
        })

    def put(self, request, pk):
        books = Book.objects.get(pk=pk)
        body = request.body
        jsonb = body.decode()

        # str类型转换为字典类型
        params = json.loads(jsonb)

        books.name = params['name'],
        # print(params['name'])
        books.save()
        return JsonResponse({
            'code': 200,
            'msg': '更新成功',
            'data': books.name
        })

    def delete(self, request, pk):
        books = Book.objects.get(pk=pk)
        books.delete()
        return JsonResponse({
            'code': 200,
            'msg': '删除成功',
        })


class BookInfoView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookInfoSerializers


class BookInfoViewS(APIView):
    def get(self, request):
        books = Book.objects.all()
        bs = BookInfoSerializers(instance=books, many=True)  # 如果是查询集需要加many=True
        # bs.data
        # print(bs.data)
        # books = Book.objects.get(pk=1)
        # books.hello ='qqqq'
        # bs = BookInfoSerializers(instance=books)
        return Response({'data': bs.data, 'code': 200, 'msg': 'success'}, status.HTTP_200_OK)
        # return JsonResponse({
        #     'code': 200,
        #     'msg': 'success',
        #     'data': bs.data
        # })

    def post(self, request):
        """反序列化演示"""
        data = request.data
        # books = Book.objects.all()
        bs = BookInfoSerializers(data=data)
        isv = bs.is_valid()
        if isv:
            res = bs.save()
            return Response({'data': bs.validated_data, 'code': 200, 'msg': '创建成功'}, status.HTTP_200_OK)

        return Response({'code': 200, 'msg': 'err'}, status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        data = request.data
        books = Book.objects.get(pk=pk)
        bs = BookInfoSerializers(instance=books, data=data)
        if bs.is_valid():
            res = bs.save()

            return Response({'data': bs.validated_data, 'code': 200, 'msg': '修改成功'}, status.HTTP_204_NO_CONTENT)
        return Response({'code': 200, 'msg': 'err'}, status.HTTP_400_BAD_REQUEST)


class BookInfoAPIView(APIView):

    def get(self, request):
        books = Book.objects.all()
        bms = BookInfoModelSerializers(books, many=True);
        return Response({'data': bms.data, 'code': 200, 'msg': 'success'}, 200)

    def post(self, request: object) -> object:
        bs = BookInfoModelSerializers(data=request.data)
        bs.is_valid(raise_exception=True)
        res = bs.save()
        return Response({'data': bs.validated_data, 'code': 200, 'msg': '创建成功'}, status.HTTP_200_OK)


class BookDetailAPIView(APIView):

    def get(self, request, pk):
        try:
            books = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response(status.HTTP_400_BAD_REQUEST)
        bms = BookInfoModelSerializers(books);
        return Response({'data': bms.data, 'code': 200, 'msg': 'success'}, 200)

    def delete(self, request, pk):
        try:
            books = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response(status.HTTP_400_BAD_REQUEST)
        books.delete()
        return Response({'code': 200, 'msg': 'success'}, status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        try:
            books = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response(status.HTTP_400_BAD_REQUEST)
        bs = BookInfoModelSerializers(books, data=request.data)
        bs.is_valid(raise_exception=True)
        res = bs.save()
        return Response({'data': bs.data, 'code': 200, 'msg': '修改成功'}, status.HTTP_204_NO_CONTENT)


class BooKInfoGenericAPIView(GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookInfoModelSerializers

    def get(self, request):
        qs = self.get_queryset()
        bms = self.get_serializer(qs, many=True)
        return Response({'data': bms.data, 'code': 200, 'msg': 'success'}, 200)

    def post(self, request):
        bs = self.get_serializer(data=request.data)
        bs.is_valid(raise_exception=True)
        bs.save()
        return Response({'data': bs.data, 'code': 200, 'msg': '创建成功'})


class BooKDetailGenericAPIView(GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookInfoModelSerializers

    def get(self, request, pk):
        book = self.get_object()
        bms = self.get_serializer(book)
        return Response({'data': bms.data, 'code': 200, 'msg': 'success'}, 200)

    def put(self, request, pk):
        books = self.get_object()
        bms = self.get_serializer(books, data=request.data)
        bms.is_valid(raise_exception=True)
        bms.save()
        return Response({'data': bms.data, 'code': 200, 'msg': '更新成功'})

    def delete(self, request, pk):
        books = self.get_object()
        books.delete()
        return Response({'code': 200, 'msg': 'success'}, status.HTTP_204_NO_CONTENT)


"""
class BooKInfoGenericAPIViewMixins(CreateModelMixin, ListModelMixin, GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookInfoModelSerializers

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class BooKDetailGenericAPIViewMixins(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookInfoModelSerializers

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)
"""


# class BooKInfoGenericAPIViewMixins(CreateAPIView, ListAPIView):
class BooKInfoGenericAPIViewMixins(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookInfoModelSerializers


# class BooKDetailGenericAPIViewMixins(UpdateAPIView, DestroyAPIView, RetrieveAPIView):
class BooKDetailGenericAPIViewMixins(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookInfoModelSerializers


class BoobInfoViewSet(ViewSet):

    def list(self, request):
        books = Book.objects.all()
        bms = BookInfoModelSerializers(books, many=True);
        return Response({'data': bms.data, 'code': 200, 'msg': 'success'}, 200)

    def retrieve(self, request, pk):
        books = Book.objects.get(pk=pk)
        bms = BookInfoModelSerializers(books);
        return Response({'data': bms.data, 'code': 200, 'msg': 'success'}, 200)

    def create(self, request):
        bms = BookInfoModelSerializers(data=request.data)
        bms.is_valid(raise_exception=True)
        bms.save()
        return Response({'data': bms.data, 'code': 200, 'msg': 'success'}, 200)

    def update(self, request, pk):
        books = Book.objects.get(pk=pk)
        bms = BookInfoModelSerializers(books, data=request.data)
        bms.is_valid(raise_exception=True)
        bms.save()
        return Response({'data': bms.data, 'code': 200, 'msg': 'success'}, 200)

    def destroy(self, request, pk):
        try:
            books = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response(status.HTTP_400_BAD_REQUEST)
        books.delete()
        return Response({'code': 200, 'msg': 'success'}, status.HTTP_204_NO_CONTENT)


"""
class BookInfoGenericViewSet(GenericViewSet):
    queryset = Book.objects.all()
    serializer_class = BookInfoModelSerializers

    def list(self, request):
        qs = self.get_queryset()
        bms = self.get_serializer(qs, many=True)
        return Response({'data': bms.data, 'code': 200, 'msg': 'success'}, 200)

    def retrieve(self, request, pk):
        book = self.get_object()
        bms = self.get_serializer(book)
        return Response({'data': bms.data, 'code': 200, 'msg': 'success'}, 200)

    def create(self, request):
        bms = self.get_serializer(data=request.data)
        bms.is_valid(raise_exception=True)
        bms.save()
        return Response({'data': bms.data, 'code': 200, 'msg': 'success'}, 200)

    def update(self, request, pk):
        book = self.get_object()
        bms = self.get_serializer(book, data=request.data)
        bms.is_valid(raise_exception=True)
        bms.save()
        return Response({'data': bms.data, 'code': 200, 'msg': 'success'}, 200)

    def destroy(self, request, pk):
        book = self.get_object()
        book.delete()
        return Response(status.HTTP_204_NO_CONTENT)
"""

"""
class BookInfoGenericViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin,
                             GenericViewSet):
    queryset = Book.objects.all()
    serializer_class = BookInfoModelSerializers
"""


class BookInfoGenericViewSet(ModelViewSet):
    """
         list:
         返回所有项目信息

         create:
         创建项目

         retrieve:
         获取某个项目的详细信息

         update:
         更新项目

         destroy：
         删除项目

         latest:
         查询最后一本书

         read:
         修改阅读量
    """
    queryset = Book.objects.all()
    serializer_class = BookInfoModelSerializers
    # 单个增加权限
    # permission_classes = (IsAuthenticatedOrReadOnly,)

    # 添加查询
    # filter_backends = (DjangoFilterBackend,) #单个执行过滤
    filter_fields = ['name', 'book_id', 'isSell', 'read']

    # #指定后端为排序
    # filter_backends = [OrderingFilter]
    # # 指定排序字段 http://localhost:8000/lbooks/?ordering=-createTime
    # ordering_fields = ['book_id', 'createTime']

    # 分页 可以改变page_size的大小
    pagination_class = CustomPageSize

    # 查询最后一本书 detail=False 表示列表视图
    @action(methods=['get'], detail=False)
    def latest(self, request):
        # 主动抛出异常
        # from django.db import DatabaseError
        # raise DatabaseError()

        book = Book.objects.latest('book_id')
        serializer = self.get_serializer(book)
        return Response(serializer.data)

    # 修改阅读量 detail=True 表示非列表视图
    @action(methods=['put'], detail=True)
    def read(self, request, pk):
        book = self.get_object()
        book.read = request.data.get('read')
        book.save()
        serializer = self.get_serializer(book)
        return Response(serializer.data)
