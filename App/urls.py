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
from rest_framework.documentation import include_docs_urls

from bookTest import views
from user import views as u_views
from bookTest.models import Book

# 只能结合视图集使用  routers.SimpleRouter 没有跟路由请求  routers.DefaultRouter() 有跟路由请求
router = routers.DefaultRouter()
# router.register(r'booksm', views.BookInfoView)
router.register(r'books', views.BookInfoGenericViewSet, basename='book')
router.register(r'users', u_views.UserViewSet, basename='user')
router.register(r'login', u_views.LoginViewSet, basename='login')
router.register(r'upload', u_views.FileViewSet, basename='upload')
urlpatterns = [
    path('admin/', admin.site.urls),

    # 最全的逻辑重写viewsets.ModelViewSet +  serializers.ModelSerializer
    path('api/', include(router.urls)),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # 自动生成api
    path('docs/', include_docs_urls(title="接口测试平台API文档", description="这个是接口平台的文档")),

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
    # path('lbooks', views.BoobInfoViewSet.as_view({'get': 'list', 'post': 'create'})),
    # path('lbooks/<int:pk>', views.BoobInfoViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}))

    # GenericViewSet + [mixins]
    # path('lbooks', views.BookInfoGenericViewSet.as_view({'get': 'list', 'post': 'create'})),
    # path('lbooks/<int:pk>',
    #      views.BookInfoGenericViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    # # 额外增加的行为单独定义路由如下获取 列表视图
    # path('lbooks/latest', views.BookInfoGenericViewSet.as_view({'get': 'latest'})),
    # # 额外增加的行为单独定义路由如下获非   列表视图
    # # path('lbooks/<int:pk>/read', views.BookInfoGenericViewSet.as_view({'put': 'read'})),
    # path('lbooks/read/<int:pk>', views.BookInfoGenericViewSet.as_view({'put': 'read'})),  # (这种也行)
]
