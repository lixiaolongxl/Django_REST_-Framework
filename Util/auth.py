from rest_framework.authentication import BaseAuthentication


class JwtAuthentication(BaseAuthentication):
    def authenticate(self, request):
        pass
