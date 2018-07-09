from django.conf.urls import url

from xym import views


urlpatterns = [
    # url('^hello/', views.hello)
    #首页
    # url(r'^index/',views.my_home,name='my_index'),
    # #登录
    url(r'^login/',views.login,name='login'),
    # #注册
    # url(r'^register/',views.my_register,name='my_register'),
    #上传新房源
    url(r'^addnewhouse/',views.my_new_house,name='my_new_house'),
    #房源添加后展示
    url(r'^shownewhouse/',views.show_newhouse,name='show_new_house'),
    #成功添加房源后跳转页面
    url(r'^success/', views.show_success, name='show_success'),
    url(r'^removenewhouse/',views.remove_newhouse,name='remove_newhouse')


]