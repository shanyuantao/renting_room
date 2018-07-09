from django.conf.urls import url

from app import views


urlpatterns = [
    url('^hello/', views.hello),
    url('^hello1/', views.hello1),
    url('^adminlogin/', views.adminlogin),
    url('^adminlogout/', views.adminlogout),
    url('^refresh/', views.refresh),
    url('^update_pwd/',views.update_pwd),
    url('^house_manage/(\d+)/', views.house_manage),
    url('^system/', views.system),
    url('^del_house/(\d+)/(\d+)/',views.del_house),
    url('^del_house1/(\d+)/',views.del_house1),
    url('^edit_house/(\d+)/(\d+)/', views.edit_house),
    # url('^edit_house1/(\d+)/(\d+)/', views.edit_house1),
    url('^search/(\d+)/(\w+)/(\w+)/(.+)/(\d+)/', views.search),
    url('^set_avatar/', views.set_avatar),
    url('^manage_account/(\d+)/(.*)/', views.manage_account),
    url('^edit_account/(\d+)/', views.edit_account),
    url('^forbidden_account/(\d+)/(.*)/', views.forbidden_account),
    url('^save_account/(\d+)/(.*)/', views.save_account)

]