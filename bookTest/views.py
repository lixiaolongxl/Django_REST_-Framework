# Create your views here.
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from django.views import View
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
from rest_framework.viewsets import ViewSet, GenericViewSet
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