import datetime

from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

from app.models import User


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ticket = request.COOKIES.get('ticket')
        if request.path != '/app/adminlogin/':
            if User.objects.filter(ticket=ticket).exists() and ticket != None:
                user = User.objects.get(ticket=ticket)
                user.out_time = datetime.datetime.now()
                user.save()
            else:
                return HttpResponseRedirect('/app/adminlogin/')