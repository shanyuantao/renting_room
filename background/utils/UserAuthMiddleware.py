import datetime
import re

from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

from app.models import User


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ticket = request.COOKIES.get('ticket')
        if request.path == '/app/hello/' or request.path == '/app/adminlogout/' or request.path == '/app/refresh/' or request.path == '/app/update_pwd/' or re.match(r'/app/house_manage/(\d+)/$', request.path) or re.match(r'/app/system/$', request.path) or re.match(r'/app/del_house/(\d+)/(\d+)/$', request.path) or re.match(r'/app/del_house1/(\d+)/$', request.path) or re.match(r'/app/edit_house/(\d+)/(\d+)/$', request.path) or re.match(r'/app/search/(\d+)/(\w+)/(\w+)/(.+)/(\d+)/$', request.path) or request.path.startswith('/app/set_avatar/') or request.path.startswith('/app/manage_account/') or request.path.startswith('/app/edit_account/') or request.path.startswith('/app/forbidden_account/') or request.path.startswith('/app/save_account/'):
            if User.objects.filter(ticket=ticket).exists() and ticket != None:
                user = User.objects.get(ticket=ticket)
                user.out_time = datetime.datetime.now()
                user.save()
            else:
                return HttpResponseRedirect('/app/adminlogin/')