import datetime
import random

import time
from urllib import parse

import pymysql
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from app.models import User, Area, HouseType, House, HouseDetail, HouseImg, Count
from app.status_code import USER_REGISTER_PARAMS_ERROR, USERNAME_NOT_EXIST, SUCCESS, USER_PASSWORD_ERROR, \
    INPUT_IS_INCONSISTENT, SYSTEM_INSTUSION

client = pymysql.connect(host='101.132.39.189',
                       user='root',
                       passwd='2905058',
                       db='room',
                       port=3306,
                       charset='utf8'
                       )

cursor = client.cursor()


def adminlogout(request):
    """
    管理员退出
    :param request:
    :return: 退出登录状态, 返回登录页面
    """
    if request.method == 'GET':
        response = HttpResponseRedirect('/app/adminlogin/')
        response.delete_cookie('ticket')
        return response



def adminlogin(request):
    """
    管理员登录
    :param request:
    :return: 1.GET: 返回管理员登录页面
             2.POST: 登录成功返回后台页面, 登录失败返回响应(失败)数据信息给前端进行处理!
    """
    if request.method == 'GET':
        return render(request, 'back_login.html')
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        data = {}
        if len(username) == 0 or username == '用户名':
            data['error'] = USER_REGISTER_PARAMS_ERROR['msg']
            return render(request, 'login_error.html', data)   # 账号/密码不能为空
        else:
            if User.objects.filter(account=username).exists() and User.objects.get(account=username).role_id == 2:
                password = request.POST.get('password')
                if len(password) == 0:
                    data['error'] = USER_REGISTER_PARAMS_ERROR['msg']
                    return render(request, 'login_error.html', data)
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
                        response.set_cookie('ticket', ticket,max_age=3600)
                        #这个函数里面，max_age就是cookie的超时时间，是以秒为单位的。也可以用expires设置绝对时间做为有效期，格式："Wdy, DD-Mon-YY HH:MM:SS GMT"，expires也可以是datetime.datetime的对象
                        user.ticket = ticket
                        user.out_time = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
                        user.save()
                        # 问题1: 如果使用ajax请求登录的情况下, 如何给客户端返回设置的cookie呢?
                        return response
            else:
                data['error'] = USERNAME_NOT_EXIST['msg']
                return render(request, 'login_error.html', data)  #用户名不存在


def hello(request):
    """
    后台页面
    :param request:
    :return: 返回后台页面
    """
    if request.method == 'GET':
        return render(request, 'backend.html')


def refresh(request):
    """
    更新
    :param request:
    :return: 前端ajax在页面加载完毕后向本函数发出请求, 本函数将响应数据返回给前端.
    """
    if request.method == 'GET':
        cookies = request.COOKIES.get('ticket')
        if cookies and User.objects.filter(ticket=cookies).exists():
            user = User.objects.get(ticket=cookies)
            data = SUCCESS
            data['user_id'] = user.user_id
            data['account'] = user.account
            data['phone'] = user.phone
            data['nick_name'] = user.nick_name
            data['avatar'] = user.avatar

        else:
            data = SYSTEM_INSTUSION

        return JsonResponse(data)


def update_pwd(request):
    """
    修改密码
    :param request:
    :return: 1.GET:返回修改密码页面
             2.POST: 前端ajax请求后返回响应数据给前端进行处理
    """
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
    """
    房屋管理
    :param request:
    :param the_page: 当前页面
    :return: 返回房屋管理页面(当前页码)
    """
    if request.method == 'GET':
        positions = Area.objects.all()
        house_types = HouseType.objects.all()
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
    """
    系统概况
    :param request:
    :return: 返回系统概况页面
    """
    if request.method == 'GET':
        return render(request, 'system_overview.html')


def del_house(request, house_id, the_page):
    """
    Manage_house页面下删除房屋数据, 通过前端传参删除, 在后端执行跳转操作
    :param request:
    :param house_id: 房屋编号
    :param the_page: 当前页面
    :return: 删除后返回当前页面并刷新
    """
    if request.method == 'GET':
        # 1. 删除房屋详情
        HouseDetail.objects.filter(house_id=house_id).delete()
        # 2. 删除房屋对应设备关联数据
        sql = 'delete from house_facility where house_id=%d' % (int(house_id))
        cursor.execute(sql)
        # 3. 删除房屋图片
        HouseImg.objects.filter(house_id=house_id).delete()
        # 4. 删除用户收藏对应关联数据
        sql1 = 'delete from collect where house_id=%d' % (int(house_id))
        cursor.execute(sql1)
        # 5. 删除统计表中数据, 并提交sql语句
        Count.objects.filter(house_id=house_id).delete()
        client.commit()
        # 6. 最后, 删除房屋表数据
        House.objects.filter(house_id=house_id).delete()

        return HttpResponseRedirect('/app/house_manage/' + the_page + '/')


def del_house1(request, house_id):
    """
    Search页面下删除房屋数据, 通过前端发出删除数据消息并且前端ajax发出刷新页面操作
    :param request:
    :param house_id: 房屋编号
    :param the_page: 当前页面
    :return: 返回json格式数据(成功)
    """
    if request.method == 'GET':
        # 1. 删除房屋详情
        HouseDetail.objects.filter(house_id=house_id).delete()
        # 2. 删除房屋对应设备关联数据
        sql = 'delete from house_facility where house_id=%d' % (int(house_id))
        cursor.execute(sql)
        # 3. 删除房屋图片
        HouseImg.objects.filter(house_id=house_id).delete()
        # 4. 删除用户收藏对应关联数据
        sql1 = 'delete from collect where house_id=%d' % (int(house_id))
        cursor.execute(sql1)
        # 5. 删除统计表中数据, 并提交sql语句
        Count.objects.filter(house_id=house_id).delete()
        client.commit()
        # 6. 最后, 删除房屋表数据
        House.objects.filter(house_id=house_id).delete()

        return JsonResponse(SUCCESS)


def edit_house(request, house_id, the_page):
    """
    编辑房屋信息
    :param request:
    :param house_id: 房屋编号
    :param the_page: 当前页面
    :return: 1.GET:弹出子页面(表单页面)
             2.POST:关闭弹出框,提交请求后返回到当前页并刷新
    """
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
        # 以上为房屋信息编辑提交
        house_detail = HouseDetail.objects.get(house_id=house_id)
        house_detail.lease = lease
        house_detail.save()
        # 以上为房屋细节信息编辑提交
        user = User.objects.get(user_id=house.user_id)
        user.nick_name = nick_name
        user.phone = phone
        user.save()
        # 以上为用户信息编辑提交


def search(request, area_id, price_range, acreage_range, house_type, the_page):
    """
    条件查询(区别与上面页面管理)
    :param request:
    :param area_id:
    :param price_range:
    :param acreage_range:
    :param house_type:
    :param the_page:
    :return:

    注意: 从url传过来的参数拿到的收拾字符串, 字符串都是真, 所以必须进行int操作
    """
    if request.method == 'GET':
        all_house = House.objects.all()

        house1 = all_house.filter(area_id=area_id) if int(area_id) else all_house

        price_min = int(price_range.split('_')[0])
        if len(price_range) != 1:
            price_max = int(price_range.split('_')[1])
        else:
            price_range = int(price_range)
            price_max = price_min
        house2 = house1 if not price_range else house1.filter(price__gte=price_min, price__lt=price_max)

        acreage_min = int(acreage_range.split('_')[0])
        if len(acreage_range) != 1:
            acreage_max = int(acreage_range.split('_')[1])
        else:
            acreage_range = int(acreage_range)
            acreage_max = acreage_min
        house3 = house2.filter(acreage__gte=acreage_min, acreage__lt=acreage_max) if acreage_range else house2

        if int(house_type.split('室')[0]):
            house_type = parse.unquote(house_type)
            types = HouseType.objects.filter(type_name__startswith=house_type)
            type_ids = [i.type_id for i in types]
            house4 = house3.filter(type_id__in=type_ids)
        else:
            house4 = house3

        positions = Area.objects.all()
        house_types = HouseType.objects.all()
        t = []
        for i in house_types:
            t.append(i.type_name[:2])
        new_type = list(set(t))
        new_type.sort()
        the_page = int(the_page)
        page_size = 10
        pre_page = the_page - 1
        all_record = house4.all().count()
        total_page = (house4.all().count() // page_size) if (house4.all().count() % 10 == 0) else (
                house4.all().count() // page_size + 1)
        houses = house4.all()[pre_page * page_size: the_page * page_size]

        return render(request, 'search.html',
                      {'positions':positions,
                       'new_type':new_type,
                       'houses':houses,
                       'the_page':the_page,
                       'total_page':total_page,
                       'all_record':all_record,
                       'area_id':area_id,
                       'price_range':price_range,
                       'acreage_range':acreage_range,
                       'house_type':house_type})

