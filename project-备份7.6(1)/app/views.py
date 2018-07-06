from django.contrib.auth.backends import UserModel
from django.http import JsonResponse
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
def my_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')


# 注册
def my_register(requst):
    if requst.method == 'GET':
        return render(requst, 'register.html')


# 上传新房源
@csrf_exempt
def my_new_house(request):
    load_new_house = False
    if request.method == 'GET':
        area = Area.objects.all()
        facility_name = Facility.objects.all()
        type_names = HouseType.objects.all()
        data = {
            'area': area,
            'facility_name': facility_name,
            'type_names': type_names
        }
        return render(request, 'newhouse.html', data)

    if request.method == 'POST':
        print('1%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        # 查找当前用户
        # user = request.user
        print('2%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        data = {
            'msg': '请求成功',
            'code': 200
        }
        # if user.id:
        #     user_id = user.id
        # 标题
        # print('user_id'%user_id)

        title = request.POST.get('title')
        # 价格
        price = request.POST.get('price')
        # 支付方式
        pay_way = request.POST.get('pay_way')
        # 租赁方式
        lease = request.POST.get('lease')
        # 区域
        area = request.POST.get('area')
        area_id =1 #area.area_id
        # 地址
        address = request.POST.get('address')
        # 面积
        acreage = request.POST.get('acreage')
        # 房型
        type = request.POST.get('type')
        type_id =1 #type.type_id
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
        # 房屋图片
        index_img_url = request.FILES.get('house_image')
        print(index_img_url)
        # 将获取到的图片信息插入到数据库中
        house = House.objects.create(
            index_img_url=index_img_url
        )

        facilityname = request.POST.get('facility_name')  # get name from html
        facility = Facility.objects.filter(facility_name=facilityname).first()  # search database for name to get object
        facility_id = 1 # get id from object that we find

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
    else:
        return render(request, 'login.html')

    # house_id = models.AutoField(primary_key=True)
    # user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    # area = models.ForeignKey(Area, models.DO_NOTHING, blank=True, null=True)
    # type = models.ForeignKey('HouseType', models.DO_NOTHING, blank=True, null=True)
    # title = models.CharField(max_length=1024, blank=True, null=True)
    # price = models.IntegerField(blank=True, null=True)
    # address = models.CharField(max_length=512, blank=True, null=True)
    # acreage = models.IntegerField(blank=True, null=True)
    # index_img_url = models.CharField(max_length=1024, blank=True, null=True)
    # mainwheels = MainWheel.objects.all()
# 初始化是否已将上传该房源为false


def load_image(request):
    if request.method == 'GET':
        return render(request, 'picture.html')
