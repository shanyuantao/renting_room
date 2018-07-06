import os
import re

from django.contrib.auth.hashers import check_password, make_password
from django.core.files.base import ContentFile

from project import settings
from django.core.files.storage import default_storage
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from app.models import House, User
from app import jsonresponse


# 写入取session方法
def Get_user(a):
    user = a.session.get('account')
    user_id = User.objects.filter(account=user).first()
    return user_id


# 首页
def Index(request):
    if request.method == 'GET':
        # 获取数据库中房屋信息
        house = House.objects.all()
        return render(request, 'cwd/index.html', {'hous': house})


# 个人中心(同时能修改昵称和头像)
def My_self(request):
    # 获取登录者信息
    user_id = Get_user(request)
    if request.method == 'GET':
        #

        是否登录
        if user_id:
            # 如果登录才能到个人中心页面

            return render(request, 'cwd/page.html', {'user': user_id})
        else:
            # 返回主界面
            return HttpResponseRedirect('/cwd/index/')
            # 返回没有用户的json格式
            # return JsonResponse(jsonresponse.NO_USER)
    if request.method == 'POST':
        nick_name = request.POST.get('nick_name')
        img_url = request.FILES.get('avatar')
        # path = default_storage.save('../meida/' + img_url.name, ContentFile(img_url.read()))
        # tmp_file = os.path.join(settings.MEDIA_ROOT, path)
        User.objects.filter(user_id=user_id.user_id).update(nick_name=nick_name, avatar=img_url)
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
            house = House.objects.filter()
            return render(request, 'cwd/adv.html', {'house':house})
        else:
            return HttpResponseRedirect('/cwd/index/')


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


# 用户登录
def login(request):
    # get请求获取登录页面
    if request.method == 'GET':
        return render(request, 'cwd/login.html')

    # post请求获取信息
    if request.method == 'POST':
        account = request.POST.get('name')
        password = request.POST.get('password')

        # 判断账号是否存在
        if User.objects.filter(account=account).exists():
            users = User.objects.filter(account=account)  # 获取的是列表类型

            # 检查密码
            if check_password(password, users[0].password):

                # 将登录的账户名传递给session对象

                request.session['account'] = account
                return HttpResponseRedirect('/cwd/index/')
            else:
                return HttpResponse('登录密码错误')
        else:
            return HttpResponse('登录账号错误')
