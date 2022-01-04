from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views import View
from .models import Book


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")


class BookListView(View):
    def get(self, request):

        books = Book.objects.all()
        print(books);
        return HttpResponse("Hello, world. You're at the polls index.")
        # pass

    def post(self, request):
        pass


class BookDetailView(View):
    def get(self, request, pk):
        # print(pk)
        return HttpResponse("detail, world. You're at the polls index.")

    def put(self, request, pk):
        pass

    def delete(self, request, pk):
        pass
