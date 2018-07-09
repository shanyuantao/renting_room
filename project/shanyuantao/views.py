import re

from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from django.shortcuts import render

from django.core.urlresolvers import reverse

from shanyuantao.models import User, Area, Facility, House, HouseType, HousePrice, Acreage

from django.db.models import Q

# 注册页面
def regist(request):

    return render(request, 'regist.html')


# 注册提交页面
def regist_post(request):

    if request.method == 'POST':

        account = request.POST.get('account')
        password = request.POST.get('password')
        nickname = request.POST.get('nickname')
        phone = request.POST.get('phone')
        avatar = request.FILES.get('avatar')

        if not all([account, password, nickname, phone, avatar]):

            return HttpResponse('信息填写不全')

        if not re.match(r'1[24578]\d{9}', phone):

            return HttpResponse('手机号码不符合规则')

        if User.objects.filter(phone=phone).first():

            return HttpResponse('该手机号已注册')

        User.objects.create(account=account, password=password,
                            nickname=nickname, phone=phone, avatar=avatar)

        return HttpResponseRedirect(reverse('shan:login'))


# 登录页面
def login(request):

    return render(request, 'login.html')


# 登录提交页面
def login_post(request):

    if request.method == 'POST':

       pass


# 区域
def area(request):

    areas = Area.objects.all()

    area_list = []

    area_dict = {
        'msg': '请求成功',
        'code': '200'
    }

    for area in areas:

        a_dict = {'id': area.area_id, 'name': area.name}

        area_list.append(a_dict)

    area_dict["area_list"] = area_list

    return JsonResponse(area_dict)


# 设施
def facilities(request):

    facilities = Facility.objects.all()

    fac_list = []

    fac_dict = {

        'msg': '请求成功',
        'code': '200'
    }

    for facility in facilities:

        f_dict = {'id': facility.facility_id, 'name': facility.facility_name, 'css': facility.css}

        fac_list.append(f_dict)

    fac_dict["fac_list"] = fac_list

    return JsonResponse(fac_dict)


# 房子类型
def type_house(request):

    house_types = HouseType.objects.all()

    type_list = []

    type_dict = {

        'msg': '请求成功',
        'code': '200'
    }

    for house_type in house_types:

        t_dict = {'id': house_type.type_id, 'name': house_type.type_name}

        type_list.append(t_dict)

    type_dict["type_list"] = type_list

    return JsonResponse(type_dict)






# 区域查询
def area_query_house(request, area_id):

    area = Area.objects.get(area_id=area_id)

    houses = area.house_set.all()

    house_list = []

    house_dict = {
        'msg': '请求成功',
        'code': '200',
    }

    for house in houses:

        house_type = house.type
        typename = house_type.type_name

        count_list = house.count_set.all()
        count = count_list[0].look_times if count_list else '0'

        h_dict = {
            'house_id': house.house_id,
            'house_type': typename,
            'house_title': house.title,
            'house_price': house.price,
            'house_address': house.address,
            'house_acreage': house.acreage,
            'house_index_img_url': house.index_img_url,
            'house_count': count

        }

        house_list.append(h_dict)

    house_dict["area_list"] = house_list

    return JsonResponse(house_dict)


# 价格查询房子
def price_query_house(request, price1, price2):

    houses = House.objects.filter(price__gt=price1, price__lt=price2)

    house_list = []

    house_dict = {
        'msg': '请求成功',
        'code': '200',
    }

    for house in houses:
        house_type = house.type
        typename = house_type.type_name

        count_list = house.count_set.all()
        count = count_list[0].look_times if count_list else '0'

        h_dict = {
            'house_id': house.house_id,
            'house_type': typename,
            'house_title': house.title,
            'house_price': house.price,
            'house_address': house.address,
            'house_acreage': house.acreage,
            'house_index_img_url': house.index_img_url,
            'house_count': count

        }

        house_list.append(h_dict)

    house_dict["price_list"] = house_list

    return JsonResponse(house_dict)


# 面积查询房子
def acreage_query_house(request, acr1, acr2):

    houses = House.objects.filter(acreage__gt=acr1, acreage__lt=acr2)

    house_list = []

    house_dict = {
        'msg': '请求成功',
        'code': '200',
    }

    for house in houses:
        house_type = house.type
        typename = house_type.type_name

        count_list = house.count_set.all()
        count = count_list[0].look_times if count_list else '0'

        h_dict = {
            'house_id': house.house_id,
            'house_type': typename,
            'house_title': house.title,
            'house_price': house.price,
            'house_address': house.address,
            'house_acreage': house.acreage,
            'house_index_img_url': house.index_img_url,
            'house_count': count

        }

        house_list.append(h_dict)

    house_dict["acreage_list"] = house_list

    return JsonResponse(house_dict)


# 房型查询房子
def type_query_house(request, typeid):

    houses = House.objects.filter(type_id=typeid)
    house_list = []

    house_dict = {
        'msg': '请求成功',
        'code': '200',
    }

    for house in houses:
        house_type = house.type
        typename = house_type.type_name

        count_list = house.count_set.all()
        count = count_list[0].look_times if count_list else '0'

        h_dict = {
            'house_id': house.house_id,
            'house_type': typename,
            'house_title': house.title,
            'house_price': house.price,
            'house_address': house.address,
            'house_acreage': house.acreage,
            'house_index_img_url': house.index_img_url,
            'house_count': count

        }

        house_list.append(h_dict)

    house_dict["type_list"] = house_list

    return JsonResponse(house_dict)


def invest_jump(request):

    return HttpResponseRedirect(reverse('shan:myinvest', args=('0', '0', '0', '0')))


# 展示invest.html页面
def invest_html(request, area_id, price_id, acreage_id, house_type_id):

    if area_id == 0 and price_id == 0 and acreage_id == 0 and house_type_id == 0:
        houses = House.objects.all()

    else:
        q1 = Q()
        q1.connector = 'AND'

        if int(area_id) != 0:
            q1.children.append(('area', area_id))
        if int(price_id) != 0:
            q1.children.append(('price', price_id))
        if int(acreage_id) != 0:
            q1.children.append(('acreage', acreage_id))
        if int(house_type_id) != 0:
            q1.children.append(('type', house_type_id))

        houses = House.objects.filter(q1).order_by('house_id')

    # 分成三页
    paginator = Paginator(houses, 4)
    # 获取链接的页码
    current_page = request.GET.get('current_page', 1)
    # 指定要访问的页码的内容
    page_data = paginator.page(current_page)

    areas = Area.objects.all()
    house_types = HouseType.objects.all()
    house_prices = HousePrice.objects.all()
    house_acreages = Acreage.objects.all()

    data = {}

    data['areas'] = areas
    data['house_types'] = house_types
    data['house_prices'] = house_prices
    data['house_acreages'] = house_acreages

    data['area_id'] = area_id
    data['price_id'] = price_id
    data['acreage_id'] = acreage_id
    data['house_type_id'] = house_type_id
    data['page_data'] = page_data

    return render(request, 'invest.html', data)










