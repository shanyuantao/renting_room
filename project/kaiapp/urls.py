from django.conf.urls import url

from kaiapp import views

urlpatterns = [

    # 用户注册
    url(r'^register/', views.register, name='register'),
    # 用户登录
    url(r'^login/', views.login, name='login'),
    # 用户退出
    url(r'^logout/', views.logout, name='logout'),
    # 首页
    url(r'^index/', views.index, name='index'),

]
