import re

from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from app.models import User, House, Forbidden


# 用户注册
def register(request):
    # get请求获取注册页面
    if request.method == 'GET':
        return render(request, 'kai/register.html')

    # post请求获取数据提交至数据库，并返回登录页面
    if request.method == 'POST':
        account = request.POST.get('account')  # 注册账号
        password1 = request.POST.get('password1')  # 密码
        password2 = request.POST.get('password2')  # 密码确认
        phone = request.POST.get('phone')  # 电话号

        if not all([account, password1, password2, phone]):  # 判断注册时信息是否填写完整
            return HttpResponse('注册信息未填完整')

        if not re.match(r'1[34578]\d{9}$', phone):  # 判断注册手机号是否正确
            return HttpResponse('注册手机号有误')

        # if User.objects.filter(User.phone == phone):  # 判断输入手机号是否被注册
        if User.objects.filter(phone=phone).exists():
            return HttpResponse('手机号已被注册')

        if password1 != password2:  # 判断两次密码输入是否一致
            return HttpResponse('两次密码输入不一致')

        password = make_password(password1)  # 哈希加密
        User.objects.create(role_id=1, account=account, password=password, phone=phone)  # 保存信息

        return HttpResponseRedirect('/kaiapp/login')


# 用户登录
def login(request):
    # get请求获取登录页面
    if request.method == 'GET':
        return render(request, 'kai/login.html')

    # post请求获取信息
    if request.method == 'POST':
        account = request.POST.get('account')
        password = request.POST.get('password')

        # 判断账号是否存在
        if User.objects.filter(account=account).exists():
            users = User.objects.filter(account=account)  # 获取的是列表类型
            if Forbidden.objects.filter(user_id=users[0].user_id).exists():
                return HttpResponse('此用户可能涉及违规, 已被封禁')
            # 检查密码
            if check_password(password, users[0].password):

                # 将登录的账户名传递给session对象
                request.session['account'] = account
                return HttpResponseRedirect('/cwd/index/')
            else:
                return HttpResponse('登录密码错误')
        else:
            return HttpResponse('登录账号错误')


# 用户退出
def logout(request):
    if request.method == 'GET':
        # 删除session
        del request.session['account']
        return HttpResponseRedirect('/kaiapp/login/')


# 首页
def index(request):
    # if 'account' in request.session:
    #     return render(request, 'kai/index.html')
    # else:
    #     # return render(request, 'kai/login.html')
    #     return render(request, 'kai/index.html')
    if request.method == 'GET':
        # 获取最新上传的一条房源信息
        latest_data = House.objects.get(house_id=260)
        # latest_data = House.objects.last()

        name = request.session.get('account')  # 获取登录的账户名
        one_data = User.objects.get(account=name) if name else ''  # 获取账户对应的一整条数据库存储数据
        data = {
            'latest_data': latest_data,
            'one_data': one_data
        }
        return render(request, 'kai/index.html', data)
