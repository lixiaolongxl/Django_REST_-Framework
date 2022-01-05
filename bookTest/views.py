from django.shortcuts import render

# Create your views here.
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from django.views import View
from .models import Book
from rest_framework import serializers, viewsets
from django.http import QueryDict
from .serializers import BookInfoSerializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
import json


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")


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
