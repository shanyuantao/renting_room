import datetime

from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

from app.models import User


class AuthMiddleware(MiddlewareMixin):
    pass
#     def process_request(self, request):
#         ticket = request.COOKIES.get('ticket')
#         if request.path != '/app/hello/':
#             if User.objects.filter(ticket=ticket).exists():
#                 user = User.objects.get(ticket=ticket)
#                 user.out_time = datetime.datetime.now()
#                 user.save()
#             else:
#                 return HttpResponseRedirect('/app/admin/')