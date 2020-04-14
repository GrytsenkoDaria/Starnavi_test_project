from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

from rest_framework.authtoken.models import Token
from re import sub

from social_network.models import User


class UpdateLastActivityMiddleware(MiddlewareMixin):
    def process_request(self, request):
        header_token = request.META.get('HTTP_AUTHORIZATION', None)
        if header_token is not None:
            try:
                token = sub('Token ', '', header_token)
                token_obj = Token.objects.get(key=token)
                request.user = token_obj.user
            except Token.DoesNotExist:
                pass
            current_user = request.user
            current_user = User.objects.get(id=request.user.id)
            current_user.last_activity = timezone.now()
            current_user.save(update_fields=['last_activity'])
