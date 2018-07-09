import os

from django.contrib.auth import authenticate
from django.contrib.auth.backends import UserModel
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.sites import requests
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.


# def hello(request):
#     if request.method == 'GET':
#         return render(request, 'test.html')
# 首页
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from app.models import Facility, Area, HouseType, House, User, HouseDetail, HouseImg, HouseFacility


# 用户登录
def login(request):
    # get请求获取登录页面
    if request.method == 'GET':
        return render(request, 'xym/login.html')

    # post请求获取信息
    if request.method == 'POST':
        username = request.POST.get('account')  # because is name='account' in html
        password = request.POST.get('password')
        #just print to check the account and password you get
        print(username)
        print(password)

        # 判断账号是否存在
        #search from the mysql if the username is exist
        if User.objects.filter(account=username).exists():  # chec kif the user exist
            users = User.objects.filter(account=username)  # 获取的是列表类型 # get row from database, index 0 because 1 result
            print('users:')
            print(users)
            # 检查密码
            # if check_password(password, users[0].password): # check the hashed password of the user
            if password == users[0].password:

                # 将登录的账户名传递给session对象

                request.session['account'] = username  # store user into session after login
                # request.session['yanmei_data']=123
                # request.session['user_id'] = users[0].user_id
                # session is server side database
                return HttpResponseRedirect('/xym/index.html')
            else:  # wrong password
                return HttpResponse('登录密码错误')
        else:  # wrong user
            return HttpResponse('登录账号错误')


# 上传新房源
@csrf_exempt
def my_new_house(request):
    # yanmei=request.session.get('yanmei_data') # yanmei will be equal to 123 now

    # OPTION A
    # this is different website, we want to get session
    # find who is login now
    username = request.session.get('account')  # get username from session, we need to login first !!!
    # after session we check database for user_id for username
    users = User.objects.filter(account=username)  # search database,  get users from database with username user
    user_id = users[0].user_id  # we get user_id from first one (row 0, always 0)
    print('user_id:')
    print(user_id)

    # OPTION B

    # another way to get user id (faster, no database)
    # user_id = request.session.get('user_id') # after login

    if request.method == 'GET': # here we send data to html
        #get all the area from mysql
        area = Area.objects.all()
        facility_name = Facility.objects.all()
        facilitys_id = Facility.objects.all
        type_names = HouseType.objects.all()
        data = { # the data html use to display: area, facility
            'area': area,
            'facility_name': facility_name,
            'type_names': type_names,
            'facility_id': facilitys_id
        }
        if user_id:
            #if the user is login
            return render(request, 'xym/newhouse.html', data)
        else:
            #if not login return to login page
            return render(request, 'xym/login.html')

    if request.method == 'POST': # here we get the data from form html (name=)
        # data = {
        #     'msg': '请求成功',
        #     'code': 200
        # }

        title = request.POST.get('title')
        # 价格
        price = request.POST.get('price')
        print('price')
        print(price)
        # 支付方式
        pay_way = request.POST.get('pay_way')
        print('支付')
        print(pay_way)
        # 租赁方式
        lease = request.POST.get('lease')
        # 区域
        area_id = request.POST.get('area_id')  # this is the name as in html under name=
        print('area')
        print(area_id)
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
        img_file = request.FILES.get('house_image')
        #use the FileSystemStorage() function
        fs = FileSystemStorage()
        filename = fs.save(img_file.name, img_file)
        index_img_url=fs.url(filename)
        print('image')
        print(index_img_url)


        facilitys_id = request.POST.getlist('facilitys')  # get name from html
        print('facility_id')
        print(facilitys_id)

         # search database for name to get object
         # get id from object that we find


        #房屋状态
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
        house_id = house.house_id  # we get the house id from the new object

        # my_house = request.POST.get('house_id')
        # house_id = House.objects.filter(house_id=my_house).first()
        house_detail = HouseDetail.objects.create(
            # another table ,is not house table, the house detail need house id  to connect
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

        #for loop over facility_id to add lines to facility database
        for facility_id in facilitys_id:
            facility = HouseFacility.objects.create(

                house_id=house_id,
                ## database column name = your name
                facility_id=facility_id
            )

        #return JsonResponse(data)
        return render(request,'xym/success.html')



#添加新房源后展示
def show_newhouse(request):
    # get user from session. after he login
    # get house  from database for the user
    #send user  and house  to my—house.html—
    users = request.session.get('account')
    user = User.objects.filter(account=users)
    user_id = user[0].user_id

    #find the house information vy user_id
    house = House.objects.filter(user_id=user_id)
    data = {
        'user':user,
        'house':house
    }
    if user:
        if request.method == 'GET':
            return render(request, 'xym/showHouse.html', data)
    else:
        return render(request,'xym/login.html')



def show_success(request):

    if request.method == 'GET':
        return render(request,'xym/success.html')

#删除新增的房源
@csrf_exempt
def remove_newhouse(request):
    if request.method == 'GET':
        return render(request,'xym/showHouse.html')

    if request.method == 'POST':
        houses = request.POST.get('house_id')
        print(houses)
        HouseDetail.objects.filter(house_id=houses).delete() # remove the house from table, where house_id is foreign key
        HouseFacility.objects.filter(house_id=houses).delete() # remove the house from table, where house_id is foreign key
        HouseImg.objects.filter(house_id=houses).delete() # remove the house from table, where house_id is foreign key
        House.objects.filter(house_id=houses).delete() # at last we remove the house from main table, where house_id is MAIN key
        return render(request,'xym/showHouse.html')
