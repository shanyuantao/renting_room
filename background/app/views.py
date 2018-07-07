import datetime
import random

import time
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from app.models import User, Area, HouseType, House, HouseDetail
from app.status_code import USER_REGISTER_PARAMS_ERROR, USERNAME_NOT_EXIST, SUCCESS, USER_PASSWORD_ERROR, \
    INPUT_IS_INCONSISTENT


def adminlogout(request):
    if request.method == 'GET':
        response = HttpResponseRedirect('/app/adminlogin/')
        response.delete_cookie('ticket')
        return response



def adminlogin(request):
    if request.method == 'GET':
        return render(request, 'back_login.html')
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        if len(username) == 0:
            return JsonResponse(USER_REGISTER_PARAMS_ERROR)   # 账号/密码不能为空
        else:
            if User.objects.filter(account=username).exists() and User.objects.get(account=username).role_id == 2:
                password = request.POST.get('password')
                if len(password) == 0:
                    return JsonResponse(USER_REGISTER_PARAMS_ERROR)
                else:
                    user = User.objects.get(account=username)
                    if user.password == password:
                        s = 'qwertyuiopasdfghjklzxcvbnm'
                        ticket = ''
                        for i in range(18):
                            ticket += random.choice(s)
                        now_time = int(time.time())
                        ticket += str(now_time)

                        response = HttpResponseRedirect('/app/hello/')
                        response.set_cookie('ticket', ticket,max_age=600)
                        #这个函数里面，max_age就是cookie的超时时间，是以秒为单位的。也可以用expires设置绝对时间做为有效期，格式："Wdy, DD-Mon-YY HH:MM:SS GMT"，expires也可以是datetime.datetime的对象
                        user.ticket = ticket
                        user.out_time = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
                        user.save()
                        return response
            else:
                return JsonResponse(USERNAME_NOT_EXIST)  #用户名不存在


def hello(request):
    if request.method == 'GET':
        return render(request, 'backend.html')


def refresh(request):
    if request.method == 'GET':
        cookies = request.COOKIES.get('ticket')
        user = User.objects.get(ticket=cookies)
        data = SUCCESS
        data['user_id'] = user.user_id
        data['account'] = user.account
        data['phone'] = user.phone
        data['nick_name'] = user.nick_name
        data['avatar'] = user.avatar
        print(data)
        return JsonResponse(data)


def update_pwd(request):
    if request.method == 'GET':
        return render(request, 'update_pwd.html')
    if request.method == 'POST':
        ticket = request.COOKIES.get('ticket')
        password = request.POST.get('password')
        user = User.objects.get(ticket=ticket)
        if password == user.password:
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password1 == password2:
                user.password = password1
                user.save()
                return JsonResponse(SUCCESS)
            else:
                return JsonResponse(INPUT_IS_INCONSISTENT)
        else:
            return JsonResponse(USER_PASSWORD_ERROR)


def house_manage(request,the_page):
    if request.method == 'GET':
        positions = Area.objects.all()
        house_types = HouseType.objects.all()
        print(house_types)
        t = []
        for i in house_types:
            t.append(i.type_name[:2])
        new_type = list(set(t))
        new_type.sort()
        the_page = int(the_page)
        page_size=10
        pre_page = the_page - 1
        all_record = House.objects.all().count()
        total_page = (House.objects.all().count() // page_size) if (House.objects.all().count() % 10 == 0) else (House.objects.all().count() // page_size + 1)
        houses = House.objects.all()[pre_page * page_size: the_page * page_size]

        return render(request, 'house_manage.html',
                      {'positions':positions,
                       'new_type':new_type,
                       'houses':houses,
                       'the_page':the_page,
                       'total_page':total_page,
                       'all_record':all_record})


def system(request):
    if request.method == 'GET':
        return render(request, 'system_overview.html')


def del_house(request, house_id, the_page):
    if request.method == 'GET':
        House.objects.filter(house_id=house_id).delete()
        return HttpResponseRedirect('/app/house_manage/'+ the_page + '/')


def edit_house(request, house_id, the_page):
    if request.method == 'GET':
        house = House.objects.filter(house_id=house_id).first()
        areas = Area.objects.all()
        house_types = HouseType.objects.all()

        return render(request, 'edit_house.html',
                      {'the_page':the_page,
                       'house':house,
                       'areas':areas,
                       'house_types':house_types})
    if request.method == 'POST':
        house_id = request.POST.get('house_id')
        title = request.POST.get('title')
        area_id = request.POST.get('fangyuanEntity.fyDhCode')
        address = request.POST.get('fangyuanEntity.fyCh')
        acreage = request.POST.get('fangyuanEntity.fyFh')
        type_id = request.POST.get('fangyuanEntity.fyZongMj')
        price = request.POST.get('fangyuanEntity.fyJizuMj')
        lease = request.POST.get('fangyuanEntity.fyHxCode')
        nick_name = request.POST.get('fangyuanlianxiren')
        phone = request.POST.get('fangyuanEntity.fyZldz')
        house_status = request.POST.get('fangyuanEntity.fyStatus')
        house = House.objects.get(house_id=house_id)
        house.title = title
        house.address = address
        house.acreage = acreage
        house.area_id = area_id
        house.type_id = type_id
        house.price = price
        house.house_status = house_status
        house.save()

        house_detail = HouseDetail.objects.get(house_id=house_id)
        house_detail.lease = lease
        house_detail.save()

        user = User.objects.get(user_id=house.user_id)
        user.nick_name = nick_name
        user.phone = phone
        user.save()


        return HttpResponseRedirect('/app/house_manage/'+ the_page + '/')






# def update_house(request):
#     if request.method =='GET':
#         print(1)
#
#
#     if request.method == 'POST':
#
#
#         return None