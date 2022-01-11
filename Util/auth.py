from rest_framework.authentication import BaseAuthentication
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication, jwt_decode_handler
from common import common
from rest_framework.exceptions import AuthenticationFailed
import jwt


class JwtAuthentication(BaseJSONWebTokenAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            payload = jwt_decode_handler(token)
        except jwt.ExpiredSignature:
            raise common.ValidationErrorFailed('token过期了')
        except jwt.DecodeError:
            raise AuthenticationFailed({
                'code': 204,
                'msg': 'token失效了'
            })
        except jwt.InvalidTokenError:
            raise common.ValidationErrorFailed('不合法的token')
        person = payload;

        return person, token
