import os

from django.contrib.auth import authenticate
from django.contrib.auth.backends import UserModel
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.sites import requests
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from app.models import Facility, Area, HouseType, House, User, HouseDetail, HouseImg, HouseFacility


# 用户登录
def login(request):
    if request.method == 'GET':
        return render(request, 'xym/login.html')

    # post请求获取信息
    if request.method == 'POST':
        username = request.POST.get('account')
        password = request.POST.get('password')

        if User.objects.filter(account=username).exists():
            users = User.objects.filter(account=username)

            # if check_password(password, users[0].password):
            if password == users[0].password:

                # 将登录的账户名传递给session对象
                request.session['account'] = username

                return HttpResponseRedirect('/xym/index.html')
            else:  # wrong password
                return HttpResponse('登录密码错误')
        else:  # wrong user
            return HttpResponse('登录账号错误')


# 上传新房源
@csrf_exempt
def my_new_house(request):
    username = request.session.get('account')
    users = User.objects.filter(account=username)
    user_id = users[0].user_id

    if request.method == 'GET':
        area = Area.objects.all()
        facility_name = Facility.objects.all()
        facilitys_id = Facility.objects.all
        type_names = HouseType.objects.all()
        data = {
            'area': area,
            'facility_name': facility_name,
            'type_names': type_names,
            'facility_id': facilitys_id
        }
        if user_id:
            # if the user is login
            return render(request, 'xym/newhouse.html', data)
        else:
            # if not login return to login page
            return render(request, 'xym/login.html')

    if request.method == 'POST':

        title = request.POST.get('title')
        # 价格
        price = request.POST.get('price')

        # 支付方式
        pay_way = request.POST.get('pay_way')

        # 租赁方式
        lease = request.POST.get('lease')
        # 区域
        area_id = request.POST.get('area_id')  # this is the name as in html under name=

        # 地址
        address = request.POST.get('address')
        # 面积
        acreage = request.POST.get('acreage')
        # 房型
        type = request.POST.get('type')
        type_id = 1

        # 楼层
        floor = request.POST.get('floor')
        # 朝向
        house_head = request.POST.get('house_head')
        # 小区名
        community = request.POST.get('community')
        # 周围设施
        surround_facility = request.POST.get('surround_facility')
        # 交通
        transportation = request.POST.get('transportation')
        # 获取House数据
        # house_form = House(data=request.POST)
        # 房屋图片
        img_file = request.FILES.get('house_image')
        # use the FileSystemStorage() function
        fs = FileSystemStorage()
        filename = fs.save(img_file.name, img_file)
        index_img_url = fs.url(filename)

        facilitys_id = request.POST.getlist('facilitys')  # get name from html

        # 房屋状态
        house_status = request.POST.get('house_statuss')

        # insert into the databases
        house = House.objects.create(
            # this creates new house in table, house id is automatically created for this object
            user_id=user_id,
            area_id=area_id,
            type_id=type_id,
            title=title,
            price=price,
            address=address,
            acreage=acreage,
            index_img_url=index_img_url,
            house_status=house_status

        )
        house_id = house.house_id
        house_detail = HouseDetail.objects.create(
            house_id=house_id,
            lease=lease,
            pay_way=pay_way,
            floor=floor,
            house_head=house_head,
            community=community,
            surround_facility=surround_facility,
            transportation=transportation

        )
        url = house.index_img_url
        img = HouseImg.objects.create(
            house_id=house_id,
            url=url

        )

        # for loop over facility_id to add lines to facility database
        for facility_id in facilitys_id:
            facility = HouseFacility.objects.create(

                house_id=house_id,
                facility_id=facility_id
            )

        return render(request, 'xym/success.html')




def show_success(request):
    if request.method == 'GET':
        return render(request, 'xym/success.html')
