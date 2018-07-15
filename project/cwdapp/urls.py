from cwdapp import views
from django.conf.urls import url

urlpatterns = [
    # 首页
    url('^index/', views.Index),
    # 我的个人中心
    url('^myself/', views.My_self),
    # 修改密码
    url('^change_pas/', views.Change_password),
    # 我的关注
    url('^like/', views.I_like),
    # 实名认证
    url('^ture/', views.Ture_name),
    # 我发布的房源
    url('^myhouse/', views.My_house),
    # ajax跳转到删除方法
    url('^del/', views.Del),
    # 房屋查询页面
    url('^find/(\d+)/', views.Find),
    url('^search/(.+)/(.+)/(.+)/(\d+)/', views.Search),

]
