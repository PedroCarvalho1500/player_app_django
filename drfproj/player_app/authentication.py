import datetime
from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
import pytz
from drfproj.settings import TOKEN_EXPIRE_TIME
from rest_framework.authtoken.models import Token as AuthToken


class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            token = AuthToken.objects.get(key=key)
        except AuthToken.DoesNotExist:
            raise AuthenticationFailed('Invalid token')
        
        if not token.user.is_active:
            raise AuthenticationFailed('User inactive or deleted!')
        
        utc_now = datetime.datetime.now()
        utc_now = utc_now.replace(tzinfo=pytz.utc)

        if token.created < utc_now - TOKEN_EXPIRE_TIME:
            raise AuthenticationFailed('Token has expired')
        
        return token.user, token