from PIL import Image
from django.contrib.auth.hashers import check_password, make_password

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from app.models import House, User, Collect, HouseDetail, HouseFacility, HouseImg, Area, HouseType



# 写入取session方法
def Get_user(a):
    user = a.session.get('account')
    user_id = User.objects.filter(account=user).first()
    print('user_id')
    print(user_id)
    return user_id

# 首页
def Index(request):
    if request.method == 'GET':
        # 获取数据库中房屋信息
        house = House.objects.order_by('-house_id')[:5]
        user = Get_user(request)
        return render(request, 'cwd/index.html', {'hous': house, 'user': user})


# 个人中心(同时能修改昵称和头像)
def My_self(request):
    # 获取登录者信息
    user_id = Get_user(request)
    if request.method == 'GET':
        # 是否登录
        if user_id:
            # 如果登录才能到个人中心页面

            return render(request, 'cwd/page.html', {'user': user_id})
        else:
            # 返回主界面
            return HttpResponseRedirect('/kaiapp/login/')
            # 返回没有用户的json格式
            # return JsonResponse(jsonresponse.NO_USER)
    if request.method == 'POST':
        nick_name = request.POST.get('nick_name')
        img_url = request.FILES.get('avatar')
        img = Image.open(img_url)
        img.save('media/%s' % img_url)
        im_url = '/media/' + str(img_url)
        User.objects.filter(user_id=user_id.user_id).update(nick_name=nick_name, avatar=im_url)
        return HttpResponseRedirect('/cwd/myself/')


# 修改密码界面
def Change_password(request):
    # 获取登录者信息
    user_id = Get_user(request)
    if request.method == 'GET':

        # 是否登录
        if user_id:
            # 如果登录才能到个人中心页面
            return render(request, 'cwd/pass.html', {'user': user_id})
    if request.method == 'POST':
        old_pass = request.POST.get('mpass')
        new_pass = request.POST.get('newpass')
        rnew_pass = request.POST.get('renewpass')
        if all([old_pass, new_pass, rnew_pass]):
            if check_password(old_pass, user_id.password):
                if new_pass == rnew_pass:
                    password = make_password(new_pass)
                    User.objects.filter(user_id=user_id.user_id).update(password=password)
                    return HttpResponseRedirect('/cwd/myself/')
                else:
                    return HttpResponse('两次密码不一致')
            else:
                return HttpResponse('原密码错误')
        else:
            return HttpResponse('信息输入不完整')


# 我的关注界面
def I_like(request):
    user = Get_user(request)
    if request.method == 'GET':
        if user:
            house = User.objects.get(user_id=user.user_id).col_house.all()
            return render(request, 'cwd/adv.html', {'house': house, 'user': user})
        else:
            return HttpResponseRedirect('/cwd/index/')


# 删除页面
def Del(request):
    if request.method == 'GET':
        house_id = request.GET.get('adv')
        # 删除关注页面
        if house_id:
            Collect.objects.filter(house_id=house_id).delete()
            return JsonResponse({'code': 200, 'msg': '已删除关注房源'})
        houses = request.GET.get('myhouse')
        # 删除发布房屋
        if houses:
            HouseDetail.objects.filter(house_id=houses).delete()
            HouseFacility.objects.filter(house_id=houses).delete()
            HouseImg.objects.filter(house_id=houses).delete()
            House.objects.filter(house_id=houses).delete()
            return JsonResponse({'code': 200, 'msg': '已删除发布房源'})


# 实名认证
def Ture_name(request):
    user = Get_user(request)
    if request.method == 'GET':
        if user:
            return render(request, 'cwd/ture.html', {'user': user})
        else:
            return HttpResponse('/cwd/index/')

    if request.method == 'POST':
        id_name = request.POST.get('id_name')
        id_card = request.POST.get('id_card')
        if all([id_name, id_card]):
            # 返回json消息
            # return JsonResponse(jsonresponse.NO_THING)
            # 网络上找的验证身份证号码
            # if not re.match(r'^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$',id_card)
            if len(id_card) == 18:
                User.objects.filter(user_id=user.user_id).update(id_name=id_name, id_card=id_card)
                return HttpResponseRedirect('/cwd/myself/')
            else:
                # return JsonResponse(jsonresponse.ID_LEN_ERROR)
                return HttpResponse('身份证号码不正确')

        else:
            return HttpResponse('请将信息输入完整')


# 我发布的房源
def My_house(request):
    user = Get_user(request)
    if user:
        if request.method == 'GET':
            house = House.objects.filter(user_id=user.user_id)
            # return render(request, 'cwd/my_house.html', {'house': house, 'user': user})
            return render(request, 'xym/showHouse.html', {'house':house, 'user':user})


# 默认查询页面
def Find(request, the_page):
    if request.method == 'GET':
        # 获取地区
        positions = Area.objects.all()
        # 获取房屋类型钱4个字段（如：两室一厅）
        house_types = HouseType.objects.all()
        t = []
        for i in house_types:
            t.append(i.type_name[:4])
        # 添加t标签并且去重排序
        new_type = list(set(t))
        new_type.sort()
        # 获取页面页数并且改为整数类型
        the_page = int(the_page)
        # 设定每页显示数量
        page_size = 10
        # 减一的话可以根据页面传递的当前页面参数来传递每页不同的房屋详情（下面的计算用得着↓）
        pre_page = the_page - 1
        # 获取一共有多少条数据
        all_record = House.objects.all().count()
        # 获取总页数，如果能能整除10的话否则整除11
        total_page = (House.objects.all().count() // page_size) if (House.objects.all().count() % 10 == 0) else (
                House.objects.all().count() // page_size + 1)
        # 获取每页的十条页面信息，根据传递的翻页参数来定（这个地方就用到了↑）比如第一页[0:10]第二页[2-1*10:2*10]
        houses = House.objects.all()[pre_page * page_size: the_page * page_size]

        return render(request, 'cwd/find.html',
                      {'positions': positions,  # 地区详情
                       'new_type': new_type,  # 类型详情
                       'houses': houses,  # 房屋详情十条
                       'the_page': the_page,  # 当前页面
                       'total_page': total_page,  # 总页面
                       'all_record': all_record})  # 一共多少条


# 查询页面
def Search(request, a, p, s, n):
    if request.method == 'GET':
        house = House.objects.all()
        if int(a) != 0:
            house = house.filter(area_id=a)
        else:
            house = house

        if p != '0':
            price_min = int(p.split('-')[0])
            price_max = int(p.split('-')[1])
            house = house.filter(price__gte=price_min, price__lt=price_max)
        else:
            house = house

        if s != '0':
            types = HouseType.objects.filter(type_name__startswith=s)  # 字段__startswith = value：该字段以value开头的
            type_ids = [i.type_id for i in types]
            house = house.filter(type_id__in=type_ids)
        else:
            house = house
        # 获取地区
        positions = Area.objects.all()
        # 获取房屋类型钱4个字段（如：两室一厅）
        house_types = HouseType.objects.all()
        t = []
        for i in house_types:
            t.append(i.type_name[:4])
        # 添加t标签并且去重排序
        new_type = list(set(t))
        new_type.sort()
        # 获取页面页数并且改为整数类型
        the_page = int(n)
        # 设定每页显示数量
        page_size = 10
        # 减一的话可以根据页面传递的当前页面参数来传递每页不同的房屋详情（下面的计算用得着↓）
        pre_page = the_page - 1
        # 获取一共有多少条数据
        all_record = house.all().count()
        # 获取总页数，如果能能整除10的话否则整除11
        total_page = (house.all().count() // page_size) if (house.all().count() % 10 == 0) else (
                house.all().count() // page_size + 1)
        # 获取每页的十条页面信息，根据传递的翻页参数来定（这个地方就用到了↑）比如第一页[0:10]第二页[2-1*10:2*10]
        houses = house.all()[pre_page * page_size: the_page * page_size]
        return render(request, 'cwd/search.html',
                      {'positions': positions,  # 地区详情
                       'new_type': new_type,  # 类型详情
                       'houses': houses,  # 房屋详情十条
                       'the_page': the_page,  # 当前页面
                       'total_page': total_page,  # 总页面
                       'all_record': all_record})  # 一共多少条
