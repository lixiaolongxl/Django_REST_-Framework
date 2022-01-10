from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin


class MYmid(MiddlewareMixin):

    def process_request(self, request):

        print(request.path)

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        if request.path != '/api/login/':
            session = request.session.get('token')
            if not session:
                return JsonResponse({'msg': '暂无权限请重新登录', 'code': 403})

    def process_response(self, request, response):
        return response
