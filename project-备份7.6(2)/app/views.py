import os

from django.contrib.auth import authenticate
from django.contrib.auth.backends import UserModel
from django.contrib.auth.hashers import check_password
from django.contrib.sites import requests
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.


# def hello(request):
#     if request.method == 'GET':
#         return render(request, 'test.html')
# 首页
from django.views.decorators.csrf import csrf_exempt

from app.models import Facility, Area, HouseType, House, User, HouseDetail, HouseImg, HouseFacility


def my_home(request):
    if request.method == 'GET':
        return render(request, 'index.html')


# 登陆页面

# 用户登录
def login(request):
    # get请求获取登录页面
    if request.method == 'GET':
        return render(request, 'login.html')

    # post请求获取信息
    if request.method == 'POST':
        account = request.POST.get('account')
        password = request.POST.get('password')

        # 判断账号是否存在
        if User.objects.filter(account=account).exists():
            users = User.objects.filter(account=account)  # 获取的是列表类型

            # 检查密码
            if check_password(password, users[0].password):

                # 将登录的账户名传递给session对象
                request.session['account'] = account

                return HttpResponseRedirect('app:index')
                # return render(request,'index.html',data)

            else:
                return HttpResponse('登录密码错误')
        else:
            return HttpResponse('登录账号错误')


# 注册
def my_register(requst):
    if requst.method == 'GET':
        return render(requst, 'register.html')


# # 上传新房源,做用户认证
# @csrf_exempt
# def my_new_house(request):
#
#     if request.method == 'GET':
#         if 'account' in request.session:
#             area = Area.objects.all()
#             facility_name = Facility.objects.all()
#             facility_id = Facility.objects.all
#             type_names = HouseType.objects.all()
#             data = {
#                 'area': area,
#                 'facility_name': facility_name,
#                 'type_names': type_names,
#                 'facility_id':facility_id
#             }
#             return render(request, 'newhouse.html', data)
#         else:
#             return HttpResponse('请先登录！')
#
#     if request.method == 'POST':
#
#         if 'account' in request.session:
#             # 查找当前用户
#             # user = request.user
#             data = {
#                 'msg': '请求成功',
#                 'code': 200
#             }
#             user = request.session.get['account']
#             user_id = UserModel.objects.filter(acount=user).first()
#
#             title = request.POST.get('title')
#             # 价格
#             price = request.POST.get('price')
#             # 支付方式
#             pay_way = request.POST.get('pay_way')
#             print(pay_way)
#             # 租赁方式
#             lease = request.POST.get('lease')
#             # 区域
#             area = request.POST.get('area')
#             area_id = 1  # area.area_id
#             # 地址
#             address = request.POST.get('address')
#             # 面积
#             acreage = request.POST.get('acreage')
#             # 房型
#             type = request.POST.get('type')
#             type_id = 1  # type.type_id
#             # 楼层
#             floor = request.POST.get('floor')
#             # 朝向
#             house_head = request.POST.get('house_head')
#             # 小区名
#             community = request.POST.get('community')
#             # 周围设施
#             surround_facility = request.POST.get('surround_facility')
#             # 交通
#             transportation = request.POST.get('transportation')
#             # 获取House数据
#             # house_form = House(data=request.POST)
#             # 房屋图片
#             index_img_url = request.FILES.get('house_image')
#             facility_name = request.POST.getlist('facility_name')  # get name from html
#             print('test')
#             print(facility_name)
#             facility = Facility.objects.filter(facility_name=facility_name).first()  # search database for name to get object
#             facility_id = 1  # get id from object that we find
#
#             user_id = 1
#             house = House.objects.create(
#                 user_id=user_id,
#                 area_id=area_id,
#                 type_id=type_id,
#                 title=title,
#                 price=price,
#                 address=address,
#                 acreage=acreage,
#                 index_img_url=index_img_url
#
#             )
#             my_house = request.POST.get('house_id')
#             house_id = House.objects.filter(house_id=my_house).first()
#             house_detail = HouseDetail.objects.create(
#                 house_id=house_id,
#                 lease=lease,
#                 pay_way=pay_way,
#                 floor=floor,
#                 house_head=house_head,
#                 community=community,
#                 surround_facility=surround_facility,
#                 transportation=transportation
#
#             )
#             # img = HouseImg.objects.create(
#             #     house_id=house_id,
#             #     index_img_url=index_img_url
#             #
#             # )
#             facility = HouseFacility.objects.create(
#
#                 house_id=house_id,
#                 facility_id=facility_id
#             )
#
#         return JsonResponse(data)
#     else:
#         return render(request, 'login.html')

# 上传新房源,没做认证
@csrf_exempt
def my_new_house(request):

    if request.method == 'GET':
        print('1***************88888')

        area = Area.objects.all()
        facility_name = Facility.objects.all()
        facility_id = Facility.objects.all
        type_names = HouseType.objects.all()
        data = {
            'area': area,
            'facility_name': facility_name,
            'type_names': type_names,
            'facility_id':facility_id
        }
        return render(request, 'newhouse.html', data)

    if request.method == 'POST':


        # 查找当前用户
        # user = request.user
        data = {
            'msg': '请求成功',
            'code': 200
        }
        user = request.session.get['account']
        user_id = UserModel.objects.filter(acount=user).first()

        title = request.POST.get('title')
        # 价格
        price = request.POST.get('price')
        # 支付方式
        pay_way = request.POST.get('pay_way')
        print(pay_way)
        # 租赁方式
        lease = request.POST.get('lease')
        # 区域
        area = request.POST.get('area')
        area_id = 1  # area.area_id
        # 地址
        address = request.POST.get('address')
        # 面积
        acreage = request.POST.get('acreage')
        # 房型
        type = request.POST.get('type')
        type_id = 1  # type.type_id
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
        index_img_url = request.FILES.get('house_image')
        facility_name = request.POST.getlist('facility_name')  # get name from html
        print('test')
        print(facility_name)
        facility = Facility.objects.filter(facility_name=facility_name).first()  # search database for name to get object
        facility_id = 1  # get id from object that we find
        print('2***************88888')
        print(facility)

        user_id = 1
        house = House.objects.create(
            user_id=user_id,
            area_id=area_id,
            type_id=type_id,
            title=title,
            price=price,
            address=address,
            acreage=acreage,
            index_img_url=index_img_url

        )
        my_house = request.POST.get('house_id')
        house_id = House.objects.filter(house_id=my_house).first()
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
        # img = HouseImg.objects.create(
        #     house_id=house_id,
        #     index_img_url=index_img_url
        #
        # )
        facility = HouseFacility.objects.create(

            house_id=house_id,
            facility_id=facility_id
        )

    return JsonResponse(data)




