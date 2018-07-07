from django.conf.urls import url

from app import views


urlpatterns = [
    # url('^hello/', views.hello)
    #首页
    url(r'^index/',views.my_home,name='my_index'),
    #登录
    url(r'^login/',views.login,name='login'),
    #注册
    url(r'^register/',views.my_register,name='my_register'),
    #上传新房源
    url(r'^addnewhouse/',views.my_new_house,name='my_new_house'),
    #上传房源图片
    # url(r'^checkload/',views.check_load,name='check_load'),



]