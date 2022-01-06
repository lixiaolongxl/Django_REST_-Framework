"""App URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers, serializers, viewsets
from bookTest import views
from bookTest.models import Book

router = routers.DefaultRouter()
router.register(r'booksm', views.BookInfoView)
# router.register(r'booklist', views.BookInfoViewS)

urlpatterns = [
    path('admin/', admin.site.urls),

    # 最全的逻辑重写viewsets.ModelViewSet +  serializers.ModelSerializer
    path('', include(router.urls)),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # APIView + serializers.Serializer
    # path('bookss/<int:pk>', views.BookInfoViewS.as_view()),

    # View + 最原始的Django 编写
    # path('books', views.BookListView.as_view()), # 一键是不使用rest_framework 形式
    # path('books/<int:pk>', views.BookDetailView.as_view())

    #  APIView +  serializers.ModelSerializer
    # path('books', views.BookInfoAPIView.as_view()),
    # path('books/<int:pk>', views.BookDetailAPIView.as_view())

    #  GenericAPIView + serializers.ModelSerializer
    # path('books', views.BooKInfoGenericAPIView.as_view()),
    # path('books/<int:pk>', views.BooKDetailGenericAPIView.as_view())

    # mixins + GenericAPIView + serializers.ModelSerializer
    # path('books', views.BooKInfoGenericAPIViewMixins.as_view()),
    # path('books/<int:pk>', views.BooKDetailGenericAPIViewMixins.as_view())

    # viewsets.ViewSet + serializers.ModelSerializer
    # path('books', views.BoobInfoViewSet.as_view({'get': 'list', 'post': 'create'})),
    # path('books/<int:pk>', views.BoobInfoViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}))

    # GenericViewSet + [mixins]
    path('books', views.BookInfoGenericViewSet.as_view({'get': 'list'})),
    path('books/<int:pk>', views.BoobInfoViewSet.as_view({'get': 'retrieve'}))
]
